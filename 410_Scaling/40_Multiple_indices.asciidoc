[[multiple-indices]]
=== Multiple Indices

Finally, remember that there is no rule that limits your application to using
only a single index.((("scaling", "using multiple indices")))((("indices", "multiple")))  When we issue a search request, it is forwarded to a
copy (a primary or a replica) of all the shards in an index.  If we issue the
same search request on multiple indices, the exact same thing happens--there
are just more shards involved.

TIP: Searching 1 index of 50 shards is exactly equivalent to searching
50 indices with 1 shard each: both search requests hit 50 shards.

This can be a useful fact to remember when you need to add capacity on the
fly.  Instead of having to reindex your data into a bigger index, you can
just do the following:

* Create a new index to hold new data.
* Search across both indices to retrieve new and old data.

In fact, with a little forethought, adding a new index can be done in a
completely transparent way, without your application ever knowing that
anything has changed.

In <<index-aliases>>, we spoke about using an index alias to point to the
current version of your index. ((("index aliases")))((("aliases, index"))) For instance, instead of naming your index
`tweets`, name it `tweets_v1`.  Your application would still talk to `tweets`,
but in reality that would be an alias that points to `tweets_v1`. This allows
you to switch the alias to point to a newer version of the index on the fly.

A similar technique can be used to expand capacity by adding a new index.  It
requires a bit of planning because you will need two aliases: one for
searching and one for indexing:

[source,json]
---------------------------
PUT /tweets_1/_alias/tweets_search <1>
PUT /tweets_1/_alias/tweets_index <1>
---------------------------
<1> Both the `tweets_search` and the `tweets_index` alias point to
    index `tweets_1`.

New documents should be indexed into `tweets_index`,  and searches should be
performed against `tweets_search`.  For the moment, these two aliases point to
the same index.

When we need extra capacity, we can create a new index called `tweets_2` and
update the aliases as follows:

[source,json]
---------------------------
POST /_aliases
{
  "actions": [
    { "add":    { "index": "tweets_2", "alias": "tweets_search" }}, <1>
    { "remove": { "index": "tweets_1", "alias": "tweets_index"  }}, <2>
    { "add":    { "index": "tweets_2", "alias": "tweets_index"  }}  <2>
  ]
}
---------------------------
<1> Add index `tweets_2` to the `tweets_search` alias.
<2> Switch `tweets_index` from `tweets_1` to `tweets_2`.

A search request can target multiple indices, so having the search alias point
to `tweets_1` and `tweets_2` is perfectly valid.  However, indexing requests can
target only a single index. For this reason, we have to switch the index alias
to point to only the new index.

[TIP]
==================================================

A document `GET` request, like((("HTTP methods", "GET")))((("GET method"))) an indexing request, can target only one index.
This makes retrieving a document by ID a bit more complicated in this
scenario.  Instead, run a search request with the
http://bit.ly/1C4Q0cf[`ids` query], or do a((("mget (multi-get) API")))
http://bit.ly/1sDd2EX[`multi-get`] request on `tweets_1` and `tweets_2`.

==================================================

Using multiple indices to expand index capacity on the fly is of particular
benefit when dealing with time-based data such as logs or social-event
streams, which we discuss in the next section.

