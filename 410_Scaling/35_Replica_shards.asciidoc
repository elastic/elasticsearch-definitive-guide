[[replica-shards]]
=== Replica Shards

Up until now we have spoken only about primary shards, but we have another
tool in our belt: replica shards.((("scaling", "replica shards")))((("shards", "replica")))((("replica shards")))  The main purpose of replicas is for
failover, as discussed in <<distributed-cluster>>: if the node holding a
primary shard dies, a replica is promoted to the role of primary.

At index time, a replica shard does the same amount of work as the primary
shard.  New documents are first indexed on the primary and then on any
replicas.  Increasing the number of replicas does not change the capacity of
the index.

However, replica shards can serve read requests.  If, as is often the case,
your index is search heavy, you can increase search performance by increasing
the number of replicas, but only if you also _add extra hardware_.

Let's return to our example of an index with two primary shards.  We increased
capacity of the index by adding a second node. Adding more nodes would not
help us to add indexing capacity, but we could take advantage of the extra
hardware at search time by increasing the number of replicas:

[source,json]
-----------------------
POST /my_index/_settings
{
  "number_of_replicas": 1
}
-----------------------

Having two primary shards, plus a replica of each primary, would give us a
total of four shards: one for each node, as shown in <<img-four-nodes>>.

[[img-four-nodes]]
.An index with two primary shards and one replica can scale out across four nodes
image::images/elas_4403.png["An index with two primary shards and one replica can scale out across four nodes"]

==== Balancing Load with Replicas

Search performance depends on the response times of the slowest node, so it is a good idea to try to balance out the load across all nodes.((("replica shards", "balancing load with")))((("load balancing with replica shards"))) If we
added just one extra node instead of two, we would end up with two nodes having one shard each, and one node doing double the work with two shards.

We can even things out by adjusting the number of replicas.  By allocating two
replicas instead of one, we end up with a total of six shards, which can be
evenly divided between three nodes, as shown in <<img-three-nodes>>:

[source,json]
-----------------------
POST /my_index/_settings
{
  "number_of_replicas": 2
}
-----------------------

As a bonus, we have also increased our availability.  We can now afford to
lose two nodes and still have a copy of all our data.

[[img-three-nodes]]
.Adjust the number of replicas to balance the load between nodes
image::images/elas_4404.png["Adjust the number of replicas to balance the load between nodes"]

NOTE: The fact that node 3 holds two replicas and no primaries is not
important.  Replicas and primaries do the same amount of work; they just play
slightly different roles.  There is no need to ensure that primaries are
distributed evenly across all nodes.
