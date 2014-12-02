[[geo-shape-caching]]
=== Geo-shape Filters and Caching

The `geo_shape` query and filter perform the same function.((("caching", "geo-shape filters and")))((("filters", "geo_shape")))((("geo-shapes", "geo_shape filters, caching and")))  The query simply
acts as a filter: any matching documents receive a relevance `_score` of
`1`. Query results cannot be cached, but filter results can be.

The results are not cached by default.  Just as with geo-points, any
change in the coordinates in a shape are likely to produce a different set of
geohashes, so there is little point in caching filter results.  That said, if
you filter using the same shapes repeatedly, it can be worth caching the
results, by setting `_cache` to `true`:

[source,json]
-----------------------
GET /attractions/neighborhood/_search
{
  "query": {
    "filtered": {
      "filter": {
        "geo_shape": {
          "_cache": true, <1>
          "location": {
            "indexed_shape": {
              "index": "attractions",
              "type":  "landmark",
              "id":    "dam_square",
              "path":  "location"
            }
          }
        }
      }
    }
  }
}
-----------------------
<1> The results of this `geo_shape` filter will be cached.

