[[index-doc]]
=== Indexing a document

Documents are _indexed_ -- stored and made searchable -- using the `index`
API. But first, we need to decide where the document  lives.  As we just
discussed, a document's `_index`, `_type` and `_id` uniquely identify the
document.  We can either provide our own `_id` value or let the `index` API
generate one for us.


==== Using our own ID

If your document has a natural identifier (e.g. a `user_account` field
or some other value that identifies the document), then you should provide
your own `_id`, using this form of the `index` API:

[source,js]
--------------------------------------------------
PUT /{index}/{type}/{id}
{
  "field": "value",
  ...
}
--------------------------------------------------

For example, if our index is called `"website"`, our type is called `"blog"`
and we choose the ID `"123"`, then the index request looks like this:

[source,js]
--------------------------------------------------
PUT /website/blog/123
{
  "title": "My first blog entry",
  "text":  "Just trying this out...",
  "date":  "2014/01/01"
}
--------------------------------------------------
// SENSE: 030_Data/10_Create_doc_123.json

Elasticsearch responds with:

[source,js]
--------------------------------------------------
{
   "_index":    "website",
   "_type":     "blog",
   "_id":       "123",
   "_version":  1,
   "created":   true
}
--------------------------------------------------


The response indicates that the indexing request has been successfully created
and includes the `_index`, `_type` and `_id` metadata, and a new element:
`_version`.

Every document in Elasticsearch has a version number. Every time a change is
made to a document (including deleting it), the `_version` number is
incremented.  In <<version-control>> we will discuss how to use the `_version`
number to ensure that one part of your application doesn't overwrite changes
made by another part.

==== Auto-generating IDs

If our data doesn't have a natural ID, we can let Elasticsearch autogenerate
one for us.  The structure of the request changes: instead of using the `PUT`
verb -- ``store this document at this URL'' -- we use the `POST` verb --
``store this document *under* this URL''.

The URL now contains just the `_index` and the `_type`:

[source,js]
--------------------------------------------------
POST /website/blog/
{
  "title": "My second blog entry",
  "text":  "Still trying this out...",
  "date":  "2014/01/01"
}
--------------------------------------------------
// SENSE: 030_Data/10_Create_doc_auto_ID.json

The response is similar to what we saw before, except that the `_id`
field has been generated for us:

[source,js]
--------------------------------------------------
{
   "_index":    "website",
   "_type":     "blog",
   "_id":       "wM0OSFhDQXGZAWDf0-drSA",
   "_version":  1,
   "created":   true
}
--------------------------------------------------

Auto-generated IDs are 22 character long, URL-safe, Base64-encoded string
_universally unique identifiers_, or http://en.wikipedia.org/wiki/Uuid[UUIDs].




