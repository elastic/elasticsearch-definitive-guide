[[shard-scale]]
=== The Unit of Scale

In <<dynamic-indices>>, we explained that a shard is a _Lucene index_ and that
an Elasticsearch index is a collection of shards.((("scaling", "shard as unit of scale"))) Your application talks to an
index, and Elasticsearch routes your requests to the appropriate shards.

A shard is the _unit of scale_. ((("shards", "as unit of scale"))) The smallest index you can have is one with a
single shard. This may be more than sufficient for your needs--a single
shard can hold a lot of data--but it limits your ability to scale.

Imagine that our cluster consists of one node, and in our cluster we have one
index, which has only one shard:

[source,json]
----------------------------
PUT /my_index
{
  "settings": {
    "number_of_shards":   1, <1>
    "number_of_replicas": 0
  }
}
----------------------------
<1> Create an index with one primary shard and zero replica shards.

This setup may be small, but it serves our current needs and is cheap to run.

[NOTE]
==================================================

At the moment we are talking about only _primary_ shards.((("primary shards")))  We discuss
_replica_ shards in <<replica-shards>>.

==================================================

One glorious day, the Internet discovers us, and a single node just can't keep up with
the traffic.  We decide to add a second node, as per <<img-one-shard>>. What happens?

[[img-one-shard]]
.An index with one shard has no scale factor
image::images/elas_4401.png["An index with one shard has no scale factor"]

The answer is: nothing.  Because we have only one shard, there is nothing to
put on the second node. We can't increase the number of shards in the index,
because the number of shards is an important element in the algorithm used to
<<routing-value,route documents to shards>>:

    shard = hash(routing) % number_of_primary_shards

Our only option now is to reindex our data into a new, bigger index that has
more shards, but that will take time that we can ill afford.  By planning
ahead, we could have avoided this problem completely by _overallocating_.




