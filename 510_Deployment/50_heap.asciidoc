[[heap-sizing]]
=== Heap: Sizing and Swapping

The default installation of Elasticsearch is configured with a 1 GB heap. ((("deployment", "heap, sizing and swapping")))((("heap", "sizing and setting"))) For
just about every deployment, this number is far too small.  If you are using the
default heap values, your cluster is probably configured incorrectly.

There are two ways to change the heap size in Elasticsearch.  The easiest is to
set an environment variable called `ES_HEAP_SIZE`.((("ES_HEAP_SIZE environment variable")))  When the server process
starts, it will read this environment variable and set the heap accordingly.
As an example, you can set it via the command line as follows:

[source,bash]
----
export ES_HEAP_SIZE=10g
----

Alternatively, you can pass in the heap size via a command-line argument when starting
the process, if that is easier for your setup:

[source,bash]
----
./bin/elasticsearch -Xmx10g -Xms10g <1>
----
<1> Ensure that the min (`Xms`) and max (`Xmx`) sizes are the same to prevent
the heap from resizing at runtime, a very costly process.

Generally, setting the `ES_HEAP_SIZE` environment variable is preferred over setting
explicit `-Xmx` and `-Xms` values.

==== Give Half Your Memory to Lucene

A common problem is configuring a heap that is _too_ large. ((("heap", "sizing and setting", "giving half your memory to Lucene"))) You have a 64 GB
machine--and by golly, you want to give Elasticsearch all 64 GB of memory.  More
is better!

Heap is definitely important to Elasticsearch.  It is used by many in-memory data
structures to provide fast operation.  But with that said, there is another major
user of memory that is _off heap_: Lucene.

Lucene is designed to leverage the underlying OS for caching in-memory data structures.((("Lucene", "memory for")))
Lucene segments are stored in individual files.  Because segments are immutable,
these files never change.  This makes them very cache friendly, and the underlying
OS will happily keep hot segments resident in memory for faster access.

Lucene's performance relies on this interaction with the OS.  But if you give all
available memory to Elasticsearch's heap, there won't be any left over for Lucene.
This can seriously impact the performance of full-text search.

The standard recommendation is to give 50% of the available memory to Elasticsearch
heap, while leaving the other 50% free.  It won't go unused; Lucene will happily
gobble up whatever is left over.

[[compressed_oops]]
==== Don't Cross 32 GB!
There is another reason to not allocate enormous heaps to Elasticsearch. As it turns((("heap", "sizing and setting", "32gb heap boundary")))((("32gb Heap boundary")))
out, the JVM uses a trick to compress object pointers when heaps are less than
~32 GB.

In Java, all objects are allocated on the heap and referenced by a pointer.
Ordinary object pointers (OOP) point at these objects, and are traditionally
the size of the CPU's native _word_: either 32 bits or 64 bits, depending on the
processor.  The pointer references the exact byte location of the value.

For 32-bit systems, this means the maximum heap size is 4 GB.  For 64-bit systems,
the heap size can get much larger, but the overhead of 64-bit pointers means there
is more wasted space simply because the pointer is larger.  And worse than wasted
space, the larger pointers eat up more bandwidth when moving values between
main memory and various caches (LLC, L1, and so forth).

Java uses a trick called https://wikis.oracle.com/display/HotSpotInternals/CompressedOops[compressed oops]((("compressed object pointers")))
to get around this problem.  Instead of pointing at exact byte locations in
memory, the pointers reference _object offsets_.((("object offsets")))  This means a 32-bit pointer can
reference four billion _objects_, rather than four billion bytes.  Ultimately, this
means the heap can grow to around 32 GB of physical size while still using a 32-bit
pointer.

Once you cross that magical ~30&#x2013;32 GB boundary, the pointers switch back to
ordinary object pointers.  The size of each pointer grows, more CPU-memory
bandwidth is used, and you effectively lose memory.  In fact, it takes until around
40&#x2013;50 GB of allocated heap before you have the same _effective_ memory of a 32 GB
heap using compressed oops.

The moral of the story is this: even when you have memory to spare, try to avoid
crossing the 32 GB heap boundary.  It wastes memory, reduces CPU performance, and
makes the GC struggle with large heaps.

[role="pagebreak-before"]
.I Have a Machine with 1 TB RAM!
****
The 32 GB line is fairly important.  So what do you do when your machine has a lot
of memory?  It is becoming increasingly common to see super-servers with 300&#x2013;500 GB
of RAM.

First, we would recommend avoiding such large machines (see <<hardware>>).

But if you already have the machines, you have two practical options:

- Are you doing mostly full-text search?  Consider giving 32 GB to Elasticsearch
and letting Lucene use the rest of memory via the OS filesystem cache.  All that
memory will cache segments and lead to blisteringly fast full-text search.

- Are you doing a lot of sorting/aggregations?  You'll likely want that memory
in the heap then.  Instead of one node with 32 GB+ of RAM, consider running two or
more nodes on a single machine.  Still adhere to the 50% rule, though.  So if your
machine has 128 GB of RAM, run two nodes, each with 32 GB.  This means 64 GB will be
used for heaps, and 64 will be left over for Lucene.
+
If you choose this option, set `cluster.routing.allocation.same_shard.host: true`
in your config.  This will prevent a primary and a replica shard from colocating
to the same physical machine (since this would remove the benefits of replica high availability).
****

==== Swapping Is the Death of Performance

It should be obvious,((("heap", "sizing and setting", "swapping, death of performance")))((("memory", "swapping as the death of performance")))((("swapping, the death of performance"))) but it bears spelling out clearly: swapping main memory
to disk will _crush_ server performance.  Think about it: an in-memory operation
is one that needs to execute quickly.

If memory swaps to disk, a 100-microsecond operation becomes one that take 10
milliseconds.  Now repeat that increase in latency for all other 10us operations.
It isn't difficult to see why swapping is terrible for performance.

The best thing to do is disable swap completely on your system.  This can be done
temporarily:

[source,bash]
----
sudo swapoff -a
----

To disable it permanently, you'll likely need to edit your `/etc/fstab`.  Consult
the documentation for your OS.

If disabling swap completely is not an option, you can try to lower `swappiness`.
This value controls how aggressively the OS tries to swap memory.
This prevents swapping under normal circumstances, but still allows the OS to swap
under emergency memory situations.

For most Linux systems, this is configured using the `sysctl` value:

[source,bash]
----
vm.swappiness = 1 <1>
----
<1> A `swappiness` of `1` is better than `0`, since on some kernel versions a `swappiness`
of `0` can invoke the OOM-killer.

Finally, if neither approach is possible, you should enable `mlockall`.
 file.  This allows the JVM to lock its memory and prevent
it from being swapped by the OS.  In your `elasticsearch.yml`, set this:

[source,yaml]
----
bootstrap.mlockall: true
----
