[[delete-doc]]
=== Deleting a Document

The syntax for deleting a document((("documents", "deleting"))) follows the same pattern that we have seen
already, but ((("DELETE method", "deleting documents")))((("HTTP methods", "DELETE")))uses the `DELETE` method :

[source,js]
--------------------------------------------------
DELETE /website/blog/123
--------------------------------------------------
// SENSE: 030_Data/35_Delete_doc.json


If the document is found, Elasticsearch will return an HTTP response code
of `200 OK` and a response body like the following. Note that the `_version`
number has been incremented:

[source,js]
--------------------------------------------------
{
  "found" :    true,
  "_index" :   "website",
  "_type" :    "blog",
  "_id" :      "123",
  "_version" : 3
}
--------------------------------------------------

If the document isn't((("version number (documents)", "incremented for document not found"))) found, we get a `404 Not Found` response code and
a body like this:

[source,js]
--------------------------------------------------
{
  "found" :    false,
  "_index" :   "website",
  "_type" :    "blog",
  "_id" :      "123",
  "_version" : 4
}
--------------------------------------------------

Even though the document doesn't exist (`found` is `false`), the
`_version` number has still been incremented. This is part of the internal
bookkeeping, which ensures that changes are applied in the correct order
across multiple nodes.

NOTE: As already mentioned in <<update-doc>>, deleting a document doesn't
immediately remove the document from disk; it just marks it as deleted.
Elasticsearch will clean up deleted documents in the background as you
continue to index more data.

