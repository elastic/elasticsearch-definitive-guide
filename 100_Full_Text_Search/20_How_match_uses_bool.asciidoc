=== How match Uses bool

By now, you have probably realized that <<match-multi-word,multiword `match`
queries>> simply wrap((("match query", "use of bool query in multi-word searches")))((("bool query", "use by match query in multi-word searches")))((("full text search", "how match query uses bool query"))) the generated `term` queries in a `bool` query. With the
default `or` operator, each `term` query is added as a `should` clause, so
at least one clause must match. These two queries are equivalent:

[source,js]
--------------------------------------------------
{
    "match": { "title": "brown fox"}
}
--------------------------------------------------

[source,js]
--------------------------------------------------
{
  "bool": {
    "should": [
      { "term": { "title": "brown" }},
      { "term": { "title": "fox"   }}
    ]
  }
}
--------------------------------------------------

With the `and` operator, all the `term` queries are added as `must` clauses,
so _all_ clauses must match. These two queries are equivalent:

[source,js]
--------------------------------------------------
{
    "match": {
        "title": {
            "query":    "brown fox",
            "operator": "and"
        }
    }
}
--------------------------------------------------

[source,js]
--------------------------------------------------
{
  "bool": {
    "must": [
      { "term": { "title": "brown" }},
      { "term": { "title": "fox"   }}
    ]
  }
}
--------------------------------------------------

And if the `minimum_should_match` parameter is((("minimum_should_match parameter", "match query using bool query"))) specified, it is passed
directly through to the `bool` query, making these two queries equivalent:

[source,js]
--------------------------------------------------
{
    "match": {
        "title": {
            "query":                "quick brown fox",
            "minimum_should_match": "75%"
        }
    }
}
--------------------------------------------------

[source,js]
--------------------------------------------------
{
  "bool": {
    "should": [
      { "term": { "title": "brown" }},
      { "term": { "title": "fox"   }},
      { "term": { "title": "quick" }}
    ],
    "minimum_should_match": 2 <1>
  }
}
--------------------------------------------------
<1> Because there are only three clauses, the `minimum_should_match`
    value of `75%` in the `match` query is rounded down to `2`.
    At least two out of the three `should`  clauses must match.


Of course, we would normally write these types of queries by using the `match`
query, but understanding how the `match` query works internally lets you take
control of the process when you need to. Some things can't be
done with a single `match` query, such as give more weight to some query terms
than to others. We will look at an example of this in the next section.

