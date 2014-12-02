[[geohash-mapping]]
=== Mapping Geohashes

The first step is to decide just how much precision you need.((("geohashes", "mapping")))((("mapping (types)", "geohashes")))  Although you could
index all geo-points with the default full 12 levels of precision, do you
really need to be accurate to within a few centimeters? You can save yourself
a lot of space in the index by reducing your precision requirements to
something more realistic, such as `1km`:((("geohash_precision parameter")))((("geohash_prefix parameter")))

[source,json]
----------------------------
PUT /attractions
{
  "mappings": {
    "restaurant": {
      "properties": {
        "name": {
          "type": "string"
        },
        "location": {
          "type":               "geo_point",
          "geohash_prefix":     true, <1>
          "geohash_precision":  "1km" <2>
        }
      }
    }
  }
}
----------------------------
<1> Setting `geohash_prefix` to `true` tells Elasticsearch to index
    all geohash prefixes, up to the specified precision.
<2> The precision can be specified as an absolute number, representing the
    length of the geohash, or as a distance. A precision of `1km` corresponds
    to a geohash of length `7`.

With this mapping in place, geohash prefixes of lengths 1 to 7 will be indexed,
providing geohashes accurate to about 150 meters.

