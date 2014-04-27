=== Add failover

Running a single node means that you have a single point of failure -- there
is no redundancy. Fortunately all we need to do to protect ourselves from data
loss is to start another node. A new node will join the cluster automatically
as long as it has the same cluster name set in its config file, and it can
talk to the other nodes.

If we start a second node, our cluster would look like <<cluster-two-nodes>>.

[[cluster-two-nodes]]
.A two-node cluster -- all primary and replica shards are allocated
image::images/02-03_two_nodes.png["A two-node cluster"]

The second node has joined the cluster and three _replica shards_ have been
allocated to it -- one for each primary shard.  That means that we can lose
either node and all of our data will be intact.

Any newly indexed document will first be stored on a primary shard, then
copied in parallel to the associated replica shard(s). This ensures that our
document can be retrieved from a primary shard or from any of its replicas.

The `cluster-health` now shows a status of `green`, which means that all 6
shards (all 3 primary shards and all 3 replica shards) are active:

[source,js]
--------------------------------------------------
{
   "cluster_name":          "elasticsearch",
   "status":                "green", <1>
   "timed_out":             false,
   "number_of_nodes":       2,
   "number_of_data_nodes":  2,
   "active_primary_shards": 3,
   "active_shards":         6,
   "relocating_shards":     0,
   "initializing_shards":   0,
   "unassigned_shards":     0
}
--------------------------------------------------
<1> Cluster `status` is `green`.

Our cluster is not only fully functional but also _always available_.
