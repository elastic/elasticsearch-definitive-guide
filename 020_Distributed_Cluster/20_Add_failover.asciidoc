=== Add Failover

Running a single node means that you have a single point of failure--there
is no redundancy.((("failover, adding"))) Fortunately, all we need to do to protect ourselves from data
loss is to start another node.

.Starting a Second Node
***************************************

To test what happens when you add a second((("nodes", "starting a second node"))) node, you can start a new node
in exactly the same way as you started the first one (see
<<running-elasticsearch>>), and from the same directory. Multiple nodes can
share the same directory.

As long as the second node has the same `cluster.name` as the first node (see
the `./config/elasticsearch.yml` file), it should automatically discover and
join the cluster run by the first node. If it doesn't, check the logs to find
out what went wrong.  It may be that multicast is disabled on your network, or
that a firewall is preventing your nodes from communicating.

***************************************

If we start a second node, our cluster would look like <<cluster-two-nodes>>.

[[cluster-two-nodes]]
.A two-node cluster--all primary and replica shards are allocated
image::images/elas_0203.png["A two-node cluster"]

The((("clusters", "two-node cluster"))) second node has joined the cluster, and three _replica shards_ have ((("replica shards", "allocated to second node")))been
allocated to it--one for each primary shard.  That means that we can lose
either node, and all of our data will be intact.

Any newly indexed document will first be stored on a primary shard, and then copied in parallel to the associated replica shard(s). This ensures that our document can be retrieved from a primary shard or from any of its replicas.

The `cluster-health` now ((("cluster health", "checking after adding second node")))shows a status of `green`, which means that all six
shards (all three primary shards and all three replica shards) are active:

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

Our cluster is not only fully functional, but also _always available_.
