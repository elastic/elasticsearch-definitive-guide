[[overallocation]]
=== Shard Overallocation

A shard lives on a single node,((("scaling", "shard overallocation")))((("shards", "overallocation of"))) but a node can hold multiple shards. Imagine
that we created our index with two primary shards instead of one:

[source,json]
----------------------------
PUT /my_index
{
  "settings": {
    "number_of_shards":   2, <1>
    "number_of_replicas": 0
  }
}
----------------------------
<1> Create an index with two primary shards and zero replica shards.

With a single node, both shards would be assigned to the same node. From the
point of view of our application, everything functions as it did before.  The
application communicates with the index, not the shards, and there is still
only one index.

This time, when we add a second node, Elasticsearch will automatically move
one shard from the first node to the second node, as depicted in <<img-two-shard>>. Once the relocation has
finished, each shard will have access to twice the computing power that it had
before.

[[img-two-shard]]
.An index with two shards can take advantage of a second node
image::images/elas_4402.png["An index with two shards can take advantage of a second node"]

We have been able to double our capacity by simply copying a shard across the
network to the new node. The best part is, we achieved this with zero
downtime.  All indexing and search requests continued to function normally
while the shard was being moved.

A new index in Elasticsearch is allotted five primary shards by default.  That
means that we can spread that index out over a maximum of five nodes, with one
shard on each node.  That's a lot of capacity, and it happens without you
having to think about it at all!

.Shard Splitting
****************************

Users often ask why Elasticsearch doesn't support _shard-splitting_&#x2014;the
ability to split each shard into two or more pieces. ((("shard splitting"))) The reason is that
shard-splitting is a bad idea:

* Splitting a shard is almost equivalent to reindexing your data. It's a much
  heavier process than just copying a shard from one node to another.

* Splitting is exponential. You start with one shard, then split into two, and then
  four, eight, sixteen, and so on. Splitting doesn't allow you to increase capacity
  by just 50%.

* Shard splitting requires you to have enough capacity to hold a second copy
  of your index. Usually, by the time you realize that you need to scale out,
  you don't have enough free space left to perform the split.

In a way, Elasticsearch does support shard splitting.  You can always reindex
your data to a new index with the appropriate number of shards (see
<<reindex>>).  It is still a more intensive process than moving shards around,
and still requires enough free space to complete, but at least you can control
the number of shards in the new index.

****************************

