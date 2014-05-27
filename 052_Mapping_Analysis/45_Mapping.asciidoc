[[mapping-intro]]
=== Mapping

As explained in <<data-in-data-out>>, each document in an index has a _type_.
Every type has its own _mapping_ or _schema definition_. A mapping
defines the fields within a type, the datatype for each field,
and how the field should be handled by Elasticsearch. A mapping is also used
to configure metadata associated with the type.

We discuss mappings in detail in <<mapping>>. In this section we're going
to look at just enough to get you started.

[[core-fields]]
==== Core simple field types

Elasticsearch supports the following simple field types:

[horizontal]
String:         ::  `string`
Whole number:   ::  `byte`, `short`, `integer`, `long`
Floating point: ::  `float`, `double`
Boolean:        ::  `boolean`
Date:           ::  `date`

When you index a document which contains a new field -- one previously not
seen -- Elasticsearch will use <<dynamic-mapping,_dynamic mapping_>> to try
to guess the field type from the basic datatypes available in JSON,
using the following rules:

[horizontal]
*JSON type:*                       ::          *Field type:*

Boolean: `true` or `false`         ::          `"boolean"`

Whole number: `123`                ::          `"long"`

Floating point: `123.45`           ::          `"double"`

String, valid date: `"2014-09-15"` ::          `"date"`

String: `"foo bar"`                ::          `"string"`


NOTE: This means that, if you index a number in quotes -- `"123"` it will be
mapped as type `"string"`, not type `"long"`. However, if the field is
already mapped as type `"long"`, then Elasticsearch will try to convert
the string into a long, and throw an exception if it can't.

==== Viewing the mapping

We can view the mapping that Elasticsearch has for one or more types in one or
more indices using the `/_mapping` endpoint. At the <<mapping-analysis,start
of this chapter>> we already retrieved the mapping for type `tweet` in index
`gb`:

[source,js]
--------------------------------------------------
GET /gb/_mapping/tweet
--------------------------------------------------

This shows us the mapping for the fields (called _properties_) that
Elasticsearch generated dynamically from the documents that we indexed:

[source,js]
--------------------------------------------------
{
   "gb": {
      "mappings": {
         "tweet": {
            "properties": {
               "date": {
                  "type": "date",
                  "format": "dateOptionalTime"
               },
               "name": {
                  "type": "string"
               },
               "tweet": {
                  "type": "string"
               },
               "user_id": {
                  "type": "long"
               }
            }
         }
      }
   }
}
--------------------------------------------------

[TIP]
==================================================
Incorrect mappings, such as having an `age` field mapped as type `string`
instead of `integer`, can produce confusing results to your queries.

Instead of assuming that your mapping is correct, check it!
==================================================

[[custom-field-mappings]]
==== Customizing field mappings

The most important attribute of a field is the `type`. For fields
other than `string` fields, you will seldom need to map anything other
than `type`:

[source,js]
--------------------------------------------------
{
    "number_of_clicks": {
        "type": "integer"
    }
}
--------------------------------------------------


Fields of type `"string"` are, by default, considered to contain full text.
That is, their value will be passed through an analyzer before being indexed
and a full text query on the field will pass the query string through an
analyzer before searching.

The two most important mapping attributes for `string` fields are
`index` and `analyzer`.

===== `index`

The `index` attribute controls how the string will be indexed. It
can contain one of three values:

[horizontal]
`analyzed`::        First analyze the string, then index it.  In other words,
                    index this field as full text.

`not_analyzed`::    Index this field, so it is searchable, but index the
                    value exactly as specified. Do not analyze it.

`no`::              Don't index this field at all. This field
                    will not be searchable.

The default value of `index` for a `string` field is `analyzed`.  If we
want to map the field as an exact value, then we need to set it to
`not_analyzed`:

[source,js]
--------------------------------------------------
{
    "tag": {
        "type":     "string",
        "index":    "not_analyzed"
    }
}
--------------------------------------------------


****

The other simple types -- `long`, `double`, `date` etc -- also accept the
`index` parameter, but the only relevant values are `no` and `not_analyzed`,
as their values are never analyzed.

****

===== `analyzer`

For `analyzed` string fields, use the `analyzer` attribute to
specify which analyzer to apply both at search time and at index time. By
default, Elasticsearch uses the `standard` analyzer, but you can change this
by specifying one of the built-in analyzers, such as
`whitespace`, `simple`, or `english`:

[source,js]
--------------------------------------------------
{
    "tweet": {
        "type":     "string",
        "analyzer": "english"
    }
}
--------------------------------------------------


In <<custom-analyzers>> we will show you how to define and use custom analyzers
as well.

[[updating-a-mapping]]
==== Updating a mapping

You can specify the mapping for a type when you first create an index.
Alternatively, you can add the mapping for a new type (or update the mapping
for an existing type) later, using the `/_mapping` endpoint.

[IMPORTANT]
================================================
While you can *add* to an existing mapping, you can't *change* it.  If a field
already exists in the mapping, then it probably means that data from that
field has already been indexed.  If you were to change the field mapping, then
the already indexed data would be wrong and would not be properly searchable.
================================================

We can update a mapping to add a new field, but we can't change an existing
field from `analyzed` to `not_analyzed`.

To demonstrate both ways of specifying mappings, let's first delete the `gb`
index:

[source,sh]
--------------------------------------------------
DELETE /gb
--------------------------------------------------
// SENSE: 052_Mapping_Analysis/45_Mapping.json

Then create a new index, specifying that the `tweet` field should use
the `english` analyzer:

[source,js]
--------------------------------------------------
PUT /gb <1>
{
  "mappings": {
    "tweet" : {
      "properties" : {
        "tweet" : {
          "type" :    "string",
          "analyzer": "english"
        },
        "date" : {
          "type" :   "date"
        },
        "name" : {
          "type" :   "string"
        },
        "user_id" : {
          "type" :   "long"
        }
      }
    }
  }
}
--------------------------------------------------
// SENSE: 052_Mapping_Analysis/45_Mapping.json
<1> This creates the index with the `mappings` specified in the body.

Later on, we decide to add a new `not_analyzed` text field called `tag` to the
`tweet` mapping, using the `_mapping` endpoint:

[source,js]
--------------------------------------------------
PUT /gb/_mapping/tweet
{
  "properties" : {
    "tag" : {
      "type" :    "string",
      "index":    "not_analyzed"
    }
  }
}
--------------------------------------------------
// SENSE: 052_Mapping_Analysis/45_Mapping.json

Note that we didn't need to list all of the existing fields again, as we can't
change them anyway.  Our new field has been merged into the existing mapping.

==== Testing the mapping

You can use the `analyze` API to test the mapping for string fields by
name. Compare the output of these two requests:

[source,js]
--------------------------------------------------
GET /gb/_analyze?field=tweet
Black-cats <1>

GET /gb/_analyze?field=tag
Black-cats <1>
--------------------------------------------------
// SENSE: 052_Mapping_Analysis/45_Mapping.json
<1> The text we want to analyze is passed in the body.

The `tweet` field produces the two terms `"black"` and `"cat"`, while the
`tag` field produces the single term `"Black-cats"`. In other words, our
mapping is working correctly.
