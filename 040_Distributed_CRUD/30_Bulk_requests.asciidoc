[[distrib-multi-doc]]
=== Multi-document patterns

The patterns for the `mget` and `bulk` APIs are similar to those for
individual documents. The difference is that the requesting node knows in
which shard each document lives. It breaks up the multi-document request into
a multi-document request _per shard_, and forwards these in parallel to each
participating node.

Once it receives answers from each node, it collates their responses
into a single response, which it returns to the client.

[[img-distrib-mget]]
.Retrieving multiple documents with `mget`
image::images/04-05_mget.png["Retrieving multiple documents with mget"]

Below we list the sequence of steps necessary to retrieve multiple documents
with a single `mget` request, as depicted in <<img-distrib-mget>>:

1. The client sends an `mget` request to `Node 1`.

2. `Node 1` builds a multi-get request per shard, and forwards these
   requests in parallel to the nodes hosting each required primary or replica
   shard. Once all replies have been received, `Node 1` builds the response
   and returns it to the client.

A `routing` parameter can be set for each document in the `docs` array.

[[img-distrib-bulk]]
.Multiple document changes with `bulk`
image::images/04-06_bulk.png["Multiple document changes with bulk"]

Below we list the sequence of steps necessary to execute multiple
`create`, `index`, `delete` and `update` requests within a single
`bulk` request, as depicted in <<img-distrib-bulk>>:

1. The client sends a `bulk` request to `Node 1`.

2. `Node 1` builds a bulk request per shard, and forwards these requests in
    parallel to the nodes hosting each involved primary shard.

3. The primary shard executes each action serially, one after another. As each
   action succeeds, the primary forwards the new document (or deletion) to its
   replica shards in parallel, then moves on to the next action. Once all
   replica shards report success for all actions, the node reports success to
   the requesting node, which collates the responses and returns them to the
   client.

The `bulk` API also accepts the `replication` and `consistency` parameters
at the top-level for the whole `bulk` request, and the `routing` parameter
in the metadata for each request.


