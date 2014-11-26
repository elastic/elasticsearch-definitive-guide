[[geo-caching]]
=== Caching geo-filters

The results of geo-filters are not cached by default,((("caching", "of geo-filters")))((("filters", "caching geo-filters")))((("geo-filters, caching"))) for two reasons:

* Geo-filters are usually used to find entities that are near to a user's
    current location. The problem is that users move, and no two users
    are in exactly the same location.  A cached filter would have little
    chance of being reused.

* Filters are cached as bitsets that represent all documents in a
    <<dynamic-indices,segment>>.  Imagine that our query excludes all
    documents but one in a particular segment.  An uncached geo-filter just
    needs to check the one remaining document, but a cached geo-filter would
    need to check all of the documents in the segment.

That said, caching can be used to good effect with geo-filters.  Imagine that
your index contains restaurants from all over the United States. A user in New
York is not interested in restaurants in San Francisco.  We can treat New York
as a _hot spot_ and draw a big bounding box around the city and neighboring
areas.

This `geo_bounding_box` filter can be cached and((("geo_bounding_box filter", "caching and reusing"))) reused whenever we have a
user within the city limits of New York.  It will exclude all restaurants
from the rest of the country. We can then use an uncached, more specific
`geo_bounding_box` or `geo_distance` filter((("geo_distance filter"))) to narrow the remaining results to those that are close to the user:

[source,json]
---------------------
GET /attractions/restaurant/_search
{
  "query": {
    "filtered": {
      "filter": {
        "bool": {
          "must": [
            {
              "geo_bounding_box": {
                "type": "indexed",
                "_cache": true, <1>
                "location": {
                  "top_left": {
                    "lat":  40,8,
                    "lon": -74.1
                  },
                  "bottom_right": {
                    "lat":  40.4,
                    "lon": -73.7
                  }
                }
              }
            },
            {
              "geo_distance": { <2>
                "distance": "1km",
                "location": {
                  "lat":  40.715,
                  "lon": -73.988
                }
              }
            }
          ]
        }
      }
    }
  }
}
---------------------
<1> The cached bounding box filter reduces all results down to those in the
    greater New York area.
<2> The more costly `geo_distance` filter narrows the results to those
    within 1km of the user.


