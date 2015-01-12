[[fielddata]]
=== Fielddata

Aggregations work via a data structure known as _fielddata_ (briefly introduced
in <<fielddata-intro>>).  ((("fielddata")))((("memory usage", "fielddata")))Fielddata is often the largest consumer of memory
in an Elasticsearch cluster, so it is important to understand how it works.

[TIP]
==================================================

Fielddata can be loaded on the fly into memory, or built at index time and
stored on disk.((("fielddata", "loaded into memory vs. on disk")))  Later, we will talk about on-disk fielddata in
<<doc-values>>. For now we will focus on in-memory fielddata, as it is
currently the default mode of operation in Elasticsearch. This may well change
in a future version.

==================================================

Fielddata exists because inverted indices are efficient only for certain operations.
The inverted index excels((("inverted index", "fielddata versus"))) at finding documents that contain a term.  It does not
perform well in the opposite direction: determining which terms exist in a single
document. Aggregations need this secondary access pattern.

Consider the following inverted index:

    Term      Doc_1   Doc_2   Doc_3
    ------------------------------------
    brown   |   X   |   X   |
    dog     |   X   |       |   X
    dogs    |       |   X   |   X
    fox     |   X   |       |   X
    foxes   |       |   X   |
    in      |       |   X   |
    jumped  |   X   |       |   X
    lazy    |   X   |   X   |
    leap    |       |   X   |
    over    |   X   |   X   |   X
    quick   |   X   |   X   |   X
    summer  |       |   X   |
    the     |   X   |       |   X
    ------------------------------------

If we want to compile a complete list of terms in any document that mentions
+brown+, we might build a query like so:

[source,js]
----
GET /my_index/_search
{
  "query" : {
    "match" : {
      "body" : "brown"
    }
  },
  "aggs" : {
    "popular_terms": {
      "terms" : {
        "field" : "body"
      }
    }
  }
}
----

The query portion is easy and efficient.  The inverted index is sorted by
terms, so first we find +brown+ in the terms list, and then scan across all the
columns to see which documents contain +brown+.  We can very quickly see that
`Doc_1` and `Doc_2` contain the token +brown+.

Then, for the aggregation portion, we need to find all the unique terms in
`Doc_1`  and `Doc_2`.((("aggregations", "fielddata", "using instead of inverted index")))  Trying to do this with the inverted index would be a
very expensive process: we would have to iterate over every term in the index
and collect tokens from `Doc_1`  and `Doc_2` columns.  This would be slow
and scale poorly: as the number of terms and  documents grows, so would the
execution time.

Fielddata addresses this problem by inverting the relationship. While the
inverted index maps terms to the documents containing the term, fielddata
maps documents to the terms contained by the document:

    Doc      Terms
    -----------------------------------------------------------------
    Doc_1 | brown, dog, fox, jumped, lazy, over, quick, the
    Doc_2 | brown, dogs, foxes, in, lazy, leap, over, quick, summer
    Doc_3 | dog, dogs, fox, jumped, over, quick, the
    -----------------------------------------------------------------

Once the data has been uninverted, it is trivial to collect the unique tokens from
`Doc_1` and `Doc_2`.  Go to the rows for each document, collect all the terms, and
take the union of the two sets.


[TIP]
==================================================

The fielddata cache is per segment.((("fielddata cache")))((("segments", "fielddata cache"))) In other words, when a new segment becomes
visible to search, the fielddata cached from old segments remains valid. Only
the data for the new segment needs to be loaded into memory.

==================================================

Thus, search and aggregations are closely intertwined.  Search finds documents
by using the inverted index.  Aggregations collect and aggregate values from
fielddata, which is itself generated from the inverted index.

The rest of this chapter covers various functionality that either
decreases fielddata's memory footprint or increases execution speed.

[NOTE]
==================================================

Fielddata is not just used for aggregations.((("fielddata", "uses other than aggregations")))  It is required for any
operation that needs to look up the value contained in a specific document.
Besides aggregations, this includes sorting, scripts that access field
values, parent-child relationships (see <<parent-child>>), and certain types
of queries or filters, such as the <<geo-distance,`geo_distance`>> filter.

==================================================
