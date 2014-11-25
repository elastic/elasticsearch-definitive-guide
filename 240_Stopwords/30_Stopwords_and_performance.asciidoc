[[stopwords-performance]]
=== Stopwords and Performance

The biggest disadvantage of keeping stopwords is that of performance. When
Elasticsearch performs a ((("stopwords", "performance and")))full-text search, it has to calculate the relevance
`_score` on all matching documents in order to return the top 10 matches.

While most words typically occur in much fewer than 0.1% of all documents, a
few words such as `the` may occur in almost all of them.  Imagine you have an
index of one million documents.  A query for `quick brown fox` may match  fewer
than 1,000 documents.  But a query for `the quick brown fox` has to score and
sort almost all of the one million documents in your index, just in order to
return the top 10!

The problem is that `the quick brown fox` is really a query for `the OR quick
OR brown OR fox`&#x2014;any document that contains nothing more than the almost
meaningless term `the` is included in the result set.  What we need is a way of
reducing the number of documents that need to be scored.

[[stopwords-and]]
==== and Operator

The easiest way to reduce the number of documents is simply to use the
<<match-improving-precision,`and` operator>> with the `match` query, in order
to make all ((("stopwords", "performance and", "using and operator")))((("and operator", "using with match query")))words required.

A `match` query like this:

[source,json]
---------------------------------
{
    "match": {
        "text": {
            "query":    "the quick brown fox",
            "operator": "and"
        }
    }
}
---------------------------------

is rewritten as a `bool` query like this:

[source,json]
---------------------------------
{
    "bool": {
        "must": [
            { "term": { "text": "the" }},
            { "term": { "text": "quick" }},
            { "term": { "text": "brown" }},
            { "term": { "text": "fox" }}
        ]
    }
}
---------------------------------

The `bool` query is intelligent enough to execute each `term` query in the
optimal order--it starts with the least frequent term.  Because all terms
are required, only documents that contain the least frequent term can possibly
match. Using the `and` operator greatly speeds up multiterm queries.

==== minimum_should_match

In <<match-precision>>, we discussed using the `minimum_should_match` operator
to trim the long tail of less-relevant results.((("stopwords", "performance and", "using minimum_should_match operator")))((("minimum_should_match parameter")))  It is useful for this purpose
alone but, as a nice side effect, it offers a similar performance benefit to
the `and` operator:

[source,json]
---------------------------------
{
    "match": {
        "text": {
            "query": "the quick brown fox",
            "minimum_should_match": "75%"
        }
    }
}
---------------------------------

In this example, at least three out of the four terms must match. This means
that the only docs that need to be considered are those that contain either the least or second least frequent terms.

This offers a huge performance gain over a simple query with the default `or`
operator!  But we can do better yet...

