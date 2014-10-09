[[geo-bounding-box]]
=== geo_bounding_box Filter

This is by far the most efficient geo-filter because its calculation is very
simple. ((("geo_bounding_box filter")))((("filtering", "by geo-points", "geo_bounding_box filter"))) You provide it with the `top`, `bottom`, `left`, and `right`
coordinates of a rectangle, and all it does is compare the latitude with the
left and right coordinates, and the longitude with the top and bottom
coordinates:

[source,json]
---------------------
GET /attractions/restaurant/_search
{
  "query": {
    "filtered": {
      "filter": {
        "geo_bounding_box": {
          "location": { <1>
            "top_left": {
              "lat":  40.8,
              "lon": -74.0
            },
            "bottom_right": {
              "lat":  40.7,
              "lon": -73.0
            }
          }
        }
      }
    }
  }
}
---------------------
<1> These coordinates can also be specified as `bottom_left` and `top_right`.

[[optimize-bounding-box]]
==== Optimizing Bounding Boxes

The `geo_bounding_box` is the one geo-filter that doesn't require all
geo-points to be loaded into memory.((("geo_bounding_box filter", "optimization")))  Because all it has to do is check
whether the `lat` and `lon` values fall within the specified ranges, it can
use the inverted index to do a ((("range filters")))glorified `range` filter.

To use this optimization, the `geo_point` field ((("latitude/longitude pairs", "geo-point fields mapped to index lat/lon values separately")))must be mapped to
index the `lat` and `lon` values separately:

[source,json]
-----------------------
PUT /attractions
{
  "mappings": {
    "restaurant": {
      "properties": {
        "name": {
          "type": "string"
        },
        "location": {
          "type":    "geo_point",
          "lat_lon": true <1>
        }
      }
    }
  }
}
-----------------------
<1> The `location.lat` and `location.lon` fields will be indexed separately.
    These fields can be used for searching, but their values cannot be retrieved.

Now, when we run our query, we have to tell Elasticsearch to use the indexed
`lat` and `lon` values:

[source,json]
---------------------
GET /attractions/restaurant/_search
{
  "query": {
    "filtered": {
      "filter": {
        "geo_bounding_box": {
          "type":    "indexed", <1>
          "location": {
            "top_left": {
              "lat":  40.8,
              "lon": -74.0
            },
            "bottom_right": {
              "lat":  40.7,
              "lon":  -73.0
            }
          }
        }
      }
    }
  }
}
---------------------
<1> Setting the `type` parameter to `indexed` (instead of the default
    `memory`) tells Elasticsearch to use the inverted index for this filter.

CAUTION: While a `geo_point` field can contain multiple geo-points, the
`lat_lon` optimization can be used only on fields that contain a single
geo-point.

