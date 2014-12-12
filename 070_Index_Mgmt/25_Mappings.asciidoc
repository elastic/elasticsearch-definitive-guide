[[mapping]]
=== Types and Mappings

A _type_ in Elasticsearch represents a class of similar documents.((("types", "defined"))) A type
consists of a _name_&#x2014;such as `user` or `blogpost`&#x2014;and a _mapping_. The
mapping, ((("mapping (types)")))like a database schema, describes the fields or _properties_ that
documents of that type may have, ((("fields", "datatypes")))the datatype of each field--such as `string`,
`integer`, or `date`&#x2014;and how those fields should be indexed and stored by
Lucene.

In <<document>>, we said that a type is like a table in a relational database.
While this is a useful way to think about types initially, it is worth
explaining in more detail exactly what a type is and how they are implemented
on top of Lucene.

==== How Lucene Sees Documents

A document in Lucene consists of a simple list of field-value pairs.((("documents", "in Lucene"))) A field
must have at least one value, but any field can contain multiple values.
Similarly, a single string value may be converted into multiple values by the
analysis process.  Lucene doesn't care if the values are strings or numbers or
dates--all values are just treated as _opaque bytes_.

When we index a document in Lucene, the values for each field are added to the
inverted index for the associated field.  Optionally, the original values may
also be _stored_ unchanged so that they can be retrieved later.

==== How Types Are Implemented

Elasticsearch types are ((("types", "implementation in Elasticsearch")))implemented on top of this simple foundation. An index
may have several types, each with its own mapping, and documents of any of
these types may be stored in the same index.

Because Lucene has no concept of document types, the type name of each
document is stored with the document in a metadata field called `_type`.((("type field"))) When
we search for documents of a particular type, Elasticsearch simply uses a
filter on the `_type` field to restrict results to documents of that type.

Lucene also has no concept of mappings.((("mapping (types)"))) Mappings are the layer
that Elasticsearch uses to _map_ complex JSON documents into the
simple flat documents that Lucene expects to receive.

For instance, the mapping for the `name` field in the `user` type may declare
that the field is a `string` field, and that its value should be analyzed
by the `whitespace` analyzer before being indexed into the inverted
index called `name`:

[source,js]
--------------------------------------------------
"name": {
    "type":     "string",
    "analyzer": "whitespace"
}
--------------------------------------------------


==== Avoiding Type Gotchas

The fact that documents of different types can be added to the same index
introduces some unexpected((("types", "gotchas, avoiding"))) complications.

Imagine that we have two types in our index: `blog_en` for blog posts in
English, and `blog_es` for blog posts in Spanish.  Both types have a
`title` field, but one type uses the `english` analyzer and
the other type uses the `spanish` analyzer.

The problem is illustrated by the following query:

[source,js]
--------------------------------------------------
GET /_search
{
    "query": {
        "match": {
            "title": "The quick brown fox"
        }
    }
}
--------------------------------------------------


We are searching in the `title` field in both types.  The query string needs
to be analyzed, but which analyzer does it use: `spanish` or `english`? It
will use the analyzer for the first `title` field that it finds, which
will be correct for some docs and incorrect for the others.

We can avoid this problem either by naming the fields differently--for example, `title_en` and `title_es`&#x2014;or by explicitly including the type name in the
field name and querying each field separately:

[source,js]
--------------------------------------------------
GET /_search
{
    "query": {
        "multi_match": { <1>
            "query":    "The quick brown fox",
            "fields": [ "blog_en.title", "blog_es.title" ]
        }
    }
}
--------------------------------------------------
<1> The `multi_match` query runs a `match` query on multiple fields
    and combines the results.

Our new query uses the `english` analyzer for the field `blog_en.title` and
the `spanish` analyzer for the field `blog_es.title`, and combines the results
from both fields into an overall relevance score.

This solution can help when both fields have the same datatype, but consider
what would happen if you indexed these two documents into the same index:

* Type: user

[source,js]
--------------------------------------------------
 { "login": "john_smith" }
--------------------------------------------------

[role="pagebreak-before"]
* Type: event

[source,js]
--------------------------------------------------
 { "login": "2014-06-01" }
--------------------------------------------------

Lucene doesn't care that one field contains a string and the other field
contains a date. It will happily index the byte values from both fields.

However, if we now try to _sort_ on the `event.login` field, Elasticsearch
needs to load the values in the `login` field into memory. As we said in
<<fielddata-intro>>, it loads the values for  _all documents_ in the index
regardless of their type.

It will try to load these values either as a string or as a date, depending on
which `login` field it sees first. This will either produce unexpected results
or fail outright.

TIP: To ensure that you don't run into these conflicts, it is advisable to
ensure that fields with the _same name_ are mapped in the _same way_ in every
type in an index.
