=== Boosting Query Clauses

Of course, the `bool` query isn't restricted ((("full text search", "boosting query clauses")))to combining simple one-word
`match` queries. It can combine any other query, including other `bool`
queries.((("relevance scores", "controlling weight of query clauses")))  It is commonly used to fine-tune the relevance `_score` for each
document by combining the scores from several distinct queries.

Imagine that we want to search for documents((("bool query", "boosting weight of query clauses")))((("weight", "controlling for query clauses"))) about "full-text search,"  but we
want to give more _weight_ to documents that also mention "Elasticsearch" or
"Lucene." By _more weight_, we mean that documents mentioning
"Elasticsearch" or "Lucene" will receive a higher relevance `_score` than
those that don't, which means that they will appear higher in the list of
results.

A simple `bool` _query_ allows us to write this fairly complex logic as follows:

[source,js]
--------------------------------------------------
GET /_search
{
    "query": {
        "bool": {
            "must": {
                "match": {
                    "content": { <1>
                        "query":    "full text search",
                        "operator": "and"
                    }
                }
            },
            "should": [ <2>
                { "match": { "content": "Elasticsearch" }},
                { "match": { "content": "Lucene"        }}
            ]
        }
    }
}
--------------------------------------------------
// SENSE: 100_Full_Text_Search/25_Boost.json

<1> The `content` field must contain all of the words `full`, `text`, and `search`.
<2> If the `content` field also contains `Elasticsearch` or `Lucene`,
    the document will receive a higher `_score`.

The more `should` clauses that match, the more relevant the document.  So far,
so good.

But what if we want to give more weight to the docs that contain `Lucene` and
even more weight to the docs containing `Elasticsearch`?

We can control ((("boost parameter")))the relative weight of any query clause by specifying a `boost`
value, which defaults to `1`. A `boost` value greater than `1` increases the
relative weight of that clause.  So we could  rewrite the preceding query as
follows:

[source,js]
--------------------------------------------------
GET /_search
{
    "query": {
        "bool": {
            "must": {
                "match": {  <1>
                    "content": {
                        "query":    "full text search",
                        "operator": "and"
                    }
                }
            },
            "should": [
                { "match": {
                    "content": {
                        "query": "Elasticsearch",
                        "boost": 3 <2>
                    }
                }},
                { "match": {
                    "content": {
                        "query": "Lucene",
                        "boost": 2 <3>
                    }
                }}
            ]
        }
    }
}
--------------------------------------------------
// SENSE: 100_Full_Text_Search/25_Boost.json

<1> These clauses use the default `boost` of `1`.
<2> This clause is the most important, as it has the highest `boost`.
<3> This clause is more important than the default, but not as important
    as the `Elasticsearch` clause.

[NOTE]
[[boost-normalization]]
====
The `boost` parameter is used to increase((("boost parameter", "score normalied after boost applied"))) the relative weight of a clause
(with a `boost` greater than `1`) or decrease the relative weight (with a
`boost` between `0` and `1`), but the increase or decrease is not linear. In
other words, a `boost` of `2` does not result in double the `_score`.

Instead, the new `_score` is _normalized_ after((("normalization", "score normalied after boost applied"))) the boost is applied. Each
type of query has its own normalization algorithm, and the details are beyond
the scope of this book. Suffice to say that a higher `boost` value results in
a higher `_score`.

If you are implementing your own scoring model not based on TF/IDF and you
need more control over the boosting process, you can use the
<<function-score-query,`function_score` query>> to((("function_score query"))) manipulate a document's
boost without the normalization step.
====

We present other ways of combining queries in the next chapter,
<<multi-field-search>>. But first, let's take a look at the other important
feature of queries: text analysis.
