[[making-text-searchable]]
=== Making Text Searchable

The first challenge that had to be solved was how to((("text", "making it searchable"))) make text searchable.
Traditional databases store a single value per field, but this is insufficient
for full-text search.  Every word in a text field needs to be searchable,
which means that the database needs to be able to index multiple values--words, in this case--in a single field.

The data structure that best supports the _multiple-values-per-field_
requirement is the _inverted index_, which((("inverted index"))) we introduced in
<<inverted-index>>. The inverted index contains a sorted list of all of the
unique values, or _terms_, that occur in any document and, for each term, a list
of all the documents that contain it.

     Term  | Doc 1 | Doc 2 | Doc 3 | ...
     ------------------------------------
     brown |   X   |       |  X    | ...
     fox   |   X   |   X   |  X    | ...
     quick |   X   |   X   |       | ...
     the   |   X   |       |  X    | ...


[NOTE]
====
When discussing inverted indices, we talk about indexing _documents_ because,
historically, an inverted index was used to index whole unstructured text
documents.  A _document_ in Elasticsearch is a structured JSON document with
fields and values.  In reality, every indexed field in a JSON document has its
own inverted index.
====

The inverted index may hold a lot more information than the list
of documents that contain a particular term. It may store a count of the number of
documents that contain each term, the number of times a term appears in a particular
document, the order of terms in each document, the length of each document,
the average length of all documents, and more.  These statistics allow
Elasticsearch to determine which terms are more important than others, and
which documents are more important than others, as described in
<<relevance-intro>>.

The important thing to realize is that the inverted index needs to know about
_all_ documents in the collection in order for it to function as intended.

In the early days of full-text search, one big inverted index was built for
the entire document collection and written to disk.  As soon as the new index
was ready, it replaced the old index, and recent changes became searchable.

[role="pagebreak-before"]
==== Immutability

The inverted index that is written to disk is _immutable_: it doesn't
change.((("inverted index", "immutability"))) Ever.  This immutability has important benefits:

* There is no need for locking. If you never have to update the index, you
  never have to worry about multiple processes trying to make changes at
  the same time.

* Once the index has been read into the kernel's filesystem cache, it stays
  there, because it never changes.  As long as there is enough space in the
  filesystem cache, most reads will come from memory instead of having to
  hit disk.  This provides a big performance boost.

* Any other caches (like the filter cache) remain valid for the life of the
  index. They don't need to be rebuilt every time the data changes,
  because the data doesn't change.

* Writing a single large inverted index allows the data to be compressed,
  reducing costly disk I/O and the amount of RAM needed to cache the index.

Of course, an immutable index has its downsides too, primarily the fact that
it is immutable! You can't change it.  If you want to make new documents
searchable, you have to rebuild the entire index. This places a significant limitation either on the amount of data that an index can contain, or the frequency with which the index can be updated.


