[[bulk-format]]
==== Why the funny format?

When we learned about Bulk requests earlier in <<bulk>>, you may have asked
yourself: ``Why does the `bulk` API require the funny format with the newline
characters, instead of just sending the requests wrapped in a JSON array, like
the `mget` API?''

To answer this, we need to explain a little background:

Each document referenced in a bulk request may belong to a different primary
shard, each of which may be allocated to any of the nodes in the cluster. This
means that every _action_ inside a `bulk` request needs to be forwarded to the
correct shard on the correct node.

If the individual requests were wrapped up in a JSON array, that would mean
that we would need to:

 * parse the JSON into an array (including the document data, which
   can be very large)
 * look at each request to determine which shard it should go to
 * create an array of requests for each shard
 * serialize these arrays into the internal transport format
 * send the requests to each shard

It would work, but would need a lot of RAM to hold copies of essentially
the same data, and would create many more data structures that the JVM
would have to spend time garbage collecting.

Instead, Elasticsearch reaches up into the networking buffer, where the raw
request has been received and reads the data directly. It uses the newline
characters to identify and parse just the small _action/metadata_ lines in
order to decide which shard should handle each request.

These raw requests are forwarded directly to the correct shard. There
is no redundant copying of data, no wasted data structures. The entire
request process is handled in the smallest amount of memory possible.

