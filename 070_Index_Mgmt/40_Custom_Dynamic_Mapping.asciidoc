[[custom-dynamic-mapping]]
=== Customizing Dynamic Mapping

If you know that you are going to be adding new fields on the fly,
you probably want to leave dynamic mapping enabled.((("dynamic mapping", "custom")))((("mapping (types)", "dynamic", "custom")))  At times, though,
the dynamic mapping ``rules'' can be a bit blunt.  Fortunately, there
are settings that you can use to customize these rules to better
suit your data.

[[date-detection]]
==== date_detection

When Elasticsearch encounters a new string field, it checks to see if the
string contains a recognizable date, like `2014-01-01`.((("date_detection setting")))((("dynamic mapping", "custom", "date_detection setting"))) If it looks
like a date, the field is added as type `date`. Otherwise, it is
added as type `string`.

Sometimes this behavior can lead to problems.  Imagine that you index
a document like this:

[source,js]
--------------------------------------------------
{ "note": "2014-01-01" }
--------------------------------------------------


Assuming that this is the first time that the `note` field has been seen,
it will be added as a `date` field.  But what if the next document looks
like this:

[source,js]
--------------------------------------------------
{ "note": "Logged out" }
--------------------------------------------------


This clearly isn't a date, but it is too late.  The field is already
a date field and so this ``malformed date'' will cause an exception to be
thrown.

Date detection can be turned off by setting `date_detection` to `false`
on the ((("root object", "date_detection setting")))root object:

[source,js]
--------------------------------------------------
PUT /my_index
{
    "mappings": {
        "my_type": {
            "date_detection": false
        }
    }
}
--------------------------------------------------


With this mapping in place, a string will always be a `string`.  If you need
a `date` field, you have to add it manually.

[NOTE]
====
Elasticsearch's idea of which strings look like dates can be altered
with the http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/mapping-root-object-type.html[`dynamic_date_formats` setting].
====

[[dynamic-templates]]
==== dynamic_templates

With `dynamic_templates`, you can take complete control ((("dynamic_templates setting")))((("dynamic mapping", "custom", "dynamic_templates setting")))over the
mapping that is generated for newly detected fields. You
can even apply a different mapping depending on the field name
or datatype.

Each template has a name, which ((("templates", "dynamic_templates setting")))you can use to describe what the template
does, a `mapping` to specify the mapping that should be applied, and
at least one parameter (such as `match`) to define which fields the template
should apply to.

Templates are checked in order; the first template that matches is
applied. For instance, we could specify two templates for `string` fields:

* `es`: Field names ending in `_es` should use the `spanish` analyzer.
* `en`: All others should use the `english` analyzer.

We put the `es` template first, because it is more specific than the
catchall `en` template, which matches all string fields:

[source,js]
--------------------------------------------------
PUT /my_index
{
    "mappings": {
        "my_type": {
            "dynamic_templates": [
                { "es": {
                      "match":              "*_es", <1>
                      "match_mapping_type": "string",
                      "mapping": {
                          "type":           "string",
                          "analyzer":       "spanish"
                      }
                }},
                { "en": {
                      "match":              "*", <2>
                      "match_mapping_type": "string",
                      "mapping": {
                          "type":           "string",
                          "analyzer":       "english"
                      }
                }}
            ]
}}}
--------------------------------------------------
// SENSE: 070_Index_Mgmt/40_Custom_dynamic_mapping.json

<1> Match string fields whose name ends in `_es`.
<2> Match all other string fields.

The `match_mapping_type`  allows ((("match_mapping_type setting")))you to apply the template only
to fields of the specified type, as detected by the standard dynamic
mapping rules, (for example `string` or `long`).

The `match` parameter matches just the field name, and the `path_match`
parameter((("path_map parameter"))) matches the full path to a field in an object, so
the pattern `address.*.name` would match a field like this:

[source,js]
--------------------------------------------------
{
    "address": {
        "city": {
            "name": "New York"
        }
    }
}
--------------------------------------------------


The `unmatch` and `path_unmatch` patterns((("unmatch pattern")))((("path_unmap pattern"))) can be used to exclude fields
that would otherwise match.

More configuration options can be found in the
http://bit.ly/1wdHOzG[reference documentation for the root object].
