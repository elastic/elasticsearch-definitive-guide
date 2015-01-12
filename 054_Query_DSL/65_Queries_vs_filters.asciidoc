=== Queries and Filters

Although we refer to the query DSL, in reality there are two DSLs: the
query DSL and the filter DSL.((("DSL (Domain Specific Language)", "Query and Filter DSL")))((("Filter DSL"))) Query clauses and filter clauses are similar
in nature, but have slightly different purposes.

A _filter_ asks a yes|no question of((("filters", "queries versus")))((("exact values", "filters with yes|no questions for fields containing"))) every document and is used
for fields that contain exact values:

* Is the `created` date in the range `2013` - `2014`?

* Does the `status` field contain the term `published`?

* Is the `lat_lon` field within `10km` of a specified point?

A _query_ is similar to a filter, but also asks((("queries", "filters versus"))) the question:
How _well_ does this document match?

A typical use for a query is to find documents

* Best matching the words `full text search`

* Containing the word `run`, but maybe also matching `runs`, `running`,
  `jog`, or `sprint`

* Containing the words `quick`, `brown`, and `fox`&#x2014;the closer together they
  are, the more relevant the document

* Tagged with `lucene`,  `search`, or `java`&#x2014;the more tags, the more
  relevant the document

A query calculates how _relevant_ each document((("relevance", "calculation by queries"))) is to the
query, and assigns it a relevance `_score`, which is later used to
sort matching documents by relevance. This concept of relevance is
well suited to full-text search, where there is seldom a completely
``correct'' answer.

==== Performance Differences

The output from most filter clauses--a simple((("filters", "performance, queries versus"))) list of the documents that match
the filter--is quick to calculate and easy to cache in memory, using
only 1 bit per document. These cached filters can be reused
efficiently for subsequent requests.

Queries have to not only find((("queries", "performance, filters versus"))) matching documents, but also calculate how
relevant each document is, which typically makes queries heavier than filters.
Also, query results are not cachable.

Thanks to the inverted index, a simple query that matches just a few documents
may perform as well or better than a cached filter that spans millions
of documents.  In general, however, a cached filter will outperform a
query, and will do so consistently.

The goal of filters is to _reduce the number of documents that have to
be examined by the query_.

==== When to Use Which

As a general rule, use((("filters", "when to use")))((("queries", "when to use"))) query clauses for _full-text_ search or
for any condition that should affect the _relevance score_, and
use filter clauses for everything else.

