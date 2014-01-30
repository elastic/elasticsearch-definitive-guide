=== Cache key

The lookup example works great from the developer's point of view...but it is
going to make your filter cache very unhappy.  If you were to run this type
of query in production and watch the filter cache stats, you'd see a large
amount of evictions -- the dreaded cache churn we discussed in
<<_controlling_caching>>.

So what's going on?  To understand the problem, we need to understand how
Elasticsearch names the filters in memory.  Cached filters are stored in a map,
and each entry has a key name which is used to retrieve the filter.

By default, Elasticsearch uses the filter itself as the key.  When
parsing a query, it can simply take the entire filter contents and uses that as
the key.

As a simple example, a filter map may look like this:


    |----------------------------------------------------------------|
    |        Terms          |        Key            |     Bitset     |
    |----------------------------------------------------------------|
    | marketing             | "marketing"           | 01101011001010 |
    | sales, pr             | "sales_pr"            | 11010011111011 |
    | management, sales, pr | "management_sales_pr" | 11110111111011 |
    | engineering           | "engineering"         | 00000011001010 |
    |----------------------------------------------------------------|

As you can see, we have a list of `terms` filters.  The key is simply
the list of terms concatenated together.  Filters need to be uniquely identified,
so the filter itself works as a perfect unique key.

.Does term order matter?
****
You may wonder if the order of terms matters.  For example, is
`{"terms" : ["a", "b"]}` cached separately from `{"terms" : ["b", "a"]}`?

The answer is no, they are not cached separately.  In reality, Elasticsearch
sorts the terms and caches the filter *object* itself, not a string concatenation.
But this complicates the subject, so you can safely think of the map keys as
strings where term order does not matter.
****

This approach can, however, lead to certain edge-cases where memory usage balloons
out of control.  Our previous twitter example -- aka `terms` filters with
10,000 terms -- is one such example

Elasticsearch will simply concatenate all 10,000 terms together...which means
the key itself may potentially use more memory than the cached bitset!
Obviously, this is not ideal.  The way to fix this is to manually over-ride
the cache key using an option called `_cache_key`.  Instead of concatenating
all the terms together, Elasticsearch will use the key name that you provide.

If we tweak our lookup example from before, we can manually assign a key name:

[source,js]
--------------------------------------------------
GET /my_index/users/_search
{
  "query" : {
    "filtered" : {
      "filter" : {
        "terms" : {
          "user" : {
            "index" : "my_index",
            "type" : "user_following",
            "id" : "1",
            "path" : "following"
          },
          "_cache_key" : "user_following_1" <1>
        }
      }
    }
  }
}
--------------------------------------------------
<1> We manually add a cache key, arbitrarily set to some unique value

For this example, we are setting the cache key to the type + field name + user
ID.  The actual key value doesn't really matter, so long as it is unique to the
filter and short.  Depending on your business requirements, it may make sense
to simply hash the list of IDs (with SHA1, etc) and use that as a key.

._cache_key's cannot be automatically evicted
****
If you use custom _cache_key's, you need to manually evict them from cache
when appropriate.  In our twitter example, if you were to add a new "following"
ID to the document, the saved cache is no longer valid and needs to be manually
removed.

You can do this with the Clear Cache API, which will clear the cache for our
"following" field:

[source,js]
--------------------------------------------------
POST /my_index/_cache/clear?filter=true&fields=following
--------------------------------------------------

Alternatively, you can set a timeout for the filter cache which will expire
filters after a certain age.  This is set using the Update Cluster Settings API:

[source,js]
--------------------------------------------------
POST /_cluster/settings
{
  "persistent" : {
    "indices.cache.filter.expire" : "10m"
  }
}
--------------------------------------------------

This is a less useful method, however, since it affects your entire cluster
and filters which are not using a _custom_cache key.
****
