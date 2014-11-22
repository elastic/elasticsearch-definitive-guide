[[function-score-filters]]
=== Boosting Filtered Subsets

Let's return to the problem that we were dealing with in <<ignoring-tfidf>>,
where we wanted to score((("boosting", "filtered subsets")))((("relevance", "controlling", "boosting filtered subsets"))) vacation homes by the number of features that each
home possesses.  We ended that section by wishing for a way to use cached
filters to affect the score, and with the `function_score` query we can do
just that.((("function_score query", "boosting filtered subsets")))

The examples we have shown thus far have used a single function for all
documents.  Now we want to divide the results into subsets by using filters (one
filter per feature), and apply a different function to each subset.

The function that we will use in this example is ((("weight function")))the `weight`, which is
similar to the `boost` parameter accepted by any query.  The difference is
that the `weight` is not normalized by Lucene into some obscure floating-point
number; it is used as is.

The structure of the query has to change somewhat to incorporate multiple
functions:

[source,json]
--------------------------------
GET /_search
{
  "query": {
    "function_score": {
      "filter": { <1>
        "term": { "city": "Barcelona" }
      },
      "functions": [ <2>
        {
          "filter": { "term": { "features": "wifi" }}, <3>
          "weight": 1
        },
        {
          "filter": { "term": { "features": "garden" }}, <3>
          "weight": 1
        },
        {
          "filter": { "term": { "features": "pool" }}, <3>
          "weight": 2 <4>
        }
      ],
      "score_mode": "sum", <5>
    }
  }
}
--------------------------------

<1> This `function_score` query has a `filter` instead of a `query`.
<2> The `functions` key holds a list of functions that should be applied.
<3> The function is applied only if the document matches the (optional) `filter`.
<4> The `pool` feature is more important than the others so it has a higher `weight`.
<5> The `score_mode` specifies how the values from each function should be combined.

The new features to note in this example are explained in the following sections.

==== filter Versus query

The first thing to note is that  we have specified a `filter` instead ((("filters", "in function_score query")))of a
`query`. In this example, we do not need full-text search. We just want to
return all documents that have `Barcelona` in the `city` field, logic that is
better expressed as a filter instead of a query.  All documents returned by
the filter will have a `_score` of `1`.  The `function_score` query accepts
either a `query` or a `filter`. If neither is specified, it will default to
using the `match_all` query.

==== functions

The `functions` key holds an array of functions to apply.((("function_score query", "functions key")))  Each entry in the
array may also optionally specify a `filter`, in which case the function will be applied only to documents that match that filter.  In this example, we
apply a `weight` of `1` (or `2` in the case of `pool`) to any document
that matches the filter.

==== score_mode

Each function returns a result, and we need a way of reducing these multiple
results to a single value that can be combined with the original `_score`.
This is the role ((("function_score query", "score_mode parameter")))((("score_mode parameter")))of the `score_mode` parameter, which accepts the following
values:

`multiply`::    
      Function results are multiplied together (default).
      
`sum`::        
      Function results are added up.
      
`avg`::         
      The average of all the function results.
      
`max`::         
      The highest function result is used.
      
`min`::         
      The lowest function result is used.
      
`first`::       
      Uses only the result from the first function that either doesn't have a filter or that has a filter matching the document.

In this case, we want to add the `weight` results from each matching
filter together to produce the final score, so we have used the `sum` score
mode.

Documents that don't match any of the filters will keep their original
`_score` of `1`.
