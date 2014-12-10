
Elasticsearch is often deployed as a cluster of nodes.((("clusters", "administration")))  A variety of
APIs let you manage and monitor the cluster itself, rather than interact
with the data stored within the cluster.

As with most functionality in Elasticsearch, there is an overarching design goal
that tasks should be performed through an API rather than by modifying static
configuration files.  This becomes especially important as your cluster scales.
Even with a provisioning system (such as Puppet, Chef, and Ansible), a single HTTP API call
is often simpler than pushing new configurations to hundreds of physical machines.

To that end, this chapter presents the various APIs that allow you to
dynamically tweak, tune, and configure your cluster.  It also covers a
host of APIs that provide statistics about the cluster itself so you can
monitor for health and performance.
