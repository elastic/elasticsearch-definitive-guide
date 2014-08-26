=== Partial updates to a document

The `update` API  combines the read and write patterns explained above.

[[img-distrib-update]]
.Partial updates to a document
image::images/04-04_update.png["Partial updates to a document"]

Below we list the sequence of steps used to perform a partial update on  a
document, as depicted in <<img-distrib-update>>:

1. The client sends an update request to `Node 1`.

2. It forwards the request to `Node 3`, where the primary shard is allocated.

3. `Node 3` retrieves the document from the primary shard, changes the JSON
   in the `_source` field, and tries to reindex the document on the primary
   shard. If the document has already been changed by another process, it
   retries step 3 up to `retry_on_conflict` times, before giving up.

4. If `Node 3` has managed to update the document successfully, it forwards
   the new version of the document in parallel to the replica shards on  `Node
   1` and `Node 2` to be reindexed. Once all replica shards report success,
   `Node 3` reports success to the requesting node,  which reports success to
   the client.

The `update` API also accepts the `routing`, `replication`, `consistency` and
`timeout` parameters that are explained in <<distrib-write>>.

.Document based replication
****

When a primary shard forwards changes to its replica shards, it doesn't
forward the update request. Instead it forwards the new version of the full
document. Remember that these changes are forwarded to the replica shards
asynchronously and there is no guarantee that they will arrive in the same
order that they were sent. If Elasticsearch forwarded just the change, it is
possible that changes would be applied in the wrong order, resulting in a
corrupt document.

****
