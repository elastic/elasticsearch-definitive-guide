[role="pagebreak-before"]
=== Rolling Restarts

There will come a time when you need to perform a rolling restart of your
cluster--keeping the cluster online and operational, but taking nodes offline
one at a time.((("rolling restart of your cluster")))((("clusters", "rolling restarts")))((("post-deployment", "rolling restarts")))

The common reason is either an Elasticsearch version upgrade, or some kind of
maintenance on the server itself (such as an OS update, or hardware).  Whatever the case,
there is a particular method to perform a rolling restart.

By nature, Elasticsearch wants your data to be fully replicated and evenly balanced.
If you shut down a single node for maintenance, the cluster will
immediately recognize the loss of a node and begin rebalancing.  This can be irritating
if you know the node maintenance is short term, since the rebalancing of
very large shards can take some time (think of trying to replicate 1TB--even
on fast networks this is nontrivial).

What we want to do is tell Elasticsearch to hold off on rebalancing, because
we have more knowledge about the state of the cluster due to external factors.
The procedure is as follows:

1. If possible, stop indexing new data.  This is not always possible, but will
help speed up recovery time.

2. Disable shard allocation.  This prevents Elasticsearch from rebalancing
missing shards until you tell it otherwise.  If you know the maintenance window will be
short, this is a good idea.  You can disable allocation as follows:
+
[source,js]
----
PUT /_cluster/settings
{
    "transient" : {
        "cluster.routing.allocation.enable" : "none"
    }
}
----

3. Shut down a single node, preferably using the `shutdown` API on that particular
machine:
+
[source,js]
----
POST /_cluster/nodes/_local/_shutdown
----

4. Perform a maintenance/upgrade.
5. Restart the node, and confirm that it joins the cluster.
6. Reenable shard allocation as follows:
+
[source,js]
----
PUT /_cluster/settings
{
    "transient" : {
        "cluster.routing.allocation.enable" : "all"
    }
}
----
+
Shard rebalancing may take some time.  Wait until the cluster has returned
to status `green` before continuing.

7. Repeat steps 2 through 6 for the rest of your nodes.

8. At this point you are safe to resume indexing (if you had previously stopped),
but waiting until the cluster is fully balanced before resuming indexing will help
to speed up the process.

