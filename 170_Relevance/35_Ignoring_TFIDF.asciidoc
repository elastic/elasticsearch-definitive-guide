[[ignoring-tfidf]]
=== Ignoring TF/IDF

Sometimes we just don't care about TF/IDF.((("relevance", "controlling", "ignoring  TF/IDF")))((("Term Frequency/Inverse Document Frequency  (TF/IDF) similarity algorithm", "ignoring")))  All we want to know is that a certain
word appears in a field. Perhaps we are searching for a vacation home and we
want to find houses that have as many of these features as possible:

* WiFi
* Garden
* Pool

The vacation home documents look something like this:

[source,json]
------------------------------
{ "description": "A delightful four-bedroomed house with ... " }
------------------------------

We could use a simple `match` query:

[source,json]
------------------------------
GET /_search
{
  "query": {
    "match": {
      "description": "wifi garden pool"
    }
  }
}
------------------------------

However, this isn't really _full-text search_. In this case, TF/IDF just gets
in the way.  We don't care whether `wifi` is a common term, or how often it
appears in the document.  All we care about is that it does appear.
In fact, we just want to rank houses by the number of features they have--the more, the better. If a feature is present, it should score `1`, and if it
isn't, `0`.

[[constant-score-query]]
==== constant_score Query

Enter the http://bit.ly/1DIgSAK[`constant_score`] query.
This ((("constant_score query")))query can wrap either a query or a filter, and assigns a score of
`1` to any documents that match, regardless of TF/IDF:

[source,json]
------------------------------
GET /_search
{
  "query": {
    "bool": {
      "should": [
        { "constant_score": {
          "query": { "match": { "description": "wifi" }}
        }},
        { "constant_score": {
          "query": { "match": { "description": "garden" }}
        }},
        { "constant_score": {
          "query": { "match": { "description": "pool" }}
        }}
      ]
    }
  }
}
------------------------------

Perhaps not all features are equally important--some have more value to
the user than others. If the most important feature is the pool, we could
boost that clause to make it count for more:

[source,json]
------------------------------
GET /_search
{
  "query": {
    "bool": {
      "should": [
        { "constant_score": {
          "query": { "match": { "description": "wifi" }}
        }},
        { "constant_score": {
          "query": { "match": { "description": "garden" }}
        }},
        { "constant_score": {
          "boost":   2 <1>
          "query": { "match": { "description": "pool" }}
        }}
      ]
    }
  }
}
------------------------------
<1> A matching `pool` clause would add a score of `2`, while
    the other clauses would add a score of only `1` each.

NOTE: The final score for each result is not simply the sum of the scores of
all matching clauses.  The <<coord,coordination factor>> and
<<query-norm,query normalization factor>> are still taken into account.

We could improve our vacation home documents by adding a `not_analyzed`
`features` field to our vacation homes:

[source,json]
------------------------------
{ "features": [ "wifi", "pool", "garden" ] }
------------------------------

By default, a `not_analyzed` field has <<field-norm,field-length norms>>
disabled ((("not_analyzed fields", "field length norms and index_options")))and has `index_options` set to `docs`, disabling
<<tf,term frequencies>>, but the problem remains: the
<<idf,inverse document frequency>> of each term is still taken into account.

We could use the same approach that we used previously, with the `constant_score`
query:

[source,json]
------------------------------
GET /_search
{
  "query": {
    "bool": {
      "should": [
        { "constant_score": {
          "query": { "match": { "features": "wifi" }}
        }},
        { "constant_score": {
          "query": { "match": { "features": "garden" }}
        }},
        { "constant_score": {
          "boost":   2
          "query": { "match": { "features": "pool" }}
        }}
      ]
    }
  }
}
------------------------------

Really, though, each of these features should be treated like a filter.  A
vacation home either has the feature or it doesn't--a filter seems like it
would be a natural fit.  On top of that, if we use filters, we can
benefit from filter caching.

The problem is this: filters don't score. What we need is a way of bridging
the gap between filters and queries. The `function_score` query does this
and a whole lot more.


