[[near-real-time]]
=== Near Real-Time Search

With the development of per-segment search, the ((("searching", "near real-time search")))delay between indexing a
document and making it visible to search dropped dramatically.  New documents
could be made searchable within minutes, but that still isn't fast enough.

The bottleneck is the disk. ((("committing segments to disk")))((("fsync")))((("segments", "committing to disk"))) Commiting a new segment to disk requires an
http://en.wikipedia.org/wiki/Fsync[`fsync`] to ensure that the segment is
physically written to disk and that data will not be lost if there is a power
failure. But an `fsync` is costly; it cannot be performed every time a
document is indexed without a big performance hit.

What was needed was a more lightweight way to make new documents visible to
search, which meant removing `fsync` from the equation.

Sitting between Elasticsearch and the disk is the filesystem cache.((("filesystem cache")))  As before, documents in the in-memory indexing buffer (<<img-pre-refresh>>) are written to a new segment (<<img-post-refresh>>). But the new
segment is written to the filesystem cache first--which is cheap--and
only later is it flushed to disk--which is expensive.  But once a file is in
the cache, it can be opened and read, just like any other file.

[[img-pre-refresh]]
.A Lucene index with new documents in the in-memory buffer
image::images/elas_1104.png["A Lucene index with new documents in the in-memory buffer"]

Lucene allows new segments to be written and opened--making the documents
they contain visible to search--without performing a full commit. This is a
much lighter process than a commit, and can be done frequently without ruining
performance.

[[img-post-refresh]]
.The buffer contents have been written to a segment, which is searchable, but is not yet commited
image::images/elas_1105.png["The buffer contents have been written to a segment, which is searchable, but is not yet commited"]


[[refresh-api]]
==== refresh API

In Elasticsearch, this lightweight process of writing and opening a new
segment is called a _refresh_.((("shards", "refreshes")))((("refresh API"))) By default, every shard is refreshed
automatically once every second. This is why we say that Elasticsearch has
_near_ real-time search: document changes are not visible to search
immediately, but will become visible within 1 second.

This can be confusing for new users: they index a document and try to search
for it, and it just isn't there.  The way around this is to perform a manual
refresh, with the `refresh` API:

[source,json]
-----------------------------
POST /_refresh <1>
POST /blogs/_refresh <2>
-----------------------------
<1> Refresh all indices.
<2> Refresh just the `blogs` index.

[TIP]
====
While a refresh is much lighter than a commit, it still has a performance
cost.((("indices", "refresh_interval")))  A manual refresh can be useful when writing tests, but don't do a
manual refresh every time you index a document in production; it will hurt
your performance.  Instead, your application needs to be aware of the near
real-time nature of Elasticsearch and make allowances for it.
====

Not all use cases require a refresh every second.  Perhaps you are using
Elasticsearch to index millions of log files, and you would prefer to optimize
for index speed rather than near real-time search.  You can reduce the
frequency of refreshes on a per-index basis by ((("refresh_interval setting")))setting the `refresh_interval`:

[source,json]
-----------------------------
PUT /my_logs
{
  "settings": {
    "refresh_interval": "30s" <1>
  }
}
-----------------------------
<1> Refresh the `my_logs` index every 30 seconds.

The `refresh_interval` can be updated dynamically on an existing index.  You
can turn off automatic refreshes while you are building a big new index, and then turn them back on when you start using the index in production:

[source,json]
-----------------------------
POST /my_logs/_settings
{ "refresh_interval": -1 } <1>

POST /my_logs/_settings
{ "refresh_interval": "1s" } <2>
-----------------------------
<1> Disable automatic refreshes.
<2> Refresh automatically every second.

CAUTION: The `refresh_interval` expects a _duration_ such as `1s` (1
second) or `2m` (2 minutes).  An absolute number like `1` means
_1 millisecond_--a sure way to bring your cluster to its knees.


