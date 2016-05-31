[[distributed-cluster]]
== Life Inside a Cluster

.Supplemental Chapter
****

As mentioned earlier, this is the first of several supplemental chapters
about how Elasticsearch operates in a distributed((("clusters"))) environment.  In this
chapter, we explain commonly used terminology like _cluster_, _node_, and
_shard_, the mechanics of how Elasticsearch scales out, and how it deals with
hardware failure.

Although this chapter is not required reading--you can use Elasticsearch for
a long time without worrying about shards, replication, and failover--it will
help you to understand the processes at work inside Elasticsearch. Feel free
to skim through the chapter and to refer to it again later.

****

Elasticsearch is built to be ((("scalability, Elasticsearch and")))always available, and to scale with your needs.
Scale can come from buying bigger ((("vertical scaling, Elasticsearch and")))servers (_vertical scale_, or _scaling up_)
or from buying more ((("horizontal scaling, Elasticsearch and")))servers (_horizontal scale_, or _scaling out_).

While Elasticsearch can benefit from more-powerful hardware, vertical scale
has its limits. Real scalability comes from horizontal scale--the ability to
add more nodes to the cluster and to spread load and reliability between them.

With most databases, scaling horizontally usually requires a major overhaul of
your application to take advantage of these extra boxes. In contrast,
Elasticsearch is _distributed_ by nature: it knows how to manage multiple
nodes to provide scale and high availability.  This also means that your
application doesn't need to care about it.

In this chapter, we show how you can set up your cluster,
nodes, and shards to scale with your needs and to ensure that your data is
safe from hardware failure.
