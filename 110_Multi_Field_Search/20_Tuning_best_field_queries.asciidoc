=== Tuning Best Fields Queries

What would happen if the user((("multifield search", "best fields queries", "tuning")))((("best fields queries", "tuning"))) had searched instead for ``quick pets''?  Both
documents contain the word `quick`, but only document 2 contains the word
`pets`. Neither document contains _both words_ in the _same field_.

A simple `dis_max` query like the following would ((("dis_max (disjunction max) query")))((("relevance scores", "calculation in dis_max queries")))choose the single best
matching field, and ignore the other:

[source,js]
--------------------------------------------------
{
    "query": {
        "dis_max": {
            "queries": [
                { "match": { "title": "Quick pets" }},
                { "match": { "body":  "Quick pets" }}
            ]
        }
    }
}
--------------------------------------------------
// SENSE: 110_Multi_Field_Search/15_Best_fields.json

[source,js]
--------------------------------------------------
{
  "hits": [
     {
        "_id": "1",
        "_score": 0.12713557, <1>
        "_source": {
           "title": "Quick brown rabbits",
           "body": "Brown rabbits are commonly seen."
        }
     },
     {
        "_id": "2",
        "_score": 0.12713557, <1>
        "_source": {
           "title": "Keeping pets healthy",
           "body": "My quick brown fox eats rabbits on a regular basis."
        }
     }
   ]
}
--------------------------------------------------
<1> Note that the scores are exactly the same.

We would probably expect documents that match on both the `title` field and
the `body` field to rank higher than documents that match on just one field,
but this isn't the case. Remember: the `dis_max` query simply uses the
`_score` from the _single_ best-matching clause.

==== tie_breaker

It is possible, however, to((("dis_max (disjunction max) query", "using tie_breaker parameter")))((("relevance scores", "calculation in dis_max queries", "using tie_breaker parameter"))) also take the `_score` from the other matching
clauses into account, by specifying ((("tie_breaker parameter")))the `tie_breaker` parameter:

[source,js]
--------------------------------------------------
{
    "query": {
        "dis_max": {
            "queries": [
                { "match": { "title": "Quick pets" }},
                { "match": { "body":  "Quick pets" }}
            ],
            "tie_breaker": 0.3
        }
    }
}
--------------------------------------------------
// SENSE: 110_Multi_Field_Search/15_Best_fields.json

This gives us the following results:

[source,js]
--------------------------------------------------
{
  "hits": [
     {
        "_id": "2",
        "_score": 0.14757764, <1>
        "_source": {
           "title": "Keeping pets healthy",
           "body": "My quick brown fox eats rabbits on a regular basis."
        }
     },
     {
        "_id": "1",
        "_score": 0.124275915, <1>
        "_source": {
           "title": "Quick brown rabbits",
           "body": "Brown rabbits are commonly seen."
        }
     }
   ]
}
--------------------------------------------------
<1> Document 2 now has a small lead over document 1.

The `tie_breaker` parameter makes the `dis_max` query behave more like a
halfway house between `dis_max` and `bool`. It changes the score calculation
as follows:

1. Take the `_score` of the best-matching clause.
2. Multiply the score of each of the other matching clauses by the `tie_breaker`.
3. Add them all together and normalize.

With the `tie_breaker`, all matching clauses count, but the best-matching
clause counts most.

[NOTE]
====
The `tie_breaker` can be a floating-point value between `0` and `1`, where `0`
uses just the best-matching clause((("tie_breaker parameter", "value of"))) and `1` counts all matching clauses
equally.  The exact value can be tuned based on your data and queries, but a
reasonable value should be close to zero, (for example, `0.1 - 0.4`), in order not to
overwhelm the best-matching nature of `dis_max`.
====

