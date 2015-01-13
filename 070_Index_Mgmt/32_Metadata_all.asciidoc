[[all-field]]
==== Metadata: _all Field

In <<search-lite>>, we introduced the `_all` field: a special field that
indexes the ((("metadata, document", "_all field")))((("_all field", sortas="all field")))values from all other fields as one big string. The `query_string`
query clause (and searches performed as `?q=john`) defaults to searching in
the `_all` field if no other field is specified.

The `_all` field is useful during the exploratory phase of a new application,
while you are still unsure about the final structure that your documents will
have. You can throw any query string at it and you have a good chance of
finding the document you're after:

[source,js]
--------------------------------------------------
GET /_search
{
    "match": {
        "_all": "john smith marketing"
    }
}
--------------------------------------------------


As your application evolves and your search requirements become more exacting,
you will find yourself using the `_all` field less and less. The `_all` field
is a shotgun approach to search. By querying individual fields, you have more
flexbility, power, and fine-grained control over which results are considered
to be most relevant.

[NOTE]
====
One of the important factors taken into account by the
<<relevance-intro,relevance algorithm>>
is the length of the field: the shorter the field, the more important. A term
that appears in a short `title` field is likely to be more important than the
same term that appears somewhere in a long `content` field. This distinction
between field lengths disappears in the `_all` field.
====

If you decide that you no longer need the `_all` field, you can disable it
with this mapping:

[source,js]
--------------------------------------------------
PUT /my_index/_mapping/my_type
{
    "my_type": {
        "_all": { "enabled": false }
    }
}
--------------------------------------------------


Inclusion in the `_all` field can be controlled on a field-by-field basis
by using the `include_in_all` setting, ((("include_in_all setting")))which defaults to `true`.  Setting
`include_in_all` on an object (or on the root object) changes the
default for all fields within that object.

You may find that you want to keep the `_all` field around to use
as a catchall full-text field just for specific fields, such as
`title`, `overview`, `summary`, and `tags`. Instead of disabling the `_all`
field completely, disable `include_in_all` for all fields by default,
and enable it only on the fields you choose:

[source,js]
--------------------------------------------------
PUT /my_index/my_type/_mapping
{
    "my_type": {
        "include_in_all": false,
        "properties": {
            "title": {
                "type":           "string",
                "include_in_all": true
            },
            ...
        }
    }
}
--------------------------------------------------


Remember that the `_all` field is just((("analyzers", "configuring for all field"))) an analyzed `string` field.  It
uses the default analyzer to analyze its values, regardless of which
analyzer has been set on the fields where the values originate.  And
like any `string` field, you can configure which analyzer the `_all`
field should use:

[source,js]
--------------------------------------------------
PUT /my_index/my_type/_mapping
{
    "my_type": {
        "_all": { "analyzer": "whitespace" }
    }
}
--------------------------------------------------





