
== Approximate Aggregations

Life is easy if all your data fits on a single machine.((("aggregations", "approximate")))  Classic algorithms
taught in CS201 will be sufficient for all your needs.  But if all your data fits
on a single machine, there would be no need for distributed software
like Elasticsearch at all.  But once you start distributing data, algorithm
selection needs to be made carefully.

Some algorithms are amenable to distributed execution.  All of the aggregations
discussed thus far execute in a single pass and give exact results. These types 
of algorithms are often referred to as _embarrassingly parallel_, 
because they parallelize to multiple machines with little effort.  When 
performing a `max` metric, for example, the underlying algorithm is very simple:

1. Broadcast the request to all shards.
2. Look at the +price+ field for each document.  If `price > current_max`, replace
`current_max` with `price`.
3. Return the maximum price from all shards to the coordinating node.
4. Find the maximum price returned from all shards.  This is the true maximum.

The algorithm scales linearly with machines because the algorithm requires no
coordination (the machines don't need to discuss intermediate results), and the 
memory footprint is very small (a single integer representing the maximum).

Not all algorithms are as simple as taking the maximum value, unfortunately.
More complex operations require algorithms that make conscious trade-offs in
performance and memory utilization. There is a triangle of factors at play: 
big data, exactness, and real-time latency.

You get to choose two from this triangle:

Exact + real time:: Your data fits in the RAM of a single machine.  The world
is your oyster; use any algorithm you want. Results will be 100% accurate and
relatively fast.

Big data + exact::  A classic Hadoop installation.  Can handle petabytes of data
and give you exact answers--but it may take a week to give you that answer.

Big data + real time:: Approximate algorithms that give you accurate, but not
exact, results.

Elasticsearch currently supports two approximate algorithms (`cardinality` and 
`percentiles`). ((("approximate algorithms")))((("cardinality")))((("percentiles"))) These will give you accurate results, but not 100% exact.
In exchange for a little bit of estimation error, these algorithms give you
fast execution and a small memory footprint.

For _most_ domains, highly accurate results that return _in real time_ across
_all your data_ is more important than 100% exactness. At first blush, this may be an alien concept to you. _"We need exact answers!"_ 
you may yell.  But consider the implications of a 0.5% error:

- The true 99th percentile of latency for your website is 132ms.
- An approximation with 0.5% error will be within +/- 0.66ms of 132ms.
- The approximation returns in milliseconds, while the "true" answer may take seconds, or
be impossible.

For simply checking on your website's latency, do you care if the approximate 
answer is 132.66ms instead of 132ms?  Certainly, not all domains can tolerate
approximations--but the vast majority will have no problem.  Accepting
an approximate answer is more often a _cultural_ hurdle rather than a business
or technical imperative.



