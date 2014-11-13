=== An Empty Cluster

If we start a single node, with no data and no ((("empty cluster")))((("clusters", "empty")))indices, our cluster looks like
<<img-cluster>>.

[[img-cluster]]
.A cluster with one empty node
image::images/elas_0201.png["A cluster with one empty node"]

A _node_ is a running instance of ((("nodes", "in clusters")))Elasticsearch, while a _cluster_ consists of
one or more nodes with the same `cluster.name` that are working together to
share their data and workload. As nodes are added to or removed from the
cluster, the cluster reorganizes itself to spread the data evenly.

One node in the cluster is elected to be the _master_ node, which((("master node"))) is in charge
of managing cluster-wide changes like creating or deleting an index, or adding
or removing a node from the cluster.  The master node does not need to be
involved in document-level changes or searches, which means that having just
one master node will not become a bottleneck as traffic grows. Any node can
become the master. Our example cluster has only one node, so it performs the
master role.

As users, we can talk to _any node in the cluster_, including the master node.
Every node knows where each document lives and can forward our request
directly to the nodes that hold the data we are interested in. Whichever node
we talk to manages the process of gathering the response from the node or
nodes holding the data and returning the final response to the client. It is
all managed transparently by Elasticsearch.

