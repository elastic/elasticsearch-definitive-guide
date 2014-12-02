[[indexed-geo-shapes]]
=== Querying with Indexed Shapes

With shapes that are often used in queries, it can be more convenient to store
them in the index and to refer to them by name in the query.((("indexed shapes, querying with")))((("geo-shapes", "querying with indexed shapes")))  Take our example
of central Amsterdam in the previous example.  We could store it as a document
of type `neighborhood`.

First, we set up the mapping in the same way as we did for `landmark`:

[source,json]
-----------------------
PUT /attractions/_mapping/neighborhood
{
  "properties": {
    "name": {
      "type": "string"
    },
    "location": {
      "type": "geo_shape"
    }
  }
}
-----------------------

Then we can index a shape for central Amsterdam:

[source,json]
-----------------------
PUT /attractions/neighborhood/central_amsterdam
{
  "name" : "Central Amsterdam",
  "location" : {
      "type" : "polygon",
      "coordinates" : [[
        [4.88330,52.38617],
        [4.87463,52.37254],
        [4.87875,52.36369],
        [4.88939,52.35850],
        [4.89840,52.35755],
        [4.91909,52.36217],
        [4.92656,52.36594],
        [4.93368,52.36615],
        [4.93342,52.37275],
        [4.92690,52.37632],
        [4.88330,52.38617]
      ]]
  }
}
-----------------------

After the shape is indexed, we can refer to it by `index`, `type`, and `id` in the
query itself:

[source,json]
-----------------------
GET /attractions/landmark/_search
{
  "query": {
    "geo_shape": {
      "location": {
        "relation": "within",
        "indexed_shape": { <1>
          "index": "attractions",
          "type":  "neighborhood",
          "id":    "central_amsterdam",
          "path":  "location"
        }
      }
    }
  }
}
-----------------------
<1> By specifying `indexed_shape` instead of `shape`, Elasticsearch knows that
    it needs to retrieve the query shape from the specified document and
    `path`.

There is nothing special about the shape for central Amsterdam.  We could
equally use our existing shape for Dam Square in queries.  This query finds
neighborhoods that intersect with Dam Square:

[source,json]
-----------------------
GET /attractions/neighborhood/_search
{
  "query": {
    "geo_shape": {
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
-----------------------



