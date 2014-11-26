[[geo-memory]]
=== Reducing Memory Usage

Each `lat/lon` pair requires 16 bytes of memory, memory that is in short
supply.((("latitude/longitude pairs", "reducing memory usage by lat/lon pairs")))((("memory usage", "reducing for geo-points")))((("geo-points", "reducing memory usage"))) It needs this much memory in order to provide very accurate results.
But as we have commented before, such exacting precision is seldom required.

You can reduce the amount of memory that is used by switching to a
`compressed` fielddata format and by((("fielddata", "compressed, using for geo-points"))) specifying how precise you need your geo-points to be.  Even reducing precision to `1mm` reduces memory usage by a
third. A more realistic setting of `3m` reduces usage by 62%, and `1km` saves
a massive 75%!

This setting can be changed on a live index with the `update-mapping` API:

[source,json]
----------------------------
POST /attractions/_mapping/restaurant
{
  "location": {
    "type": "geo_point",
    "fielddata": {
      "format":    "compressed",
      "precision": "1km" <1>
    }
  }
}
----------------------------
<1> Each `lat/lon` pair will require only 4 bytes, instead of 16.

Alternatively, you can avoid using memory for geo-points altogether, either by
using the technique described in <<optimize-bounding-box>>, or by storing
geo-points ((("doc values", "storing geo-points as")))as <<doc-values,doc values>>:

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
          "type":       "geo_point",
          "doc_values": true <1>
        }
      }
    }
  }
}
----------------------------
<1> Geo-points will not be loaded into memory, but instead stored on disk.

Mapping a geo-point to use doc values can be done only when the field is first
created. There is a small performance cost in using doc values instead of
fielddata, but with memory in such short supply, it is often worth doing.




