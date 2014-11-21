[[proximity-relevance]]
=== Proximity for Relevance

Although proximity queries are useful, the fact that they require all terms to be
present can make them overly strict.((("proximity matching", "using for relevance")))((("relevance", "proximity queries for"))) It's the same issue that we discussed in
<<match-precision>> in <<full-text-search>>: if six out of seven terms match,
a document is probably relevant enough to be worth showing to the user, but
the `match_phrase` query would exclude it.

Instead of using proximity matching as an absolute requirement, we can
use it as a _signal_&#x2014;as one of potentially many queries, each of which
contributes to the overall score for each document (see <<most-fields>>).

The fact that we want to add together the scores from multiple queries implies
that we should combine them by using the `bool` query.((("bool query", "proximity query for relevance in")))

We can use a simple `match` query as a `must` clause. This is the query that
will determine which documents are included in our result set.  We can trim
the long tail with the `minimum_should_match` parameter.  Then we can add other,
more specific queries as `should` clauses. Every one that matches will
increase the relevance of the matching docs.

[source,js]
--------------------------------------------------
GET /my_index/my_type/_search
{
  "query": {
    "bool": {
      "must": {
        "match": { <1>
          "title": {
            "query":                "quick brown fox",
            "minimum_should_match": "30%"
          }
        }
      },
      "should": {
        "match_phrase": { <2>
          "title": {
            "query": "quick brown fox",
            "slop":  50
          }
        }
      }
    }
  }
}
--------------------------------------------------
// SENSE: 120_Proximity_Matching/25_Relevance.json

<1> The `must` clause includes or excludes documents from the result set.
<2> The `should` clause increases the relevance score of those documents that
    match.

We could, of course, include other queries in the `should` clause, where each
query targets a specific aspect of relevance.
