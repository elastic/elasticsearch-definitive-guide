[[faking-it]]
=== Faking Index per User with Aliases

To keep our design simple and clean, we would((("scaling", "faking index-per-user with aliases")))((("aliases, index")))((("index aliases"))) like our application to believe that
we have a dedicated index per user--or per forum in our example--even if
the reality is that we are using one big <<shared-index,shared index>>. To do
that, we need some way to hide the `routing` value and the filter on
`forum_id`.

Index aliases allow us to do just that. When you associate an alias with an
index, you can also specify a filter and routing values:

[source,json]
------------------------------
PUT /forums/_alias/baking
{
  "routing": "baking",
  "filter": {
    "term": {
      "forum_id": "baking"
    }
  }
}
------------------------------

Now, we can treat the `baking` alias as if it were its own index.  Documents
indexed into the `baking` alias automatically get the custom routing value
applied:

[source,json]
------------------------------
PUT /baking/post/1 <1>
{
  "forum_id": "baking", <1>
  "title":    "Easy recipe for ginger nuts",
  ...
}
------------------------------
<1> We still need the `forum_id` field for the filter to work, but
    the custom routing value is now implicit.

Queries run against the `baking` alias are run just on the shard associated
with the custom routing value, and the results are automatically filtered by
the filter we specified:

[source,json]
------------------------------
GET /baking/post/_search
{
  "query": {
    "match": {
      "title": "ginger nuts"
    }
  }
}
------------------------------

Multiple aliases can be specified when searching across multiple forums:

[source,json]
------------------------------
GET /baking,recipes/post/_search <1>
{
  "query": {
    "match": {
      "title": "ginger nuts"
    }
  }
}
------------------------------
<1> Both `routing` values are applied, and results can match either filter.

