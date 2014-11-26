=== Search Options

A few ((("search options")))optional query-string parameters can influence the search process.

==== preference

The `preference` parameter allows((("preference parameter")))((("search options", "preference"))) you to control which shards or nodes are
used to handle the search request. It accepts values such as `_primary`,
`_primary_first`, `_local`, `_only_node:xyz`, `_prefer_node:xyz`, and
`_shards:2,3`, which are explained in detail on the
http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-request-preference.html[search `preference`]
documentation page.

However, the most generally useful value is some arbitrary string, to avoid
the _bouncing results_ problem.((("bouncing results problem")))

[[bouncing-results]]
.Bouncing Results
****

Imagine that you are sorting your results by a `timestamp` field, and 
two documents have the same timestamp.  Because search requests are
round-robined between all available shard copies, these two documents may be
returned in one order when the request is served by the primary, and in
another order when served by the replica.

This is known as the _bouncing results_ problem: every time the user refreshes
the page, the results appear in a different order. The problem can be avoided by always using the same shards for the same user,
which can be done by setting the `preference` parameter to an arbitrary string
like the user's session ID.

****

==== timeout

By default, the coordinating node waits((("search options", "timeout"))) to receive a response from all shards.
If one node is having trouble, it could slow down the response to all search
requests.

The `timeout` parameter tells((("timeout parameter"))) the coordinating node how long it should wait
before giving up and just returning the results that it already has. It can be
better to return some results than none at all.

The response to a search request will indicate whether the search timed out and
how many shards responded successfully:

[source,js]
--------------------------------------------------
    ...
    "timed_out":     true,  <1>
    "_shards": {
       "total":      5,
       "successful": 4,
       "failed":     1 <2>
    },
    ...
--------------------------------------------------
<1> The search request timed out.
<2> One shard out of five failed to respond in time.

If all copies of a shard fail for other reasons--perhaps because of a
hardware failure--this will also be reflected in the `_shards` section of
the response.

[[search-routing]]
==== routing

In <<routing-value>>, we explained how a custom `routing` parameter((("search options", "routing")))((("routing parameter"))) could be
provided at index time to ensure that all related documents, such as the
documents belonging to a single user, are stored on a single shard.  At search
time, instead of searching on all the shards of an index, you can specify
one or more `routing` values to limit the search to just those shards:

[source,js]
--------------------------------------------------
GET /_search?routing=user_1,user2
--------------------------------------------------

This technique comes in handy when designing very large search systems, and we
discuss it in detail in <<scale>>.

[[search-type]]
==== search_type

While `query_then_fetch` is the default((("query_then_fetch search type")))((("search options", "search_type")))((("search_type"))) search type, other search types can
be specified for particular purposes, for example:

[source,js]
--------------------------------------------------
GET /_search?search_type=count
--------------------------------------------------

`count`::

The `count` search type has only a `query` phase.((("count search type")))  It can be used when you
don't need search results, just a document count or
<<aggregations,aggregations>> on documents matching the query.

`query_and_fetch`::

The `query_and_fetch` search type ((("query_and_fetch serch type")))combines the query and fetch phases into a
single step.  This is an internal optimization that is used when a search
request targets a single shard only, such as when a
<<search-routing,`routing`>> value has been specified. While you can choose
to use this search type manually, it is almost never useful to do so.

`dfs_query_then_fetch` and `dfs_query_and_fetch`::

The `dfs` search types((("dfs search types"))) have a prequery phase that fetches the term
frequencies from all involved shards in order to calculate global term
frequencies. We discuss this further in <<relevance-is-broken>>.

`scan`::

The `scan` search type is((("scan search type"))) used in conjunction with the `scroll` API ((("scroll API")))to
retrieve large numbers of results efficiently. It does this by disabling
sorting.  We discuss _scan-and-scroll_ in the next section.




