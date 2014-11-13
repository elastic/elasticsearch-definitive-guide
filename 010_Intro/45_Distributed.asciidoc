=== Distributed Nature

At the beginning of this chapter, we said that Elasticsearch((("distributed nature of Elasticsearch"))) can scale out to
hundreds (or even thousands) of servers and handle petabytes of data. While
our tutorial gave examples of how to use Elasticsearch, it didn't touch on the
mechanics at all. Elasticsearch is distributed by nature, and it is designed
to hide the complexity that comes with being distributed.

The distributed aspect of Elasticsearch is largely transparent.  Nothing in
the tutorial required you to know about distributed systems, sharding, cluster
discovery, or dozens of other distributed concepts.  It happily ran the
tutorial on a single node living inside your laptop, but if you were to run
the tutorial on a cluster containing 100 nodes, everything would work in
exactly the same way.

Elasticsearch tries hard to hide the complexity of distributed systems. Here are some of
the operations happening automatically under the hood:

 * Partitioning your documents into different containers((("documents", "partitioning into shards")))((("shards"))) or _shards_, which
   can be stored on a single node or on  multiple nodes

 * Balancing these shards across the nodes in your cluster to spread the
   indexing and search load

 * Duplicating each shard to provide redundant copies of your data, to
   prevent data loss in case of hardware failure

 * Routing requests from any node in the cluster to the nodes that hold the
   data you're interested in

 * Seamlessly integrating new nodes as your cluster grows or redistributing
   shards to recover from node loss

As you read through this book, you'll encounter supplemental chapters about the
distributed nature of Elasticsearch.  These chapters will teach you about
how the cluster scales and deals with failover (<<distributed-cluster>>),
handles document storage (<<distributed-docs>>), executes distributed search
(<<distributed-search>>), and what a shard is and how it works
(<<inside-a-shard>>).

These chapters are not required reading--you can use Elasticsearch without
understanding these internals--but they will provide insight that will make
your knowledge of Elasticsearch more complete. Feel free to skim them and
revisit at a later point when you need a more complete understanding.

