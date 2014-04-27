=== Add an index

To add data to Elasticsearch, we need an _index_ -- a place to store related
data.  In reality, an index is just a ``logical namespace'' which points to
one or more physical _shards_.

A _shard_ is a low-level ``worker unit''. Each shard is a single instance of
Lucene, and is a complete search engine in its own right. Our documents are
stored and indexed in shards, but our applications don't talk to them directly.
Instead, they talk to an index.

Shards are how Elasticsearch distributes data around your cluster. Think of
shards as containers for data. Documents are stored in shards, and shards are
allocated to nodes in your cluster. As your cluster grows or shrinks,
Elasticsearch will automatically migrate shards between nodes so that the
cluster remains balanced.

A shard can be either a _primary_ shard or a _replica_ shard. Each document in
your index belongs to a single primary shard, so the number of primary shards
that you have determines the maximum amount of data that your index can hold.

****

While there is no theoretical limit to the amount of data that a primary shard
can hold, there is a practical limit.  What constitutes the maximum shard size
depends entirely on your use case: the hardware you have, the size and
complexity of your documents, how you index and query your documents, and your
expected response times.

****

A replica shard is just a copy of a primary shard. Replicas are used to provide
redundant copies of your data to protect against hardware failure, and to
serve read requests like searching or retrieving a document.

The number of primary shards in an index is fixed at the time that an index is
created, but the number of replica shards can be changed at any time.

Let's create an index called `blogs` in our empty one-node cluster. By
default, indices are assigned 5 primary shards, but for the purpose of this
demonstration, we'll assign just 3 primary shards and 1 replica (one replica
of every primary shard):

[source,js]
--------------------------------------------------
PUT /blogs
{
   "settings" : {
      "number_of_shards" : 3,
      "number_of_replicas" : 1
   }
}
--------------------------------------------------
// SENSE: 020_Distributed_Cluster/15_Add_index.json

[[cluster-one-node]]
.A single-node cluster with an index
image::images/02-02_one_node.png["A single-node cluster with an index"]

Our cluster now looks like <<cluster-one-node>> -- all 3 primary shards have
been allocated to `Node 1`. If we were to check the
<<cluster-health,`cluster-health`>> now, we would see this:

[source,js]
--------------------------------------------------
{
   "cluster_name":          "elasticsearch",
   "status":                "yellow", <1>
   "timed_out":             false,
   "number_of_nodes":       1,
   "number_of_data_nodes":  1,
   "active_primary_shards": 3,
   "active_shards":         3,
   "relocating_shards":     0,
   "initializing_shards":   0,
   "unassigned_shards":     3 <2>
}
--------------------------------------------------

<1> Cluster `status` is `yellow`.
<2> Our three replica shards have not been allocated to a node.

A cluster health of `yellow` means that all *primary* shards are up and
running -- the cluster is capable of serving any request successfully -- but
not  all *replica* shards are active.  In fact all three of our replica shards
are currently `unassigned` -- they haven't been allocated to a node. It
doesn't make sense to store copies of the same data on the same node. If we
were to lose that node, we would lose all copies of our data.

Currently our cluster is fully functional but at risk of data loss in case of
hardware failure.

