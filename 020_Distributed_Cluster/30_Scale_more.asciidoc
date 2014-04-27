==== Then scale some more

But what if we want to scale our search to more than 6 nodes?

The number of primary shards is fixed at the moment an index is created.
Effectively, that number defines the maximum amount of data that can be
*stored* in the index.  (The actual number depends on your data, your hardware
and your use case). However, read requests -- searches or document retrieval
-- can be handled by a primary *or* a replica shard, so the more copies of
data that you have, the more search throughput we can handle.

The number of replica shards can be changed dynamically on a live cluster,
allowing us to scale up or down as demand requires. Let's increase the number
of replicas from the default of `1` to `2`:

[source,js]
--------------------------------------------------
PUT /blogs/_settings
{
   "number_of_replicas" : 2
}
--------------------------------------------------
// SENSE: 020_Distributed_Cluster/30_Replicas.json

[[cluster-three-nodes-two-replicas]]
.Increasing the `number_of_replicas` to 2
image::images/02-05_replicas.png["A three-node cluster with two replica shards"]

As can be seen in <<cluster-three-nodes-two-replicas>>, the `blogs` index now
has 9 shards: 3 primaries and 6 replicas. If we were to add another three
nodes to our 6 node cluster, we would again have one shard per node, and our
cluster would be able to handle *50%* more search requests than before.

[NOTE]
===================================================

Of course, just having more replica shards on the same number of nodes doesn't
increase our performance at all because each shard has access to a smaller
fraction of its node's resources.  You need to add hardware to increase
throughput.

But these extra replicas do mean that we have more redundancy. With the node
configuration above, we can now afford to lose two nodes without losing any
data.

===================================================
