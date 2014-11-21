=== Index-Time Optimizations

All of the solutions we've talked about so far are implemented at
_query time_. ((("index time optimizations")))((("partial matching", "index time optimizations")))They don't require any special mappings or indexing patterns;
they simply work with the data that you've already indexed.

The flexibility of query-time operations comes at a cost: search performance.
Sometimes it may make sense to move the cost away from the query.  In a real-
time web application, an additional 100ms may be too much latency to tolerate.

By preparing your data at index time, you can make your searches more flexible
and improve performance. You still pay a price: increased index size and
slightly slower indexing throughput, but it is a price you pay once at index
time, instead of paying it on every query.

Your users will thank you.
