==== Metadata: Document Identity

There are four metadata fields ((("metadata, document", "identity")))associated with document identity:

`_id`::    
   The string ID of the document
   
`_type`::  
   The type name of the document
   
`_index`:: 
   The index where the document lives
   
`_uid`::   
   The `_type` and `_id` concatenated together as `type#id`

By default, the `_uid` field is((("id field"))) stored (can be retrieved) and
indexed (searchable).  The `_type` field((("type field")))((("index field")))((("uid field"))) is indexed but not stored,
and the `_id` and `_index` fields are neither indexed nor stored, meaning
they don't really exist.

In spite of this, you can query the `_id` field as though it were a real
field.  Elasticsearch uses the `_uid` field to derive the `_id`. Although you
can change the `index` and `store` settings for these fields, you almost
never need to do so.

The `_id` field does have one setting that you may want to use: the `path`
setting tells((("id field", "path setting")))((("path setting, id field"))) Elasticsearch that it should extract the value for the
`_id` from a field within the document itself.

[source,js]
--------------------------------------------------
PUT /my_index
{
    "mappings": {
        "my_type": {
            "_id": {
                "path": "doc_id" <1>
            },
            "properties": {
                "doc_id": {
                    "type":   "string",
                    "index":  "not_analyzed"
                }
            }
        }
    }
}
--------------------------------------------------
// SENSE: 070_Index_Mgmt/33_ID_path.json
<1> Extract the doc `_id` from the `doc_id` field.

Then, when you index a document:

[source,js]
--------------------------------------------------
POST /my_index/my_type
{
    "doc_id": "123"
}
--------------------------------------------------
// SENSE: 070_Index_Mgmt/33_ID_path.json


the `_id` value will be ((("doc_id field")))extracted from the `doc_id` field in the document
body:

[source,js]
--------------------------------------------------
{
    "_index":   "my_index",
    "_type":    "my_type",
    "_id":      "123", <1>
    "_version": 1,
    "created":  true
}
--------------------------------------------------
<1> The `_id` has been extracted correctly.


WARNING: While this is very convenient, be aware that it has a slight
performance impact on `bulk` requests (see <<bulk-format>>). The node handling
the request can no longer use the optimized bulk format to parse just
the metadata line in order to decide which shard should receive the request.
Instead, it has to parse the document body as well.



