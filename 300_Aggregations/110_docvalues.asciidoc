[[doc-values]]
=== Doc Values

In-memory fielddata is limited by the size of your heap.((("aggregations", "doc values"))) While this is a
problem that can be solved by scaling horizontally--you can always add more
nodes--you will find that heavy use of aggregations and sorting can exhaust
your heap space while other resources on the node are underutilized.

While fielddata defaults to loading values into memory on the fly, this is not
the only option. It can also be written to disk at index time in a way that
provides all the functionality of in-memory fielddata, but without the
heap memory usage. This alternative format is ((("fielddata", "doc values")))((("doc values")))called _doc values_.

Doc values were added to Elasticsearch in version 1.0.0 but, until recently,
they were much slower than in-memory fielddata.  By benchmarking and profiling
performance, various bottlenecks have been identified--in both Elasticsearch
and Lucene--and removed.

Doc values are now only about 10&#x2013;25% slower than in-memory fielddata, and
come with two major advantages:

 *  They live on disk instead of in heap memory.  This allows you to work with
    quantities of fielddata that would normally be too large to fit into
    memory.  In fact, your heap space (`$ES_HEAP_SIZE`) can now be set to a
    smaller size,  which improves the speed of garbage collection and,
    consequently, node stability.

 *  Doc values are built at index time, not at search time. While in-memory
    fielddata has to be built on the fly at search time by uninverting the
    inverted index, doc values are prebuilt and much faster to initialize.

The trade-off is a larger index size and slightly slower fielddata access. Doc
values are remarkably efficient, so for many queries you might not even notice
the slightly slower speed.  Combine that with faster garbage collections and
improved initialization times and you may notice a net gain.

The more filesystem cache space that you have available, the better doc values
will perform.  If the files holding the doc values are resident in the filesystem cache, then accessing the files is almost equivalent to reading from
RAM.  And the filesystem cache is managed by the kernel instead of the JVM.

==== Enabling Doc Values

Doc values can be enabled for numeric, date, Boolean, binary, and geo-point
fields, and for `not_analyzed` string fields.((("doc values", "enabling"))) They do not currently work with
`analyzed` string fields.  Doc values are enabled per field in the field
mapping, which means that you can combine in-memory fielddata with doc values:

[source,js]
----
PUT /music/_mapping/song
{
  "properties" : {
    "tag": {
      "type":       "string",
      "index" :     "not_analyzed",
      "doc_values": true <1>
    }
  }
}
----
<1> Setting `doc_values` to `true` at field creation time is all
    that is required to use disk-based fielddata instead of in-memory
    fielddata.

That's it!  Queries, aggregations, sorting, and scripts will function as
normal; they'll just be using doc values now.  There is no other
configuration necessary.

[TIP]
==================================================

Use doc values freely.  The more you use them, the less stress you place on
the heap.  It is possible that doc values will become the default format in
the near future.

==================================================




