[[distrib-write]]
=== Creating, Indexing, and Deleting a Document

Create, index, and delete((("documents", "creating, indexing, and deleting"))) requests are _write_ operations,((("write operations"))) which must be
successfully completed on the primary shard before they can be copied to any
associated replica shards, as shown in <<img-distrib-write>>.

[[img-distrib-write]]
.Creating, indexing, or deleting a single document
image::images/elas_0402.png["Creating, indexing or deleting a single document"]

Here is the sequence ((("primary shards", "creating, indexing, and deleting a document")))((("replica shards", "creating, indexing, and deleting a document")))of steps necessary to successfully create, index, or
delete a document on both the primary and any replica shards:

1. The client sends a create, index, or delete request to `Node 1`.

2. The node uses the document's `_id` to determine that the document
   belongs to shard `0`. It forwards the request to `Node 3`,
   where the primary copy of shard `0` is currently allocated.

3. `Node 3` executes the request on the primary shard. If it is successful,
   it forwards the request in parallel to the replica shards on `Node 1` and
   `Node 2`. Once all of the replica shards report success, `Node 3` reports
   success to the requesting node, which reports success to the client.

By the time the client receives a successful response, the document change has
been executed on the primary shard and on all replica shards. Your change is
safe.

There are a number of optional request parameters that allow you to influence
this process, possibly increasing performance at the cost of data security.
These options are seldom used because Elasticsearch is already fast, but they
are explained here for the sake of completeness:

`replication`::
+
--
The default value for ((("replication request parameter", "sync and async values")))replication is `sync`. ((("sync value, replication parameter")))This causes the primary shard to
wait for successful responses from the replica shards before returning.

If you set `replication` to `async`,((("async value, replication parameter"))) it will return success to the client
as soon as the request has been executed on the primary shard. It will still
forward the request to the replicas, but you will not know whether the replicas
succeeded.

This option is mentioned specifically to advise against using it.  The default
`sync` replication allows Elasticsearch to exert back pressure on whatever
system is feeding it with data. With `async` replication, it is possible to
overload Elasticsearch by sending too many requests without waiting for their
completion.

--

`consistency`::
+
--
By default, the primary shard((("consistency request parameter")))((("quorum"))) requires a _quorum_, or majority, of shard copies
(where a shard copy can be a primary or a replica shard) to be available
before even attempting a write operation. This is to prevent writing data to the
``wrong side'' of a network partition.  A quorum is defined as follows:

    int( (primary + number_of_replicas) / 2 ) + 1

The allowed values for `consistency` are `one` (just the primary shard), `all`
(the primary and all replicas), or the default `quorum`, or majority, of shard
copies.

Note that the `number_of_replicas` is the number of replicas _specified_ in
the index settings, not the number of replicas that are currently active.  If
you have specified that an index should have three replicas, a quorum would
be as follows:

    int( (primary + 3 replicas) / 2 ) + 1 = 3

But if you start only two nodes, there will be insufficient active shard
copies to satisfy the quorum, and you will be unable to index or delete any
documents.

--

`timeout`::

What happens if insufficient shard copies are available? Elasticsearch waits,
in the hope that more shards will appear.  By default, it will wait up to 1
minute. If you need to, you can use the `timeout` parameter((("timeout parameter"))) to make it abort
sooner: `100` is 100 milliseconds, and `30s` is 30 seconds.

[NOTE]
===================================================
A new index has `1` replica by default, which means that two active shard
copies _should_ be required in order to satisfy the need for a `quorum`.
However, these default settings would prevent us from doing anything useful
with a single-node cluster.  To avoid this problem, the requirement for
a quorum is enforced only when `number_of_replicas` is greater than `1`.
===================================================
