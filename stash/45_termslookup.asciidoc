=== Social-graph filter

Let's start this section with a problem:  You follow 10,000 people on Twitter
and want to see what they've been tweeting int he last 24 hours.  How would
you implement this in Elasticsearch?

There are a couple ways to implement it. The obvious way to accomplish this is
by maintaining a document that specifies all the users that you follow:

[source,js]
--------------------------------------------------
PUT /my_index/user_following/1
{ "following" : [2, 4] }
--------------------------------------------------

Every time you follow or un-follow a new person, this document will be updated:

[source,js]
--------------------------------------------------
PUT /my_index/user_following/1/_update
{
    "script" : "ctx._source.following += user",
    "params" : {
        "user" : 5
    }
}
--------------------------------------------------

To find the tweets of the people you follow, you must perform a GET on the
document to obtain the list of users, then a second query with those user IDs in
a Terms filter:

[source,js]
--------------------------------------------------
GET /my_index/user_following/1

GET /my_index/users/_search
{
  "query" : {
    "filtered" : {
      "filter" : {
        "terms" : {
          "user" : [2, 4, 5]
        }
      }
    }
  }
}
--------------------------------------------------


This approach works, but is inefficient (and annoying for the developer). Each
query requires two full round-trips to the server before you have useful data
to work with.

In SQL parlance, you might solve this problem by using a subquery.  The
inner subquery retrieves a list of IDs from a particular row, which is then
used in the parent query to find the rows corresponding to those IDs:

[source,sql]
--------------------------------------------------
SELECT user
FROM   users
WHERE  id IN (SELECT following
              FROM   user_following
              WHERE  id = 1)
--------------------------------------------------


The `terms` filter has a feature which is similar to a subquery.  Called a
`lookup`, it allows the filter to load values directly from a document rather
than from the query body.  This simplifies the code for a developer, and avoids
an unnecessary round-trip.

If we tweak our query just a little, we get this:

[source,js]
--------------------------------------------------
GET /my_index/users/_search
{
  "query" : {
    "filtered" : {
      "filter" : {
        "terms" : {
          "user" : {
            "index" : "my_index", <1>
            "type" : "user_following",
            "id" : "1",
            "path" : "following" <2>
          }
        }
      }
    }
  }
}
--------------------------------------------------
<1> The `index`, `type`, and `id` specify the path to the document containing
the IDs we want to load.  In this case it specifies `/my_index/user_following/1`
<2> `path` is the field that contains the IDs

In this query, we have a few new properties that facilitate the lookup process.
`index`, `type` and `id` allow you to specify where the document lives in
your elasticsearch cluster.  `Path` controls which field should be loaded
as the terms list.

The filter will now retrieve the list of user IDs from the document, rather than
from the request body.  This saves network round-trips, but it is also cached
by Elasticsearch so that subsequent requests will be faster.  If you need
to specify large lists of terms, consider the `lookup` feature.

.Cross-index lookup
****
It's important to note that the document you are "looking up" doesn't need to
reside in the same index as your search query.  You can easily search one index
and extract terms from a different index.

This can give you considerable flexibility when organizing data, but it can also
give extra performance.

Elasticsearch prefers to get the lookup document locally if possible,
since this avoids an inter-cluster round-trip to get the document.  An easy
performance trick is auto-replicating your "lookup" index to all nodes.

This guarantees a local copy of all lookup documents on each node, which makes
all `terms` lookups very fast.

This does have a disadvantage though: it fundamentally limits how much you can
scale your "lookup" index.  A better solution is to use custom routing, which
will be discussed in
****



