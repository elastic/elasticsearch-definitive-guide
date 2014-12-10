[[capacity-planning]]
=== Capacity Planning

If 1 shard is too few and 1,000 shards are too many, how do I know how many
shards I need?((("shards", "determining number you need")))((("capacity planning")))((("scaling", "capacity planning"))) This is a question that is impossible to answer in the general case. There are
just too many variables:  the hardware that you use, the size and complexity
of your documents, how you index and analyze those documents, the types of
queries that you run, the aggregations that you perform, how you model your
data, and more.

Fortunately, it is an easy question to answer in the specific case--yours:

1.  Create a cluster consisting of a single server, with the hardware that you
    are considering using in production.

2.  Create an index with the same settings and analyzers that you plan to use
    in production, but with only one primary shard and no replicas.

3.  Fill it with real documents (or as close to real as you can get).

4.  Run real queries and aggregations (or as close to real as you can get).

Essentially, you want to replicate real-world usage and to push this single
shard until it ``breaks.''  Even the definition of _breaks_ depends on you:
some users require that all responses return within 50ms; others are quite
happy to wait for 5 seconds.

Once you define the capacity of a single shard, it is easy to extrapolate that
number to your whole index.  Take the total amount of data that you need to
index, plus some extra for future growth, and divide by the capacity of a
single shard.  The result is the number of primary shards that you will need.

[TIP]
================================

Capacity planning should not be your first step.

First look for ways to optimize how you are using Elasticsearch.  Perhaps you
have inefficient queries, not enough RAM, or you have left swap enabled?

We have seen new users who, frustrated by initial performance, immediately
start trying to tune the garbage collector or adjust the number of threads,
instead of tackling the simple problems like removing wildcard queries.

================================
