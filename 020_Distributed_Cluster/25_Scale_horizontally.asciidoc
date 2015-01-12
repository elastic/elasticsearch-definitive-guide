=== Scale Horizontally

What about scaling as the demand for our application grows?((("scaling", "horizontally")))((("clusters", "three-node cluster")))((("primary shards", "in three-node cluster"))) If we start a
third node, our cluster reorganizes itself to look like
<<cluster-three-nodes>>.

[[cluster-three-nodes]]
.A three-node cluster--shards have been reallocated to spread the load
image::images/elas_0204.png["A three-node cluster"]

One shard each from `Node 1` and `Node 2` have moved to the new
`Node 3`, and we have two shards per node, instead of three.
This means that the hardware resources (CPU, RAM, I/O) of each node
are being shared among fewer shards, allowing each shard to perform
better.

A shard is a fully fledged search engine in its own right, and is
capable of using all of the resources of a single node.  With our
total of six shards (three primaries and three replicas), our index is capable
of scaling out to a maximum of six nodes, with one shard on each node
and each shard having access to 100% of its node's resources.

