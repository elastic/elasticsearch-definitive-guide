[[dynamic-indices]]
=== Dynamically Updatable Indices

The next problem that needed to be ((("indices", "dynamically updatable")))solved was how to make an inverted index
updatable without losing the benefits of immutability?  The answer turned out
to be: use more than one index.

Instead of rewriting the whole inverted index, add new supplementary indices
to reflect more-recent changes. Each inverted index can be queried in turn--starting with the oldest--and the results combined.

Lucene, the Java libraries on which Elasticsearch is based, introduced  the
concept of _per-segment search_. ((("per-segment search")))((("segments")))((("indices", "in Lucene"))) A _segment_ is an inverted index in its own
right,  but now the word _index_ in Lucene came to mean a _collection of
segments_ plus a _commit point_&#x2014;a file((("commit point"))) that lists all known segments, as depicted in <<img-index-segments>>. New documents are first added to an in-memory indexing buffer, as shown in <<img-memory-buffer>>, before being written to an on-disk segment, as in <<img-post-commit>> 

[[img-index-segments]]
.A Lucene index with a commit point and three segments
image::images/elas_1101.png["A Lucene index with a commit point and three segments"]

.Index Versus Shard
***************************************

To add to the confusion, a _Lucene index_ is what we call a _shard_ in
Elasticsearch, while an _index_ in Elasticsearch((("indices", "in Elasticsearch")))((("shards", "indices versus"))) is a collection of shards.
When Elasticsearch searches an index, it sends the query out to a copy of
every shard (Lucene index) that belongs to the index, and then reduces the
per-shards results to a global result set, as described in
<<distributed-search>>.

***************************************


A per-segment search works as follows:

1. New documents are collected in an in-memory indexing buffer.
   See <<img-memory-buffer>>.
2. Every so often, the buffer is _commited_:

** A new segment--a supplementary inverted index--is written to disk.
** A new _commit point_ is written to disk, which includes the name of the new
   segment.
** The disk is _fsync'ed_&#x2014;all writes waiting in the filesystem cache are
   flushed to disk, to ensure that they have been physically written.

3. The new segment is opened, making the documents it contains visible to search.
4. The in-memory buffer is cleared, and is ready to accept new documents.

[[img-memory-buffer]]
.A Lucene index with new documents in the in-memory buffer, ready to commit
image::images/elas_1102.png["A Lucene index with new documents in the in-memory buffer, ready to commit"]

[[img-post-commit]]
.After a commit, a new segment is added to the commit point and the buffer is cleared
image::images/elas_1103.png["After a commit, a new segment is added to the index and the buffer is cleared"]

When a query is issued, all known segments are queried in turn. Term
statistics are aggregated across all segments to ensure that the relevance of
each term and each document is calculated accurately. In this way, new
documents can be added to the index relatively cheaply.

[[deletes-and-updates]]
==== Deletes and Updates

Segments are immutable, so documents cannot be removed from older segments,
nor can older segments be updated to reflect a newer version of a document.
Instead, every ((("deleted documents")))commit point includes a `.del` file that lists which documents
in which segments have been deleted.

When a document is ``deleted,'' it is actually just _marked_ as deleted in the
`.del` file. A document that has been marked as deleted can still match a
query, but it is removed from the results list before the final query results
are returned.

Document updates work in a similar way: when a document is updated, the old
version of the document is marked as deleted, and the new version of the
document is indexed in a new segment. Perhaps both versions of the document
will match a query, but the older deleted version is removed before the query
results are returned.

In <<merge-process>>, we show how deleted documents are purged from
the filesystem.





