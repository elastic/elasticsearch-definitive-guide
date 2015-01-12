=== Best Fields

Imagine that we have a website that allows ((("multifield search", "best fields queries")))((("best fields queries")))users to search blog posts, such
as these two documents:

[source,js]
--------------------------------------------------
PUT /my_index/my_type/1
{
    "title": "Quick brown rabbits",
    "body":  "Brown rabbits are commonly seen."
}

PUT /my_index/my_type/2
{
    "title": "Keeping pets healthy",
    "body":  "My quick brown fox eats rabbits on a regular basis."
}
--------------------------------------------------
// SENSE: 110_Multi_Field_Search/15_Best_fields.json

The user types in the words ``Brown fox'' and clicks Search.   We don't
know ahead of time if the user's search terms will be found in the `title` or
the `body` field of the post, but it is likely that the user is searching for
related words.  To our eyes, document 2 appears to be the better match, as it
contains both words that we are looking for.

Now we run the following `bool` query:

[source,js]
--------------------------------------------------
{
    "query": {
        "bool": {
            "should": [
                { "match": { "title": "Brown fox" }},
                { "match": { "body":  "Brown fox" }}
            ]
        }
    }
}
--------------------------------------------------
// SENSE: 110_Multi_Field_Search/15_Best_fields.json

And we find that this query gives document 1 the higher score:

[source,js]
--------------------------------------------------
{
  "hits": [
     {
        "_id":      "1",
        "_score":   0.14809652,
        "_source": {
           "title": "Quick brown rabbits",
           "body":  "Brown rabbits are commonly seen."
        }
     },
     {
        "_id":      "2",
        "_score":   0.09256032,
        "_source": {
           "title": "Keeping pets healthy",
           "body":  "My quick brown fox eats rabbits on a regular basis."
        }
     }
  ]
}
--------------------------------------------------

To understand why, think about how the `bool` query ((("bool query", "relevance score calculation")))((("relevance scores", "calculation in bool queries")))calculates its score:

1. It runs both of the queries in the `should` clause.
2. It adds their scores together.
3. It multiplies the total by the number of matching clauses.
4. It divides the result by the total number of clauses (two).

Document 1 contains the word `brown` in both fields, so both `match` clauses
are successful and have a score.  Document 2 contains both `brown` and
`fox` in the `body` field but neither word in the `title` field. The high
score from the `body` query is added to the zero score from the `title` query,
and multiplied by one-half, resulting in a lower overall score than for document 1.

In this example, the `title` and `body` fields are competing with each other.
We want to find the single _best-matching_ field.

What if, instead of combining the scores from each field, we used the score
from the _best-matching_ field as the overall score for the query?  This would
give preference to a single field that contains _both_ of the words we are
looking for, rather than the same word repeated in different fields.

[[dis-max-query]]
==== dis_max Query

Instead of the `bool` query, we can use the  `dis_max` or _Disjunction Max
Query_.  Disjunction means _or_((("dis_max (disjunction max) query"))) (while conjunction means _and_) so the
Disjunction Max Query simply means _return documents that match any of these
queries, and return the score of the best matching query_:

[source,js]
--------------------------------------------------
{
    "query": {
        "dis_max": {
            "queries": [
                { "match": { "title": "Brown fox" }},
                { "match": { "body":  "Brown fox" }}
            ]
        }
    }
}
--------------------------------------------------
// SENSE: 110_Multi_Field_Search/15_Best_fields.json

This produces the results that we want:

[source,js]
--------------------------------------------------
{
  "hits": [
     {
        "_id":      "2",
        "_score":   0.21509302,
        "_source": {
           "title": "Keeping pets healthy",
           "body":  "My quick brown fox eats rabbits on a regular basis."
        }
     },
     {
        "_id":      "1",
        "_score":   0.12713557,
        "_source": {
           "title": "Quick brown rabbits",
           "body":  "Brown rabbits are commonly seen."
        }
     }
  ]
}
--------------------------------------------------

