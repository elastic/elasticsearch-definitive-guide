[[changing-similarities]]
=== Changing Similarities

The similarity algorithm can be set on a per-field basis.((("relevance", "controlling", "changing similarities")))((("similarity algorithms", "changing on a per-field basis")))  It's just a matter
of specifying the chosen algorithm ((("mapping (types)", "specifying similarity algorithm")))in the field's mapping:

[source,json]
------------------------------
PUT /my_index
{
  "mappings": {
    "doc": {
      "properties": {
        "title": {
          "type":       "string",
          "similarity": "BM25" <1>
        },
        "body": {
          "type":       "string",
          "similarity": "default" <2>
        }
      }
  }
}
------------------------------
<1> The `title` field uses BM25 similarity.
<2> The `body` field uses the default similarity (see <<practical-scoring-function>>).

Currently, it is not possible to change the `similarity` mapping for an
existing field.  You would need to reindex your data in order to do that.

==== Configuring BM25

Configuring a similarity is much ((("similarity algorithms", "configuring custom similarities")))((("BM25", "configuring")))like configuring an analyzer. Custom
similarities can be specified when creating an index. For instance:

[source,json]
------------------------------
PUT /my_index
{
  "settings": {
    "similarity": {
      "my_bm25": { <1>
        "type": "BM25",
        "b":    0 <2>
      }
    }
  },
  "mappings": {
    "doc": {
      "properties": {
        "title": {
          "type":       "string",
          "similarity": "my_bm25" <3>
        },
        "body": {
          "type":       "string",
          "similarity": "BM25" <4>
        }
      }
    }
  }
}
------------------------------
<1> Create a custom similarity called `my_bm25`, based on the built-in `BM25` similarity.
<2> Disable field-length normalization. See <<bm25-tunability>>.
<3> Field `title` uses the custom similarity `my_bm25`.
<4> Field `body` uses the built-in similarity `BM25`.

TIP: A custom similarity can be updated by closing the index, updating the index settings,
     and reopening the index.  This allows you to experiment with different configurations
     without having to reindex your documents.





