[[query-scoring]]
=== Manipulating Relevance with Query Structure

The Elasticsearch query DSL is immensely flexible.((("relevance", "controlling", "manipulating relevance with query structure")))((("queries", "manipulating relevance with query structure")))  You can move individual
query clauses up and down the query hierarchy to make a clause more or less
important.  For instance, imagine the following query:

    quick OR brown OR red OR fox

We could write this as a `bool` query with ((("bool query", "manipulating relevance with query structure")))all terms at the same level:

[source,json]
------------------------------
GET /_search
{
  "query": {
    "bool": {
      "should": [
        { "term": { "text": "quick" }},
        { "term": { "text": "brown" }},
        { "term": { "text": "red"   }},
        { "term": { "text": "fox"   }}
      ]
    }
  }
}
------------------------------

But this query might score a document that contains `quick`, `red`, and
`brown` the same as another document that contains `quick`, `red`, and `fox`.
_Red_ and _brown_ are synonyms and we probably only need one of them to match.
Perhaps we really want to express the query as follows:

    quick OR (brown OR red) OR fox

According to standard Boolean logic, this is exactly the same as the original
query, but as we have already seen in <<bool-query,Combining Queries>>, a `bool` query does not concern itself only with whether a document matches, but also with how
_well_ it matches.

A better way to write this query is as follows:

[source,json]
------------------------------
GET /_search
{
  "query": {
    "bool": {
      "should": [
        { "term": { "text": "quick" }},
        { "term": { "text": "fox"   }},
        {
          "bool": {
            "should": [
              { "term": { "text": "brown" }},
              { "term": { "text": "red"   }}
            ]
          }
        }
      ]
    }
  }
}
------------------------------

Now, `red` and `brown` compete with each other at their own level, and `quick`,
`fox`, and `red OR brown` are the top-level competitive terms.

We have already discussed how the <<match-query,`match`>>,
<<multi-match-query,`multi_match`>>, <<term-vs-full-text,`term`>>,
<<bool-query,`bool`>>, and  <<dis-max-query,`dis_max`>> queries can be used
to manipulate scoring. In the rest of this chapter, we present
three other scoring-related queries: the `boosting` query, the
`constant_score` query, and the `function_score` query.

