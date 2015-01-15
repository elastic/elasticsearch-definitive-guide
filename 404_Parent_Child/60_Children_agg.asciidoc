[[children-agg]]
=== Children Aggregation

Parent-child supports a
http://bit.ly/1xtpjaz[`children` aggregation]  as ((("aggregations", "children aggregation")))((("children aggregation")))((("parent-child relationship", "children aggregation")))a direct analog to the `nested` aggregation discussed in
<<nested-aggregation>>.  A parent aggregation (the equivalent of
`reverse_nested`) is not supported.

This example demonstrates how we could determine the favorite hobbies of our
employees by country:

[source,json]
-------------------------
GET /company/branch/_search?search_type=count
{
  "aggs": {
    "country": {
      "terms": { <1>
        "field": "country"
      },
      "aggs": {
        "employees": {
          "children": { <2>
            "type": "employee"
          },
          "aggs": {
            "hobby": {
              "terms": { <3>
                "field": "employee.hobby"
              }
            }
          }
        }
      }
    }
  }
}
-------------------------
<1> The `country` field in the `branch` documents.
<2> The `children` aggregation joins the parent documents with
    their associated children of type `employee`.
<3> The `hobby` field from the `employee` child documents.

