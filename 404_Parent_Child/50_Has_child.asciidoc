[[has-child]]
=== Finding Parents by Their Children

The `has_child` query and filter can be used to find parent documents based on
the contents of their children.((("has_child query and filter")))((("parent-child relationship", "finding parents by their children")))  For instance, we could find all branches that
have employees born after 1980 with a query like this:

[source,json]
-------------------------
GET /company/branch/_search
{
  "query": {
    "has_child": {
      "type": "employee",
      "query": {
        "range": {
          "dob": {
            "gte": "1980-01-01"
          }
        }
      }
    }
  }
}
-------------------------

Like the <<nested-query,`nested` query>>, the `has_child` query could
match several child documents,((("has_child query and filter", "query"))) each with a different relevance
score. How these scores are reduced to a single score for the parent document
depends on the `score_mode` parameter. The default setting is `none`, which
ignores the child scores and assigns a score of `1.0` to the parents, but it
also accepts `avg`, `min`, `max`, and `sum`.

The following query will return both `london` and `liverpool`, but `london`
will get a better score because `Alice Smith` is a better match than
`Barry Smith`:

[source,json]
-------------------------
GET /company/branch/_search
{
  "query": {
    "has_child": {
      "type":       "employee",
      "score_mode": "max",
      "query": {
        "match": {
          "name": "Alice Smith"
        }
      }
    }
  }
}
-------------------------

TIP: The default `score_mode` of `none` is significantly faster than the other
modes because Elasticsearch doesn't need to calculate the score for each child
document. Set it to `avg`, `min`, `max`, or `sum` only if you care about the
score.((("parent-child relationship", "finding parents by their children", "min_children and max_children")))

[[min-max-children]]
==== min_children and max_children

The `has_child` query and filter both accept the `min_children` and
`max_children` parameters,((("min_children parameter")))((("max_children parameter")))((("has_child query and filter", "min_children or max_children parameters"))) which will return the parent document only if the
number of matching children is within the specified range.

This query will match only branches that have at least two employees:

[source,json]
-------------------------
GET /company/branch/_search
{
  "query": {
    "has_child": {
      "type":         "employee",
      "min_children": 2, <1>
      "query": {
        "match_all": {}
      }
    }
  }
}
-------------------------
<1> A branch must have at least two employees in order to match.

The performance of a `has_child` query or filter with the `min_children` or
`max_children` parameters is much the same as a `has_child` query with scoring
enabled.

.has_child Filter
**************************

The `has_child` filter works((("has_child query and filter", "filter"))) in the same way as the `has_child` query, except
that it doesn't support the `score_mode` parameter. It can be used only in
_filter context_&#x2014;such as inside a `filtered` query--and behaves
like any other filter: it includes or excludes, but doesn't score.

While the results of a `has_child` filter are not cached, the usual caching
rules apply to the filter _inside_ the `has_child` filter.

**************************
