[[empty-search]]
=== The Empty Search

The most basic form of the((("searching", "empty search")))((("empty search"))) search API is the _empty search_, which doesn't
specify any query but simply returns all documents in all indices in the
cluster:

[source,js]
--------------------------------------------------
GET /_search
--------------------------------------------------
// SENSE: 050_Search/05_Empty_search.json

The response (edited for brevity) looks something like this:

[source,js]
--------------------------------------------------
{
   "hits" : {
      "total" :       14,
      "hits" : [
        {
          "_index":   "us",
          "_type":    "tweet",
          "_id":      "7",
          "_score":   1,
          "_source": {
             "date":    "2014-09-17",
             "name":    "John Smith",
             "tweet":   "The Query DSL is really powerful and flexible",
             "user_id": 2
          }
       },
        ... 9 RESULTS REMOVED ...
      ],
      "max_score" :   1
   },
   "took" :           4,
   "_shards" : {
      "failed" :      0,
      "successful" :  10,
      "total" :       10
   },
   "timed_out" :      false
}
--------------------------------------------------


==== hits

The most important section of the response is `hits`, which((("searching", "empty search", "hits")))((("hits"))) contains the
`total` number of documents that matched our query, and a `hits` array
containing the first 10 of those matching documents--the results.

Each result in the `hits` array contains the `_index`, `_type`, and `_id` of
the document, plus the `_source` field.  This means that the whole document is
immediately available to us directly from the search results. This is unlike
other search engines, which return just the document ID, requiring you to fetch
the document itself in a separate step.

Each element also ((("score", "for empty search")))((("relevance scores")))has a `_score`.  This is the _relevance score_, which is a
measure of how well the document matches the query.  By default, results are
returned with the most relevant documents first; that is, in descending order
of `_score`. In this case, we didn't specify any query, so all documents are
equally relevant, hence the neutral `_score` of `1` for all results.

The `max_score` value is the highest `_score` of any document that matches our
query.((("max_score value")))

==== took

The `took` value((("took value (empty search)"))) tells us how many milliseconds the entire search request took
to execute.

==== shards

The `_shards` element((("shards", "number involved in an empty search"))) tells us the `total` number of shards that were involved
in the query and,((("failed shards (in a search)")))((("successful shards (in a search)"))) of them, how many were `successful` and how many `failed`.
We wouldn't normally expect shards to fail, but it can happen. If we were to
suffer a major disaster in which we lost both the primary and the replica copy
of the same shard, there would be no copies of that shard available to respond
to search requests. In this case, Elasticsearch would report the shard as
`failed`, but continue to return results from the remaining shards.

==== timeout

The `timed_out` value tells((("timed_out value in search results"))) us whether the query timed out.  By
default, search requests do not time out.((("timeout parameter", "specifying in a request")))  If low response times are more
important to you than complete results, you can specify a `timeout` as `10`
or `10ms` (10 milliseconds), or `1s` (1 second):

[source,js]
--------------------------------------------------
GET /_search?timeout=10ms
--------------------------------------------------


Elasticsearch will return any results that it has managed to gather from
each shard before the requests timed out.

[WARNING]
================================================

It should be noted that this `timeout` does not((("timeout parameter", "not halting query execution"))) halt the execution of the
query; it merely tells the coordinating node to return the results collected
_so far_ and to close the connection.  In the background, other shards may
still be processing the query even though results have been sent.

Use the time-out because it is important to your SLA, not because you want
to abort the execution of long-running queries.

================================================

