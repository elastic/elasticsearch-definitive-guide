=== Closer Is Better

Whereas a phrase query simply excludes documents that don't contain the exact
query phrase, a _proximity query_&#x2014;a ((("proximity matching", "proximity queries")))((("slop parameter", "proximity queries and")))phrase query where `slop` is greater
than `0`&#x2014;incorporates the proximity of the query terms into the final
relevance `_score`. By setting a high `slop` value like `50` or `100`, you can
exclude documents in which the words are really too far apart, but give a higher
score to documents in which the words are closer together.

The following proximity query for `quick dog` matches both documents that
contain the words `quick` and `dog`, but gives a higher score to the
document((("relevance scores", "for proximity queries"))) in which the words are nearer to each other:

[source,js]
--------------------------------------------------
POST /my_index/my_type/_search
{
   "query": {
      "match_phrase": {
         "title": {
            "query": "quick dog",
            "slop":  50 <1>
         }
      }
   }
}
--------------------------------------------------
// SENSE: 120_Proximity_Matching/20_Scoring.json

<1> Note the high `slop` value.

[source,js]
--------------------------------------------------
{
  "hits": [
     {
        "_id":      "3",
        "_score":   0.75, <1>
        "_source": {
           "title": "The quick brown fox jumps over the quick dog"
        }
     },
     {
        "_id":      "2",
        "_score":   0.28347334, <2>
        "_source": {
           "title": "The quick brown fox jumps over the lazy dog"
        }
     }
  ]
}
--------------------------------------------------
<1> Higher score because `quick` and `dog` are close together
<2> Lower score because `quick` and `dog` are further apart
