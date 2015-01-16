[[match-multi-word]]
=== Multiword Queries

If we could search for only one word at a time, full-text search would be
pretty inflexible. Fortunately, the `match` query((("full text search", "multi-word queries")))((("match query", "multi-word query"))) makes multiword queries
just as simple:

[source,js]
--------------------------------------------------
GET /my_index/my_type/_search
{
    "query": {
        "match": {
            "title": "BROWN DOG!"
        }
    }
}
--------------------------------------------------
// SENSE: 100_Full_Text_Search/05_Match_query.json

The preceding query returns all four documents in the results list:

[source,js]
--------------------------------------------------
{
  "hits": [
     {
        "_id":      "4",
        "_score":   0.73185337, <1>
        "_source": {
           "title": "Brown fox brown dog"
        }
     },
     {
        "_id":      "2",
        "_score":   0.47486103, <2>
        "_source": {
           "title": "The quick brown fox jumps over the lazy dog"
        }
     },
     {
        "_id":      "3",
        "_score":   0.47486103, <2>
        "_source": {
           "title": "The quick brown fox jumps over the quick dog"
        }
     },
     {
        "_id":      "1",
        "_score":   0.11914785, <3>
        "_source": {
           "title": "The quick brown fox"
        }
     }
  ]
}
--------------------------------------------------

<1> Document 4 is the most relevant because it contains `"brown"` twice and `"dog"`
    once.

<2> Documents 2 and 3 both contain `brown` and `dog` once each, and the `title`
    field is the same length in both docs, so they have the same score.

<3> Document 1 matches even though it contains only `brown`, not `dog`.

Because the `match` query has to look for two terms&#x2014;`["brown","dog"]`&#x2014;internally it has to execute two `term` queries and combine their individual
results into the overall result. To do this, it wraps the two `term` queries
in a `bool` query, which we examine in detail in <<bool-query>>.

The important thing to take away from this is that any document whose
`title` field contains _at least one of the specified terms_ will match the
query.  The more terms that match, the more relevant the document.

[[match-improving-precision]]
==== Improving Precision

Matching any document that contains _any_ of the query terms may result in  a
long tail of seemingly irrelevant results. ((("full text search", "multi-word queries", "improving precision")))((("precision", "improving for full text search multi-word queries"))) It's a shotgun approach to search.
Perhaps we want to show only documents that contain _all_ of the query terms.
In other words, instead of `brown OR dog`, we want to return only documents
that match `brown AND dog`.

The `match` query accepts an `operator` parameter((("match query", "operator parameter")))((("or operator", "in match queries")))((("and operator", "in match queries"))) that defaults to `or`.
You can change it to `and` to require that all specified terms must match:

[source,js]
--------------------------------------------------
GET /my_index/my_type/_search
{
    "query": {
        "match": {
            "title": {      <1>
                "query":    "BROWN DOG!",
                "operator": "and"
            }
        }
    }
}
--------------------------------------------------
// SENSE: 100_Full_Text_Search/05_Match_query.json

<1> The structure of the `match` query has to change slightly in order to
    accommodate the `operator` parameter.

This query would exclude document 1, which contains only one of the two terms.

[[match-precision]]
==== Controlling Precision

The choice between _all_ and _any_ is a bit((("full text search", "multi-word queries", "controlling precision"))) too black-or-white. What if the
user specified five query terms, and a document contains only four of them?
Setting `operator` to `and` would exclude this document.

Sometimes that is exactly what you want, but for most full-text search use
cases, you want to include documents that may be relevant but exclude those
that are unlikely to be relevant.  In other words, we need something
in-between.

The `match` query supports((("match query", "minimum_should_match parameter")))((("minimum_should_match parameter"))) the `minimum_should_match` parameter, which allows
you to specify the number of terms that must match for a document to be considered
relevant.  While you can specify an absolute number of terms, it usually makes
sense to specify a percentage instead, as you have no control over the number of words the user may enter:

[source,js]
--------------------------------------------------
GET /my_index/my_type/_search
{
  "query": {
    "match": {
      "title": {
        "query":                "quick brown dog",
        "minimum_should_match": "75%"
      }
    }
  }
}
--------------------------------------------------
// SENSE: 100_Full_Text_Search/05_Match_query.json

When specified as a percentage, `minimum_should_match` does the right thing:
in the preceding example with three terms, `75%` would be rounded down to `66.6%`,
or two out of the three terms. No matter what you set it to, at least one term
must match for a document to be considered a match.

[NOTE]
====
The `minimum_should_match` parameter is flexible, and different rules can
be applied depending on the number of terms the user enters.  For the full
documentation see the
http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/query-dsl-minimum-should-match.html#query-dsl-minimum-should-match
====

To fully understand how the `match` query handles multiword queries, we need
to look at how to combine multiple queries with the `bool` query.
