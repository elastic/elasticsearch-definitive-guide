[[multi-match-query]]
=== multi_match Query

The `multi_match` query provides ((("multifield search", "multi_match query")))((("multi_match queries")))((("match query", "multi_match queries"))) a convenient shorthand way of running
the same query against multiple fields.

[NOTE]
====
There are several types of `multi_match` query, three of which just
happen to coincide with the three scenarios that we listed in
<<know-your-data>>:  `best_fields`, `most_fields`, and `cross_fields`.
====

By default, this query runs as type `best_fields`, which means((("best fields queries", "multi-match queries")))((("dis_max (disjunction max) query", "multi_match query wrapped in"))) that it generates a
`match` query for each field and wraps them in a `dis_max` query. This
`dis_max` query

[source,js]
--------------------------------------------------
{
  "dis_max": {
    "queries":  [
      {
        "match": {
          "title": {
            "query": "Quick brown fox",
            "minimum_should_match": "30%"
          }
        }
      },
      {
        "match": {
          "body": {
            "query": "Quick brown fox",
            "minimum_should_match": "30%"
          }
        }
      },
    ],
    "tie_breaker": 0.3
  }
}
--------------------------------------------------

could be rewritten more concisely with `multi_match` as follows:

[source,js]
--------------------------------------------------
{
    "multi_match": {
        "query":                "Quick brown fox",
        "type":                 "best_fields", <1>
        "fields":               [ "title", "body" ],
        "tie_breaker":          0.3,
        "minimum_should_match": "30%" <2>
    }
}
--------------------------------------------------
// SENSE: 110_Multi_Field_Search/25_Best_fields.json

<1> The `best_fields` type is the default and can be left out.
<2> Parameters like `minimum_should_match` or `operator` are passed through to
    the generated `match` queries.

==== Using Wildcards in Field Names

Field names can be specified with wildcards: any field that matches the
wildcard pattern((("multi_match queries", "wildcards in field names")))((("wildcards in field names")))((("fields", "wildcards in field names"))) will be included in the search. You could match on the
`book_title`, `chapter_title`, and `section_title` fields, with the following:

[source,js]
--------------------------------------------------
{
    "multi_match": {
        "query":  "Quick brown fox",
        "fields": "*_title"
    }
}
--------------------------------------------------

==== Boosting Individual Fields

Individual fields can be boosted by using the caret (`^`) syntax: just add
`^boost` after the field((("multi_match queries", "boosting individual fields")))((("boost parameter", "boosting individual fields in multi_match queries"))) name, where `boost` is a floating-point number:

[source,js]
--------------------------------------------------
{
    "multi_match": {
        "query":  "Quick brown fox",
        "fields": [ "*_title", "chapter_title^2" ] <1>
    }
}
--------------------------------------------------

<1> The `chapter_title` field has a `boost` of `2`, while the `book_title` and
    `section_title` fields have a default boost of `1`.
