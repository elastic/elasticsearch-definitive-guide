[[nested-query]]
=== Querying a Nested Object

Because nested objects ((("nested objects", "querying")))are indexed as separate hidden documents, we can't
query them directly. ((("queries", "nested"))) Instead, we have to use the
http://bit.ly/1ziFQoR[`nested` query] or
http://bit.ly/1IOp94r[`nested` filter] to  access them:

[source,json]
--------------------------
GET /my_index/blogpost/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "title": "eggs" }}, <1>
        {
          "nested": {
            "path": "comments", <2>
            "query": {
              "bool": {
                "must": [ <3>
                  { "match": { "comments.name": "john" }},
                  { "match": { "comments.age":  28     }}
                ]
        }}}}
      ]
}}}
--------------------------
<1> The `title` clause operates on the root document.
<2> The `nested` clause ``steps down'' into the nested `comments` field.
    It no longer has access to fields in the root document, nor fields in
    any other nested document.
<3> The `comments.name` and `comments.age` clauses operate on the same nested
    document.

[TIP]
==================================================

A `nested` field can contain other `nested` fields.  Similarly, a `nested`
query can contain other `nested` queries. The nesting hierarchy is applied
as you would expect.

==================================================

Of course, a `nested` query could match several nested documents.
Each matching nested document would have its own relevance score, but these
multiple scores need to be reduced to a single score that can be applied to
the root document.

By default, it averages the scores of the matching nested documents. This can
be controlled by setting the `score_mode` parameter to `avg`, `max`, `sum`, or
even `none` (in which case the root document gets a constant score of `1.0`).

[source,json]
--------------------------
GET /my_index/blogpost/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "title": "eggs" }},
        {
          "nested": {
            "path":       "comments",
            "score_mode": "max", <1>
            "query": {
              "bool": {
                "must": [
                  { "match": { "comments.name": "john" }},
                  { "match": { "comments.age":  28     }}
                ]
        }}}}
      ]
}}}
--------------------------
<1> Give the root document the `_score` from the best-matching
    nested document.

[NOTE]
====
A `nested` filter behaves much like a `nested` query, except that it doesn't
accept the `score_mode` parameter.  It can be used only in _filter context_&#x2014;such as inside a `filtered` query--and it behaves like any other filter:
it includes or excludes, but it doesn't score.

While the results of the `nested` filter itself are not cached, the usual
caching rules apply to the filter _inside_ the `nested` filter.
====

