[[default-mapping]]
=== Default Mapping

Often, all types in an index share similar fields and settings. ((("mapping (types)", "default")))((("default mapping"))) It can be
more convenient to specify these common settings in the `_default_` mapping,
instead of having to repeat yourself every time you create a new type. The
`_default_` mapping acts as a template for new types.  All types created
_after_ the `_default_` mapping will include all of these default settings,
unless explicitly overridden in the type mapping itself.

For instance, we can disable the `_all` field for all types,((("_all field", sortas="all field"))) using the
`_default_` mapping, but enable it just for the `blog` type, as follows:

[source,js]
--------------------------------------------------
PUT /my_index
{
    "mappings": {
        "_default_": {
            "_all": { "enabled":  false }
        },
        "blog": {
            "_all": { "enabled":  true  }
        }
    }
}
--------------------------------------------------
// SENSE: 070_Index_Mgmt/45_Default_mapping.json


The `_default_` mapping can also be a good place to specify index-wide
<<dynamic-templates,dynamic templates>>.
