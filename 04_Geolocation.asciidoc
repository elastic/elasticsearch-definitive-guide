ifndef::es_build[= placeholder4]

[[geoloc]]
= Geolocation

[partintro]
--
Gone are the days when we wander around a city with paper maps. Thanks to
smartphones, we now know exactly ((("geolocation")))where we are all the time, and we expect
websites to use that information.  I'm not interested in restaurants in
Greater London--I want to know about restaurants within a 5-minute walk of my
current location.

But geolocation is only one part of the puzzle.  The beauty of Elasticsearch
is that it allows you to combine geolocation with full-text search, structured
search, and analytics.

For instance: show me restaurants that mention _vitello tonnato_, are within a 5-minute walk, and are open at 11 p.m., and then rank them by a combination of user
rating, distance, and price. Another example: show me a map of vacation rental
properties available in August throughout the city, and calculate the average
price per zone.

Elasticsearch offers two ways of ((("Elasticsearch", "representing geolocations")))representing geolocations: latitude-longitude
points using the `geo_point` field type,((("geo_point field type"))) and complex shapes defined in
http://en.wikipedia.org/wiki/GeoJSON[GeoJSON], using the `geo_shape` field
type.((("geo_shape field type")))

_Geo-points_ allow you to find points within a certain distance of another
point, to calculate distances between two points for sorting or relevance
scoring, or to aggregate into a grid to display on a map.  _Geo-shapes_, on the
other hand, are used purely for filtering.  They can be used to decide whether
two shapes overlap, or whether one shape completely contains other
shapes.

--

include::310_Geopoints.asciidoc[]

include::320_Geohashes.asciidoc[]

include::330_Geo_aggs.asciidoc[]

include::340_Geoshapes.asciidoc[]



