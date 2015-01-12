[[backing-up-your-cluster]]
=== Backing Up Your Cluster

As with any software that stores data, it is important to routinely back up your
data. ((("clusters", "backing up")))((("post-deployment", "backing up your cluster")))((("backing up your cluster"))) Elasticsearch replicas provide high availability during runtime; they allow
you to tolerate sporadic node loss without an interruption of service.

Replicas do not provide protection from catastrophic failure, however.  For that,
you need a real backup of your cluster--a complete copy in case something goes
wrong.

To back up your cluster, you can use the `snapshot` API.((("snapshot-restore API")))  This will take the current
state and data in your cluster and save it to a shared repository.  This
backup process is "smart."  Your first snapshot will be a complete copy of data,
but all subsequent snapshots will save the _delta_ between the existing
snapshots and the new data.  Data is incrementally added and deleted as you snapshot
data over time.  This means subsequent backups will be substantially
faster since they are transmitting far less data.

To use this functionality, you must first create a repository to save data.
There are several repository types that you may choose from:

- Shared filesystem, such as a NAS
- Amazon S3
- HDFS (Hadoop Distributed File System)
- Azure Cloud

==== Creating the Repository

Let's set up a shared ((("backing up your cluster", "creating the repository")))((("filesystem repository")))filesystem repository:

[source,js]
----
PUT _snapshot/my_backup <1>
{
    "type": "fs", <2>
    "settings": {
        "location": "/mount/backups/my_backup" <3>
    }
}
----
<1> We provide a name for our repository, in this case it is called `my_backup`.
<2> We specify that the type of the repository should be a shared filesystem.
<3> And finally, we provide a mounted drive as the destination.

NOTE: The shared filesystem path must be accessible from all nodes in your
cluster!

This will create the repository and required metadata at the mount point.  There
are also some other options that you may want to configure, depending on the
performance profile of your nodes, network, and repository location:

`max_snapshot_bytes_per_sec`::
    When snapshotting data into the repo, this controls
the throttling of that process.  The default is `20mb` per second.

`max_restore_bytes_per_sec`::
When restoring data from the repo, this controls
how much the restore is throttled so that your network is not saturated.  The
default is `20mb` per second.

Let's assume we have a very fast network and are OK with extra traffic, so we
can increase the defaults:

[source,js]
----
POST _snapshot/my_backup/ <1>
{
    "type": "fs",
    "settings": {
        "location": "/mount/backups/my_backup",
        "max_snapshot_bytes_per_sec" : "50mb", <2>
        "max_restore_bytes_per_sec" : "50mb"
    }
}
----
<1> Note that we are using a `POST` instead of `PUT`.  This will update the settings
of the existing repository.
<2> Then add our new settings.

==== Snapshotting All Open Indices

A repository can contain multiple snapshots.((("indices", "open, snapshots on")))((("backing up your cluster", "snapshots on all open indexes")))  Each snapshot is associated with a
certain set of indices (for example, all indices, some subset, or a single index).  When
creating a snapshot, you specify which indices you are interested in and
give the snapshot a unique name.

Let's start with the most basic snapshot command:

[source,js]
----
PUT _snapshot/my_backup/snapshot_1
----

This will back up all open indices into a snapshot named `snapshot_1`, under the
`my_backup` repository.  This call will return immediately, and the snapshot will
proceed in the background.

[TIP]
==================================================

Usually you'll want your snapshots to proceed as a background process, but occasionally
you may want to wait for completion in your script.  This can be accomplished by
adding a `wait_for_completion` flag:

[source,js]
----
PUT _snapshot/my_backup/snapshot_1?wait_for_completion=true
----

This will block the call until the snapshot has completed.  Note that large snapshots
may take a long time to return!

==================================================

==== Snapshotting Particular Indices

The default behavior is to back up all open indices.((("indices", "snapshotting particular")))((("backing up your cluster", "snapshotting particular indices")))  But say you are using Marvel,
and don't really want to back up all the diagnostic `.marvel` indices.  You
just don't have enough space to back up everything.

In that case, you can specify which indices to back up when snapshotting your cluster:

[source,js]
----
PUT _snapshot/my_backup/snapshot_2
{
    "indices": "index_1,index_2"
}
----

This snapshot command will now back up only `index1` and `index2`.

==== Listing Information About Snapshots

Once you start accumulating snapshots in your repository, you may forget the details((("backing up your cluster", "listing information about snapshots")))
relating to each--particularly when the snapshots are named based on time
demarcations (for example, `backup_2014_10_28`).

To obtain information about a single snapshot, simply issue a `GET` reguest against
the repo and snapshot name:

[source,js]
----
GET _snapshot/my_backup/snapshot_2
----

This will return a small response with various pieces of information regarding
the snapshot:

[source,js]
----
{
   "snapshots": [
      {
         "snapshot": "snapshot_1",
         "indices": [
            ".marvel_2014_28_10",
            "index1",
            "index2"
         ],
         "state": "SUCCESS",
         "start_time": "2014-09-02T13:01:43.115Z",
         "start_time_in_millis": 1409662903115,
         "end_time": "2014-09-02T13:01:43.439Z",
         "end_time_in_millis": 1409662903439,
         "duration_in_millis": 324,
         "failures": [],
         "shards": {
            "total": 10,
            "failed": 0,
            "successful": 10
         }
      }
   ]
}
----

For a complete listing of all snapshots in a repository, use the `_all` placeholder
instead of a snapshot name:

[source,js]
----
GET _snapshot/my_backup/_all
----

==== Deleting Snapshots

Finally, we need a command to delete old snapshots that ((("backing up your cluster", "deleting old snapshots")))are no longer useful.
This is simply a `DELETE` HTTP call to the repo/snapshot name:

[source,js]
----
DELETE _snapshot/my_backup/snapshot_2
----

It is important to use the API to delete snapshots, and not some other mechanism
(such as deleting by hand, or using automated cleanup tools on S3).  Because snapshots are
incremental, it is possible that many snapshots are relying on old segments.
The `delete` API understands what data is still in use by more recent snapshots,
and will delete only unused segments.

If you do a manual file delete, however, you are at risk of seriously corrupting
your backups because you are deleting data that is still in use.


==== Monitoring Snapshot Progress

The `wait_for_completion` flag provides a rudimentary form of monitoring, but
really isn't sufficient when snapshotting or restoring even moderately sized clusters.

Two other APIs will give you more-detailed status about the
state of the snapshotting.  First you can execute a `GET` to the snapshot ID,
just as we did earlier get information about a particular snapshot:

[source,js]
----
GET _snapshot/my_backup/snapshot_3
----

If the snapshot is still in progress when you call this, you'll see information
about when it was started, how long it has been running, and so forth.  Note, however,
that this API uses the same threadpool as the snapshot mechanism.  If you are
snapshotting very large shards, the time between status updates can be quite large,
since the API is competing for the same threadpool resources.

A better option is to poll the `_status` API:

[source,js]
----
GET _snapshot/my_backup/snapshot_3/_status
----

The `_status` API returns immediately and gives a much more verbose output of
statistics:

[source,js]
----
{
   "snapshots": [
      {
         "snapshot": "snapshot_3",
         "repository": "my_backup",
         "state": "IN_PROGRESS", <1>
         "shards_stats": {
            "initializing": 0,
            "started": 1, <2>
            "finalizing": 0,
            "done": 4,
            "failed": 0,
            "total": 5
         },
         "stats": {
            "number_of_files": 5,
            "processed_files": 5,
            "total_size_in_bytes": 1792,
            "processed_size_in_bytes": 1792,
            "start_time_in_millis": 1409663054859,
            "time_in_millis": 64
         },
         "indices": {
            "index_3": {
               "shards_stats": {
                  "initializing": 0,
                  "started": 0,
                  "finalizing": 0,
                  "done": 5,
                  "failed": 0,
                  "total": 5
               },
               "stats": {
                  "number_of_files": 5,
                  "processed_files": 5,
                  "total_size_in_bytes": 1792,
                  "processed_size_in_bytes": 1792,
                  "start_time_in_millis": 1409663054859,
                  "time_in_millis": 64
               },
               "shards": {
                  "0": {
                     "stage": "DONE",
                     "stats": {
                        "number_of_files": 1,
                        "processed_files": 1,
                        "total_size_in_bytes": 514,
                        "processed_size_in_bytes": 514,
                        "start_time_in_millis": 1409663054862,
                        "time_in_millis": 22
                     }
                  },
                  ...
----
<1> A snapshot that is currently running will show `IN_PROGRESS` as its status.
<2> This particular snapshot has one shard still transferring (the other four have already completed).

The response includes the overall status of the snapshot, but also drills down into
per-index and per-shard statistics.  This gives you an incredibly detailed view
of how the snapshot is progressing.  Shards can be in various states of completion:

`INITIALIZING`::
    The shard is checking with the cluster state to see whether it can
be snapshotted.  This is usually very fast.

`STARTED`::
    Data is being transferred to the repository.
    
`FINALIZING`::
    Data transfer is complete; the shard is now sending snapshot metadata.
    
`DONE`::
    Snapshot complete!
    
`FAILED`::
    An error was encountered during the snapshot process, and this shard/index/snapshot
could not be completed.  Check your logs for more information.


==== Canceling a Snapshot

Finally, you may want to cancel a snapshot or restore.((("backing up your cluster", "canceling a snapshot")))  Since these are long-running
processes, a typo or mistake when executing the operation could take a long time to
resolve--and use up valuable resources at the same time.

To cancel a snapshot, simply delete the snapshot while it is in progress:

[source,js]
----
DELETE _snapshot/my_backup/snapshot_3
----

This will halt the snapshot process. Then proceed to delete the half-completed
snapshot from the repository.


