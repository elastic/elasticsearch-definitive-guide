[[top-hits]]
=== Field Collapsing

A common requirement is the need to present search results grouped by a particular
field. ((("field collapsing")))((("relationships", "field collapsing")))We might want to return the most relevant blog posts _grouped_ by the
user's name. ((("terms aggregation")))((("aggregations", "field collapsing"))) Grouping by name implies the need for a `terms` aggregation.  To
be able to group on the user's _whole_ name, the name field should be
available in its original `not_analyzed` form, as explained in
<<aggregations-and-analysis>>:

[source,json]
--------------------------------
PUT /my_index/_mapping/blogpost
{
  "properties": {
    "user": {
      "properties": {
        "name": { <1>
          "type": "string",
          "fields": {
            "raw": { <2>
              "type":  "string",
              "index": "not_analyzed"
            }
          }
        }
      }
    }
  }
}
--------------------------------
<1> The `user.name` field will be used for full-text search.
<2> The `user.name.raw` field will be used for grouping with the `terms`
    aggregation.

Then add some data:

[source,json]
--------------------------------
PUT /my_index/user/1
{
  "name": "John Smith",
  "email": "john@smith.com",
  "dob": "1970/10/24"
}

PUT /my_index/blogpost/2
{
  "title": "Relationships",
  "body": "It's complicated...",
  "user": {
    "id": 1,
    "name": "John Smith"
  }
}

PUT /my_index/user/3
{
  "name": "Alice John",
  "email": "alice@john.com",
  "dob": "1979/01/04"
}

PUT /my_index/blogpost/4
{
  "title": "Relationships are cool",
  "body": "It's not complicated at all...",
  "user": {
    "id": 3,
    "name": "Alice John"
  }
}
--------------------------------

Now we can run a query looking for blog posts about `relationships`, by users
called `John`, and group the results by user, thanks to the
http://bit.ly/1CrlWFQ[`top_hits` aggregation]:

[source,json]
--------------------------------
GET /my_index/blogpost/_search?search_type=count <1>
{
  "query": { <2>
    "bool": {
      "must": [
        { "match": { "title":     "relationships" }},
        { "match": { "user.name": "John"          }}
      ]
    }
  },
  "aggs": {
    "users": {
      "terms": {
        "field":   "user.name.raw",      <3>
        "order": { "top_score": "desc" } <4>
      },
      "aggs": {
        "top_score": { "max":      { "script":  "_score"           }}, <4>
        "blogposts": { "top_hits": { "_source": "title", "size": 5 }}  <5>
      }
    }
  }
}
--------------------------------
<1> The blog posts that we are interested in are returned under the
    `blogposts` aggregation, so we can disable the usual search `hits` by
    setting the `search_type=count`.
<2> The `query` returns blog posts about `relationships` by users named `John`.
<3> The `terms` aggregation creates a bucket for each `user.name.raw` value.
<4> The `top_score` aggregation orders the terms in the `users` aggregation
    by the top-scoring document in each bucket.
<5> The `top_hits` aggregation returns just the `title` field of the five most
    relevant blog posts for each user.

The abbreviated response is shown here:

[source,json]
--------------------------------
...
"hits": {
  "total":     2,
  "max_score": 0,
  "hits":      [] <1>
},
"aggregations": {
  "users": {
     "buckets": [
        {
           "key":       "John Smith", <2>
           "doc_count": 1,
           "blogposts": {
              "hits": { <3>
                 "total":     1,
                 "max_score": 0.35258877,
                 "hits": [
                    {
                       "_index": "my_index",
                       "_type":  "blogpost",
                       "_id":    "2",
                       "_score": 0.35258877,
                       "_source": {
                          "title": "Relationships"
                       }
                    }
                 ]
              }
           },
           "top_score": { <4>
              "value": 0.3525887727737427
           }
        },
...
--------------------------------
<1> The `hits` array is empty because we set `search_type=count`.
<2> There is a bucket for each user who appeared in the top results.
<3> Under each user bucket there is a `blogposts.hits` array containing
    the top results for that user.
<4> The user buckets are sorted by the user's most relevant blog post.

Using the `top_hits` aggregation is the((("top_hits aggregation"))) equivalent of running a query to
return the names of the users with the most relevant blog posts, and then running
the same query for each user, to get their best blog posts. But it is much more
efficient.

The top hits returned in each bucket are the result of running a light
_mini-query_ based on the original main query.  The mini-query supports the
usual features that you would expect from search such as highlighting and
pagination.

