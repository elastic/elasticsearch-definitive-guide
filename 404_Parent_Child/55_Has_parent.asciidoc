[[has-parent]]
=== Finding Children by Their Parents

While a `nested` query can always ((("parent-child relationship", "finding children by their parents")))return only the root document as a result,
parent and child documents are independent and each can be queried
independently.  The `has_child` query allows us to return parents based on
data in their children, and the `has_parent` query returns children based on
data in their parents.((("has_parent query and filter", "query")))

It looks very similar to the `has_child` query.  This example returns
employees who work in the UK:

[source,json]
-------------------------
GET /company/employee/_search
{
  "query": {
    "has_parent": {
      "type": "branch", <1>
      "query": {
        "match": {
          "country": "UK"
        }
      }
    }
  }
}
-------------------------
<1> Returns children who have parents of type `branch`

The `has_parent` query also supports the `score_mode`,((("score_mode parameter"))) but it accepts only two
settings: `none` (the default) and `score`.  Each child can have only one
parent, so there is no need to reduce multiple scores into a single score for
the child.  The choice is simply between using the score (`score`) or not
(`none`).

.has_parent Filter
**************************

The `has_parent` filter works in the same way((("has_parent query and filter", "filter"))) as the `has_parent` query, except
that it doesn't support the `score_mode` parameter. It can be used only in
_filter context_&#x2014;such as inside a `filtered` query--and behaves
like any other filter: it includes or excludes, but doesn't score.

While the results of a `has_parent` filter are not cached, the usual caching
rules apply to the filter _inside_ the `has_parent` filter.

**************************

