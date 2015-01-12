[[multi-query-strings]]
=== Multiple Query Strings

The simplest multifield query to deal with is the ((("multifield search", "multiple query strings")))one where we can _map
search terms to specific fields_. If we know that _War and Peace_ is the
title, and Leo Tolstoy is the author, it is easy to write each of these
conditions as a `match` clause ((("match clause, mapping search terms to specific fields")))((("bool query", "mapping search terms to specific fields in match clause")))and to combine them with a <<bool-query,`bool`
query>>:

[source,js]
--------------------------------------------------
GET /_search
{
  "query": {
    "bool": {
      "should": [
        { "match": { "title":  "War and Peace" }},
        { "match": { "author": "Leo Tolstoy"   }}
      ]
    }
  }
}
--------------------------------------------------
// SENSE: 110_Multi_Field_Search/05_Multiple_query_strings.json

The `bool` query takes a _more-matches-is-better_ approach, so the score from
each `match` clause will be added together to provide the final `_score` for
each document. Documents that match both clauses will score higher than
documents that match just one clause.

Of course, you're not restricted to using just `match` clauses: the `bool`
query can wrap any other query type, ((("bool query", "nested bool query in")))including other `bool` queries.  We could
add a clause to specify that we prefer to see versions of the book that have
been translated by specific translators:

[source,js]
--------------------------------------------------
GET /_search
{
  "query": {
    "bool": {
      "should": [
        { "match": { "title":  "War and Peace" }},
        { "match": { "author": "Leo Tolstoy"   }},
        { "bool":  {
          "should": [
            { "match": { "translator": "Constance Garnett" }},
            { "match": { "translator": "Louise Maude"      }}
          ]
        }}
      ]
    }
  }
}
--------------------------------------------------
// SENSE: 110_Multi_Field_Search/05_Multiple_query_strings.json


Why did we put the translator clauses inside a separate `bool` query?  All four
`match` queries are `should` clauses, so why didn't we just put the translator
clauses at the same level as the title and author clauses?

The answer lies in how the score is calculated.((("relevance scores", "calculation in bool queries")))  The `bool` query runs each
`match` query, adds their scores together, then multiplies by the number of
matching clauses, and divides by the total number of clauses. Each clause at
the same level has the same weight. In the preceding query, the `bool` query
containing the translator clauses counts for one-third of the total score. If we had
put the translator clauses at the same level as title and author, they
would have reduced the contribution of the title and author clauses to one-quarter each.

[[prioritising-clauses]]
==== Prioritizing Clauses

It is likely that an even one-third split between clauses is not what we need for
the preceding query. ((("multifield search", "multiple query strings", "prioritizing query clauses")))((("bool query", "prioritizing clauses"))) Probably we're more interested in the title and author
clauses then we are in the translator clauses. We need to tune the query to
make the title and author clauses relatively more important.

The simplest weapon in our tuning arsenal is the `boost` parameter. To
increase the weight of the `title` and `author` fields, give ((("boost parameter", "using to prioritize query clauses")))((("weight", "using boost parameter to prioritize query clauses")))them a `boost`
value higher than `1`:

[source,js]
--------------------------------------------------
GET /_search
{
  "query": {
    "bool": {
      "should": [
        { "match": { <1>
            "title":  {
              "query": "War and Peace",
              "boost": 2
        }}},
        { "match": { <1>
            "author":  {
              "query": "Leo Tolstoy",
              "boost": 2
        }}},
        { "bool":  { <2>
            "should": [
              { "match": { "translator": "Constance Garnett" }},
              { "match": { "translator": "Louise Maude"      }}
            ]
        }}
      ]
    }
  }
}
--------------------------------------------------
// SENSE: 110_Multi_Field_Search/05_Multiple_query_strings.json

<1> The `title` and `author` clauses have a `boost` value of `2`.
<2> The nested `bool` clause has the default `boost` of `1`.

The ``best'' value for the `boost` parameter is most easily determined by
trial and error: set a `boost` value, run test queries, repeat. A reasonable
range for `boost` lies between `1` and `10`, maybe `15`. Boosts higher than
that have little more impact because scores are
<<boost-normalization,normalized>>.

