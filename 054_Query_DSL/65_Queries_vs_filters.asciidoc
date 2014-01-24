=== Queries and Filters

Although we refer to the Query DSL, in reality there are two DSLs: the
Query DSL and the Filter DSL. Query clauses and filter clauses are similar
in nature, but have slightly different purposes.

A _filter_ asks a `yes|no` question of every document and is used
for fields that contain exact values:

* is the `created` date in the range `2013` .. `2014`?

* does the `status` field contain the term `"published"`?

* is the `lat_lon` field within `10km` of a specified point?

A _query_ is similar to a filter, but also asks the question:
_How *well* does this document match?_

Typical uses for a query would be to find documents:

* that best match the words: `full text search`

* that contain the word `run`, but may also match `runs`, `running`,
  `jog` or `sprint`

* containing the words `quick`, `brown` and `fox` --- the closer together they
  are, the more relevant the document

* tagged with `lucene`,  `search` or `java` -- the more tags, the more
  relevant the document

A query calculates how _relevant_ each document is to the
query, and assigns it a relevance `_score`, which is later used to
sort matching documents by relevance. This concept of relevance is
well suited to full text search where there is seldom a completely
``correct'' answer.

==== Performance differences

The output from most filter clauses -- a simple list of the documents that match
the filter -- is quick to calculate and easy to cache in memory, using
only one bit per document. These cached filters can be reused
very efficiently for subsequent requests.

Queries not only have to find matching documents, but also to calculate how
relevant each document is, which typically makes queries heavier than filters.
Also, query results are not cachable.

Thanks to the inverted index, a simple query which matches just a few documents
may perform as well or better than a cached filter which spans millions
of documents.  In general, however, a cached filter will outperform a
query, and will do so consistently.

The goal of filters is to *reduce the number of documents that have to
be examined by the query*.

==== When to use which

As a general rule, use query clauses for *full text* search or
for any condition that should affect the *relevance score*, and
use filter clauses for everything else.

