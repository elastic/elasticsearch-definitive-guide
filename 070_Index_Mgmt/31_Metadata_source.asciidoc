[[source-field]]
==== Metadata: _source Field

By default, Elasticsearch ((("metadata, document", "_source field")))((("_source field", sortas="source field")))stores the JSON string representing the
document body in the `_source` field. Like all stored fields, the `_source`
field is compressed before being written to disk.

This is almost always desired functionality because it means the following:

* The full document is available directly from the search results--no need
  for a separate round-trip to fetch the document from another data store.

* Partial `update` requests will not function without the `_source` field.

* When your mapping changes and you need to reindex your data, you can
  do so directly from Elasticsearch instead of having to retrieve all of your
  documents from another (usually slower) data store.

* Individual fields can be extracted from the `_source` field and returned
  in `get` or `search` requests when you don't need to see the whole document.

* It is easier to debug queries, because you can see exactly what each document
  contains, rather than having to guess their contents from a list of IDs.

That said, storing the `_source` field does use disk space.  If none of the
preceding reasons is important to you, you can disable the `_source` field with
the following mapping:

[source,js]
--------------------------------------------------
PUT /my_index
{
    "mappings": {
        "my_type": {
            "_source": {
                "enabled":  false
            }
        }
    }
}
--------------------------------------------------

In a search request, you can ask for only certain fields by specifying the
`_source` parameter in the request body:

[source,js]
--------------------------------------------------
GET /_search
{
    "query":   { "match_all": {}},
    "_source": [ "title", "created" ]
}
--------------------------------------------------
// SENSE: 070_Index_Mgmt/31_Source_field.json

Values for these fields will be extracted from the `_source` field and
returned instead of the full `_source`.

.Stored Fields
****

Besides indexing the values of a field, you ((("stored fields")))((("fields", "stored")))can also choose to `store` the
original field value for later retrieval. Users with a Lucene background use
stored fields to choose which fields they would like to be able to return in
their search results. In fact, the `_source` field is a stored field.

In Elasticsearch, setting individual document fields to be stored is usually a
false optimization. The whole document is already stored as the `_source`
field. It is almost always better to just extract the fields that you need
by using the `_source` parameter.

****

