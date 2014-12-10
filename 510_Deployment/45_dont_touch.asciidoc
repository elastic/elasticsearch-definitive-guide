
=== Don't Touch These Settings!

There are a few hotspots in Elasticsearch that people just can't seem to avoid
tweaking. ((("deployment", "settings to leave unaltered"))) We understand:  knobs just beg to be turned. But of all the knobs to turn, these you should _really_ leave alone. They are
often abused and will contribute to terrible stability or terrible performance.
Or both.

==== Garbage Collector

As briefly introduced in <<garbage_collector_primer>>, the JVM uses a garbage
collector to free unused memory.((("garbage collector")))  This tip is really an extension of the last tip,
but deserves its own section for emphasis:

Do not change the default garbage collector!

The default GC for Elasticsearch is Concurrent-Mark and Sweep (CMS).((("Concurrent-Mark and Sweep (CMS) garbage collector")))  This GC
runs concurrently with the execution of the application so that it can minimize
pauses.  It does, however, have two stop-the-world phases.  It also has trouble
collecting large heaps.

Despite these downsides, it is currently the best GC for low-latency server software
like Elasticsearch.  The official recommendation is to use CMS.

There is a newer GC called the Garbage First GC (G1GC). ((("Garbage First GC (G1GC)"))) This newer GC is designed
to minimize pausing even more than CMS, and operate on large heaps.  It works
by dividing the heap into regions and predicting which regions contain the most
reclaimable space.  By collecting those regions first (_garbage first_), it can
minimize pauses and operate on very large heaps.

Sounds great!  Unfortunately, G1GC is still new, and fresh bugs are found routinely.
These bugs are usually of the segfault variety, and will cause hard crashes.
The Lucene test suite is brutal on GC algorithms, and it seems that G1GC hasn't
had the kinks worked out yet.

We would like to recommend G1GC someday, but for now, it is simply not stable
enough to meet the demands of Elasticsearch and Lucene.

==== Threadpools

Everyone _loves_ to tweak threadpools.((("threadpools")))  For whatever reason, it seems people
cannot resist increasing thread counts.  Indexing a lot?  More threads!  Searching
a lot? More threads!  Node idling 95% of the time?  More threads!

The default threadpool settings in Elasticsearch are very sensible.  For all
threadpools (except `search`) the threadcount is set to the number of CPU cores.
If you have eight cores, you can be running only eight threads simultaneously.  It makes
sense to assign only eight threads to any particular threadpool.

Search gets a larger threadpool, and is configured to `# cores * 3`. 

You might argue that some threads can block (such as on a disk I/O operation), 
which is why you need more threads.  This is not a problem in Elasticsearch:
much of the disk I/O is handled by threads managed by Lucene, not Elasticsearch.

Furthermore, threadpools cooperate by passing work between each other.  You don't
need to worry about a networking thread blocking because it is waiting on a disk
write.  The networking thread will have long since handed off that work unit to
another threadpool and gotten back to networking.

Finally, the compute capacity of your process is finite.  Having more threads just forces
the processor to switch thread contexts.  A processor can run only one thread
at a time, so when it needs to switch to a different thread, it stores the current
state (registers, and so forth) and loads another thread.  If you are lucky, the switch
will happen on the same core.  If you are unlucky, the switch may migrate to a
different core and require transport on an inter-core communication bus.

This context switching eats up cycles simply by doing administrative housekeeping; estimates can peg it as high as 30μs on modern CPUs.  So unless the thread
will be blocked for longer than 30μs, it is highly likely that that time would
have been better spent just processing and finishing early.

People routinely set threadpools to silly values.  On eight core machines, we have
run across configs with 60, 100, or even 1000 threads.  These settings will simply
thrash the CPU more than getting real work done.

So. Next time you want to tweak a threadpool, please don't.  And if you
_absolutely cannot resist_, please keep your core count in mind and perhaps set
the count to double.  More than that is just a waste.






