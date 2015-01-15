[[retiring-data]]
=== Retiring Data

As time-based data ages, it becomes less relevant.((("scaling", "retiring data")))  It's possible that we
will want to see what happened last week, last month, or even last year, but
for the most part, we're interested in only the here and now.

The nice thing about an index per time frame ((("indices", "index per-timeframe", "deleting old data and")))((("indices", "deleting")))is that it enables us to easily
delete old data: just delete the indices that are no longer relevant:

[source,json]
-------------------------
DELETE /logs_2013*
-------------------------

Deleting a whole index is much more efficient than deleting individual
documents: Elasticsearch just removes whole directories.

But deleting an index is very _final_.  There are a number of things we can
do to help data age gracefully, before we decide to delete it completely.

[[migrate-indices]]
==== Migrate Old Indices

With logging data, there is likely to be one _hot_ index--the index for
today.((("indices", "migrating old indices")))  All new documents will be added to that index, and almost all queries
will target that index.  It should use your best hardware.

How does Elasticsearch know which servers are your best servers? You tell it,
by assigning arbitrary tags to each server.  For instance, you could start a
node as follows:

    ./bin/elasticsearch --node.box_type strong

The `box_type` parameter is completely arbitrary--you could have named it
whatever you like--but you can use these arbitrary values to tell
Elasticsearch where to allocate an index.

We can ensure that today's index is on our strongest boxes by creating it with
the following settings:

[source,json]
-------------------------
PUT /logs_2014-10-01
{
  "settings": {
    "index.routing.allocation.include.box_type" : "strong"
  }
}
-------------------------

Yesterday's index no longer needs to be on our strongest boxes, so we can move
it to the nodes tagged as `medium` by updating its index settings:

[source,json]
-------------------------
POST /logs_2014-09-30/_settings
{
  "index.routing.allocation.include.box_type" : "medium"
}
-------------------------

[[optimize-indices]]
==== Optimize Indices

Yesterday's index is unlikely to change.((("indices", "optimizing")))  Log events are static: what
happened in the past stays in the past.  If we merge each shard down to just a
single segment, it'll use fewer resources and will be quicker to query. We
can do this with the <<optimize-api>>.

It would be a bad idea to optimize the index while it was still allocated to
the `strong` boxes, as the optimization process could swamp the I/O on those
nodes and impact the indexing of today's logs.  But the `medium` boxes aren't
doing very much at all, so we are safe to optimize.

Yesterday's index may have replica shards.((("replica shards", "index optimization and"))) If we issue an optimize request, it
will optimize the primary shard and the replica shards, which is a waste.
Instead, we can remove the replicas temporarily, optimize, and then restore the
replicas:

[source,json]
-------------------------
POST /logs_2014-09-30/_settings
{ "number_of_replicas": 0 }

POST /logs_2014-09-30/_optimize?max_num_segments=1

POST /logs_2014-09-30/_settings
{ "number_of_replicas": 1 }
-------------------------

Of course, without replicas, we run the risk of losing data if a disk suffers
catastrophic failure.  You may((("snapshot-restore API"))) want to back up the data first, with the
http://bit.ly/14ED13A[`snapshot-restore` API].

[[close-indices]]
==== Closing Old Indices

As indices get even older, they reach a point where they are almost never
accessed.((("indices", "closing old indices")))  We could delete them at this stage, but perhaps you want to keep
them around just in case somebody asks for them in six months.

These indices can be closed. They will still exist in the cluster, but they
won't consume resources other than disk space.  Reopening an index is much
quicker than restoring it from backup.

Before closing, it is worth flushing the index to make sure that there are no
transactions left in the transaction log.  An empty transaction log will make
index recovery faster when it is reopened:

[source,json]
-------------------------
POST /logs_2014-01-*/_flush <1>
POST /logs_2014-01-*/_close <2>
POST /logs_2014-01-*/_open <3>
-------------------------
<1> Flush all indices from January to empty the transaction logs.
<2> Close all indices from January.
<3> When you need access to them again, reopen them with the `open` API.

[[archive-indices]]
==== Archiving Old Indices

Finally, very old indices ((("indices", "archiving old indices")))can be archived off to some long-term storage like a
shared disk or Amazon's S3 using the
http://bit.ly/14ED13A[`snapshot-restore` API], just in case you may need
to access them in the future.  Once a backup exists, the index can be deleted
from the cluster.

