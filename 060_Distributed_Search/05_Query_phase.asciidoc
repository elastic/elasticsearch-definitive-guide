=== Query Phase

During the initial _query phase_,  the((("distributed search execution", "query phase")))((("query phase of distributed search"))) query is broadcast to a shard copy (a
primary or replica shard) of every shard in the index. Each shard executes
the search locally and ((("priority queue")))builds a _priority queue_ of matching documents.

.Priority Queue
****

A _priority queue_ is just a sorted list that holds the _top-n_ matching
documents. The size of the priority queue depends on the pagination
parameters `from` and `size`.  For example, the following search request
would require a priority queue big enough to hold 100 documents:

[source,js]
--------------------------------------------------
GET /_search
{
    "from": 90,
    "size": 10
}
--------------------------------------------------
****

The query phase process is depicted in <<img-distrib-search>>.

[[img-distrib-search]]
.Query phase of distributed search
image::images/elas_0901.png["Query phase of distributed search"]

The query phase consists of the following three steps:

1. The client sends a `search` request to `Node 3`, which creates an empty
   priority queue of size `from + size`.

2. `Node 3` forwards the search request to a primary or replica copy of every
   shard in the index. Each shard executes the query locally and adds the
   results into a local sorted priority queue of size `from + size`.

3. Each shard returns the doc IDs and sort values of all the docs in its
   priority queue to the coordinating node, `Node 3`, which merges these
   values into its own priority queue to produce a globally sorted list of
   results.

When a search request is sent to a node, that node becomes the coordinating
node.((("nodes", "coordinating node for search requests"))) It is the job of this node to broadcast the search request to all
involved shards, and to gather their responses into a globally sorted result
set that it can return to the client.

The first step is to broadcast the request to a shard copy of every node in
the index. Just like <<distrib-read,document `GET` requests>>, search requests
can be handled by a primary shard or by any of its replicas.((("shards", "handling search requests"))) This is how more
replicas (when combined with more hardware) can increase search throughput.
A coordinating node will round-robin through all shard copies on subsequent
requests in order to spread the load.

Each shard executes the query locally and builds a sorted priority queue of
length `from + size`&#x2014;in other words, enough results to satisfy the global
search request all by itself. It returns a lightweight list of results to the
coordinating node, which contains just the doc IDs and any values required for
sorting, such as the `_score`.

The coordinating node merges these shard-level results into its own sorted
priority queue, which represents the globally sorted result set. Here the query
phase ends.

[NOTE]
====
An index can consist of one or more primary shards,((("indices", "multi-index search"))) so a search request
against a single index needs to be able to combine the results from multiple
shards. A search against _multiple_ or _all_ indices works in exactly the same
way--there are just more shards involved.
====
