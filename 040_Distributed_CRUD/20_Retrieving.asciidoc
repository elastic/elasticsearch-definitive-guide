[[distrib-read]]
=== Retrieving a Document

A document can be retrieved from a ((("documents", "retrieving")))primary shard or from any of its replicas, as shown in <<img-distrib-read>>.

[[img-distrib-read]]
.Retrieving a single document
image::images/elas_0403.png["Retrieving a single document"]

Here is the sequence of steps to retrieve a document from either a
primary or replica shard:

1. The client sends a get request to `Node 1`.

2. The node uses the document's `_id` to determine that the document
   belongs to shard `0`. Copies of shard `0` exist on all three nodes.
   On this occasion, it forwards the request to `Node 2`.

3. `Node 2` returns the document to `Node 1`, which returns the document
   to the client.

For read requests, the requesting node will choose a different shard copy on
every request in order to balance the load; it round-robins through all
shard copies.

It is possible that, while a document is being indexed, the document will
already be present on the primary shard but not yet copied to the replica
shards. In this case, a replica might report that the document doesn't exist,
while the primary would have returned the document successfully. Once the
indexing request has returned success to the user, the document will be
available on the primary and all replica shards.
