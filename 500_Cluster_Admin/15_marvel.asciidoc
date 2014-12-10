
=== Marvel for Monitoring

At the very beginning of the book (<<marvel>>), we encouraged you to install
Marvel,((("Marvel", "monitoring with")))((("clusters", "administration", "Marvel for monitoring"))) a management monitoring tool for Elasticsearch, because it would enable
interactive code samples throughout the book.

If you didn't install Marvel then, we encourage you to install it now.  This
chapter introduces a large number of APIs that emit an even larger number
of statistics.  These stats track everything from heap memory usage and garbage
collection counts to open file descriptors.  These statistics are invaluable
for debugging a misbehaving cluster.

The problem is that these APIs provide a single data point: the statistic
_right now_.  Often you'll want to see historical data too, so you can 
plot a trend.  Knowing memory usage at this instant is helpful, but knowing
memory usage _over time_ is much more useful.

Furthermore, the output of these APIs can get truly hairy as your cluster grows.
Once you have a dozen nodes, let alone a hundred, reading through stacks of JSON
becomes very tedious.

Marvel periodically polls these APIs and stores the data back in Elasticsearch.
This allows Marvel to query and aggregate the metrics, and then provide interactive
graphs in your browser.  There are no proprietary statistics that Marvel exposes;
it uses the same stats APIs that are accessible to you.  But it does greatly
simplify the collection and graphing of those statistics.

Marvel is free to use in development, so you should definitely try it out!
