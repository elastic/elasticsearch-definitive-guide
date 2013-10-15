[[reindex-optimize]]
=== Optimizing the reindexing process

Usually, while you are reindexing your data, the new index is not being
used for search. It makes sense to disable some of the high availablity and
real time search features temporarily in order to speed up reindexing.

====  `number_of_replicas`

The new index does not need replicas during reindexing.  All of your data
is safely stored in the old index.  If you have any replicas then indexing
needs to happen both on the primary shard and the replicas, which consumes
more resources within your cluster.

Instead, if you set the `number_of_replicas` to zero, then indexing only
happens on the primary shard.  Once you have finished reindexing, you can
set `number_of_replicas` back to the number you need, and the primary
shard will just be copied over to the appropriate node.

==== `refresh_interval`

By default, Elasticsearch _refreshes_ its ``view'' on search once every
second.  While this is a lightweight operation, it still has a cost.
We are not using the new index for search yet, so it makes sense
to disable refresh by setting the `refresh_interval` to `-1` during
reindexing.

==== `flush_threshold_ops`

All index and delete operations are written to a transaction log and
added to an in-memory buffer.  When the transaction log is full,
Elasticsearch performs a flush:

 * the buffer is converted to an inverted index and written to disk
 * a new Lucene _commit point_ is written to disk
 * the transaction log is truncated
 * and the disk is fsync'ed

This is a heavier operation than a refresh. We can achieve faster throughput
by flushing less frequently.  By default, a flush happens
every 5,000 operations, but this can be increased to 20,000.

NOTE: We will explain more about the refresh and flush processes in <<lucene>>.

==== Before reindexing

When you create your new index, include the above optimizations as follows:

[source,js]
--------------------------------------------------
PUT /new_index
{
    "settings": {
        "number_of_replicas":            0,
        "refresh_interval":              -1,
        "translog.flush_threshold_ops":  20000
    },
    "mappings": { ... }
}
--------------------------------------------------


==== After reindexing

Once you have finished reindexing, you can update the index settings
to be suitable for highly available real time search:

[source,js]
--------------------------------------------------
PUT /new_index/_settings
{
    "number_of_replicas":             1,
    "refresh_interval":               "1s",
    "translog.flush_threshold_ops":   5000
}
--------------------------------------------------


It will take a little time to allocate the replica shards but, as soon
as that is complete, your index is ready to use.


