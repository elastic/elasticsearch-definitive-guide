==== Then Scale Some More

But what if we want to scale our search to more than six nodes?

The number of primary shards is fixed at the moment an((("indices", "fixed number of primary shards")))((("primary shards", "fixed number in an index"))) index is created.
Effectively, that number defines the maximum amount of data that can be
_stored_ in the index.  (The actual number depends on your data, your hardware
and your use case.) However, read requests--searches or document retrieval--can be handled by a primary _or_ a replica shard, so the more copies of
data that you have, the more search throughput you can handle.

The number of ((("scaling", "increasing number of replica shards")))replica shards can be changed dynamically on a live cluster,
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

As can be seen in <<cluster-three-nodes-two-replicas>>, the `blogs` index now
has nine shards: three primaries and six replicas. This means that we can scale out to
a total of nine nodes, again with one shard per node. This would allow us to
_triple_ search performance compared to our original three-node cluster.

[[cluster-three-nodes-two-replicas]]
.Increasing the `number_of_replicas` to 2
image::images/elas_0205.png["A three-node cluster with two replica shards"]


[NOTE]
===================================================

Of course, just having more replica shards on the same number of nodes doesn't
increase our performance at all because each shard has access to a smaller
fraction of its node's resources.  You need to add hardware to increase
throughput.

But these extra replicas do mean that we have more redundancy: with the node
configuration above, we can now afford to lose two nodes without losing any
data.

===================================================
