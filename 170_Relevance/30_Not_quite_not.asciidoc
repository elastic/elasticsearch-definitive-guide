[[not-quite-not]]
=== Not Quite Not

A search on the Internet for ``Apple'' is likely to return results about the
company, the fruit, ((("relevance", "controlling", "must_not clause in bool query")))((("bool query", "must_not clause")))and various recipes.  We could try to narrow it down to
just the company by excluding words like `pie`, `tart`, `crumble`, and `tree`,
using a `must_not` clause in a `bool` query:

[source,json]
-------------------------------
GET /_search
{
  "query": {
    "bool": {
      "must": {
        "match": {
          "text": "apple"
        }
      },
      "must_not": {
        "match": {
          "text": "pie tart fruit crumble tree"
        }
      }
    }
  }
}
-------------------------------

But who is to say that we wouldn't miss a very relevant document about Apple
the company by excluding `tree` or `crumble`?  Sometimes, `must_not` can be
too strict.

[[boosting-query]]
==== boosting Query

The  http://bit.ly/1IO281f[`boosting` query] solves((("boosting query")))((("relevance", "controlling", "boosting query"))) this problem.
It allows us to still include results that appear to be about the fruit or
the pastries, but to downgrade them--to rank them lower than they would
otherwise be:

[source,json]
-------------------------------
GET /_search
{
  "query": {
    "boosting": {
      "positive": {
        "match": {
          "text": "apple"
        }
      },
      "negative": {
        "match": {
          "text": "pie tart fruit crumble tree"
        }
      },
      "negative_boost": 0.5
    }
  }
}
-------------------------------

It accepts a `positive` query and a `negative` query.((("positive query and negative query (in boosting query)")))  Only documents that
match the `positive` query will be included in the results list, but documents
that also match the `negative` query will be downgraded by multiplying the
original `_score` of((("negative_boost"))) the document with the `negative_boost`.

For this to work, the `negative_boost` must be less than `1.0`.  In this
example, any documents that contain any of the negative terms will have their
`_score` cut in half.
