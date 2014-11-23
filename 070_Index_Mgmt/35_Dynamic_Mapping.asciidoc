[[dynamic-mapping]]
=== Dynamic Mapping

When Elasticsearch encounters a previously ((("mapping (types)", "dynamic")))((("dynamic mapping")))unknown field in a document, it
uses <<mapping-intro,_dynamic mapping_>> to determine the datatype for the
field and automatically adds the new field to the type mapping.

Sometimes this is the desired behavior and sometimes it isn't. Perhaps
you don't know what fields will be added to your documents later,
but you want them to be indexed automatically.  Perhaps you just want
to ignore them.  Or--especially if you are using Elasticsearch as a
primary data store--perhaps you want unknown fields to throw an exception
to alert you to the problem.

Fortunately, you can control this behavior((("dynamic setting"))) with the `dynamic` setting,
which accepts the following options:

`true`::    
   Add new fields dynamically--the default
   
`false`::   
   Ignore new fields
   
`strict`::  
   Throw an exception if an unknown field is encountered

The `dynamic` setting may be applied to the root object or to any field
of type `object`.  You could set `dynamic` to `strict` by default,
but enable it just for a specific inner object:

[source,js]
--------------------------------------------------
PUT /my_index
{
    "mappings": {
        "my_type": {
            "dynamic":      "strict", <1>
            "properties": {
                "title":  { "type": "string"},
                "stash":  {
                    "type":     "object",
                    "dynamic":  true <2>
                }
            }
        }
    }
}
--------------------------------------------------
// SENSE: 070_Index_Mgmt/35_Dynamic_mapping.json
<1> The `my_type` object will throw an exception if an unknown field
    is encountered.
<2> The `stash` object will create new fields dynamically.


With this mapping, you can add new searchable fields into the `stash` object:

[source,js]
--------------------------------------------------
PUT /my_index/my_type/1
{
    "title":   "This doc adds a new field",
    "stash": { "new_field": "Success!" }
}
--------------------------------------------------
// SENSE: 070_Index_Mgmt/35_Dynamic_mapping.json


But trying to do the same at the top level will fail:

[source,js]
--------------------------------------------------
PUT /my_index/my_type/1
{
    "title":     "This throws a StrictDynamicMappingException",
    "new_field": "Fail!"
}
--------------------------------------------------
// SENSE: 070_Index_Mgmt/35_Dynamic_mapping.json


NOTE: Setting `dynamic` to `false` doesn't alter the contents of the `_source`
field at all. The `_source` will still contain the whole JSON document that
you indexed.  However, any unknown fields will not be added to the mapping and
will not be searchable.
