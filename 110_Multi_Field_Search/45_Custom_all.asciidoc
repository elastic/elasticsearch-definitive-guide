[[custom-all]]
=== Custom _all Fields

In <<all-field>>, we explained that the special `_all` field indexes the values
from all other fields as one big string.((("_all field", sortas="all field")))((("multifield search", "custom _all fields"))) Having all fields indexed into one
field is not terribly flexible, though.  It would be nice to have one custom
`_all` field for the person's name, and another custom `_all` field for the
address.

Elasticsearch provides us with this functionality via the `copy_to` parameter
in a field ((("copy_to parameter")))((("mapping (types)", "copy_to parameter")))mapping:

[source,js]
--------------------------------------------------
PUT /my_index
{
    "mappings": {
        "person": {
            "properties": {
                "first_name": {
                    "type":     "string",
                    "copy_to":  "full_name" <1>
                },
                "last_name": {
                    "type":     "string",
                    "copy_to":  "full_name" <1>
                },
                "full_name": {
                    "type":     "string"
                }
            }
        }
    }
}
--------------------------------------------------
// SENSE: 110_Multi_Field_Search/45_Custom_all.json

<1> The values in the `first_name` and `last_name` fields
    are also copied to the `full_name` field.

With this mapping in place, we can query the `first_name` field for first
names, the `last_name` field for last name, or the `full_name` field for first
and last names.

NOTE: Mappings of the `first_name` and `last_name` fields have no bearing
on how the `full_name` field is indexed. The `full_name` field copies the
string values from the other two fields, then indexes them according to the
mapping of the `full_name` field only.

