[[hardware]]
=== Hardware

If you've been following the normal development path, you've probably been playing((("deployment", "hardware")))((("hardware")))
with Elasticsearch on your laptop or on a small cluster of machines laying around.
But when it comes time to deploy Elasticsearch to production, there are a few
recommendations that you should consider.  Nothing is a hard-and-fast rule;
Elasticsearch is used for a wide range of tasks and on a bewildering array of
machines.  But these recommendations provide good starting points based on our experience with
production clusters.

==== Memory

If there is one resource that you will run out of first, it will likely be memory.((("hardware", "memory")))((("memory")))
Sorting and aggregations can both be memory hungry, so enough heap space to
accommodate these is important.((("heap")))  Even when the heap is comparatively small,
extra memory can be given to the OS filesystem cache.  Because many data structures
used by Lucene are disk-based formats, Elasticsearch leverages the OS cache to
great effect.

A machine with 64 GB of RAM is the ideal sweet spot, but 32 GB and 16 GB machines
are also common.  Less than 8 GB tends to be counterproductive (you end up
needing many, many small machines), and greater than 64 GB has problems that we will
discuss in <<heap-sizing>>.

==== CPUs

Most Elasticsearch deployments tend to be rather light on CPU requirements.  As
such,((("CPUs (central processing units)")))((("hardware", "CPUs"))) the exact processor setup matters less than the other resources.  You should
choose a modern processor with multiple cores.  Common clusters utilize two to eight
core machines.

If you need to choose between faster CPUs or more cores, choose more cores.  The
extra concurrency that multiple cores offers will far outweigh a slightly faster
clock speed.

==== Disks

Disks are important for all clusters,((("disks")))((("hardware", "disks"))) and doubly so for indexing-heavy clusters
(such as those that ingest log data).  Disks are the slowest subsystem in a server,
which means that write-heavy clusters can easily saturate their disks, which in
turn become the bottleneck of the cluster.

If you can afford SSDs, they are by far superior to any spinning media.  SSD-backed
nodes see boosts in both query and indexing performance.  If you can afford it,
SSDs are the way to go.

.Check Your I/O Scheduler
****
If you are using SSDs, make sure your OS I/O scheduler is((("I/O scheduler"))) configured correctly.
When you write data to disk, the I/O scheduler decides when that data is
_actually_ sent to the disk.  The default under most *nix distributions is a
scheduler called `cfq` (Completely Fair Queuing).

This scheduler allocates _time slices_ to each process, and then optimizes the
delivery of these various queues to the disk.  It is optimized for spinning media:
the nature of rotating platters means it is more efficient to write data to disk
based on physical layout.

This is inefficient for SSD, however, since there are no spinning platters
involved.  Instead, `deadline` or `noop` should be used instead.  The deadline
scheduler optimizes based on how long writes have been pending, while `noop`
is just a simple FIFO queue.

This simple change can have dramatic impacts.  We've seen a 500-fold improvement
to write throughput just by using the correct scheduler.
****

If you use spinning media, try to obtain the fastest disks possible (high-performance server disks, 15k RPM drives).

Using RAID 0 is an effective way to increase disk speed, for both spinning disks
and SSD.  There is no need to use mirroring or parity variants of RAID, since
high availability is built into Elasticsearch via replicas.

Finally, avoid network-attached storage (NAS).  People routinely claim their
NAS solution is faster and more reliable than local drives.  Despite these claims,
we have never seen NAS live up to its hype.  NAS is often slower, displays
larger latencies with a wider deviation in average latency, and is a single
point of failure.

==== Network

A fast and reliable network is obviously important to performance in a distributed((("hardware", "network")))((("network")))
system.  Low latency helps ensure that nodes can communicate easily, while
high bandwidth helps shard movement and recovery.  Modern data-center networking
(1 GbE, 10 GbE) is sufficient for the vast majority of clusters.

Avoid clusters that span multiple data centers, even if the data centers are
colocated in close proximity.  Definitely avoid clusters that span large geographic
distances.

Elasticsearch clusters assume that all nodes are equal--not that half the nodes
are actually 150ms distant in another data center. Larger latencies tend to
exacerbate problems in distributed systems and make debugging and resolution
more difficult.

Similar to the NAS argument, everyone claims that their pipe between data centers is
robust and low latency. This is true--until it isn't (a network failure will
happen eventually; you can count on it). From our experience, the hassle of
managing cross&#x2013;data center clusters is simply not worth the cost.

==== General Considerations

It is possible nowadays to obtain truly enormous machines:((("hardware", "general considerations")))  hundreds of gigabytes
of RAM with dozens of CPU cores.  Conversely, it is also possible to spin up
thousands of small virtual machines in cloud platforms such as EC2.  Which
approach is best?

In general, it is better to prefer medium-to-large boxes.  Avoid small machines,
because you don't want to manage a cluster with a thousand nodes, and the overhead
of simply running Elasticsearch is more apparent on such small boxes.

At the same time, avoid the truly enormous machines.  They often lead to imbalanced
resource usage (for example, all the memory is being used, but none of the CPU) and can
add logistical complexity if you have to run multiple nodes per machine.


