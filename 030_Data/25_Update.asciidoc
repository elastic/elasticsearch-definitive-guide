[[update-doc]]
=== Updating a Whole Document

Documents in Elasticsearch are _immutable_; we cannot change them.((("documents", "updating whole document")))((("updating documents", "whole document"))) Instead, if
we need to update an existing document, we _reindex_ or replace it,((("reindexing")))((("indexing", seealso="reindexing"))) which we
can do using the same `index` API that we have already discussed in
<<index-doc>>.

[source,js]
--------------------------------------------------
PUT /website/blog/123
{
  "title": "My first blog entry",
  "text":  "I am starting to get the hang of this...",
  "date":  "2014/01/02"
}
--------------------------------------------------
// SENSE: 030_Data/25_Reindex_doc.json

In the response, we can see that Elasticsearch has ((("version number (documents)", "incremented when document replaced")))incremented the `_version`
number:

[source,js]
--------------------------------------------------
{
  "_index" :   "website",
  "_type" :    "blog",
  "_id" :      "123",
  "_version" : 2,
  "created":   false <1>
}
--------------------------------------------------
<1> The `created` flag is((("created flag"))) set to `false` because a document with the same
    index, type, and ID already existed.

Internally, Elasticsearch has marked the old document as deleted and added an
entirely new document.((("deleted documents"))) The old version of the document doesn't disappear
immediately, although you won't be able to access it. Elasticsearch cleans up
deleted documents in the background as you continue to index more data.

Later in this chapter, we introduce the `update` API, which can be used to
make <<partial-updates,partial updates to a document>>. This API _appears_ to
change documents in place, but actually Elasticsearch is following exactly the
same process as described previously:

1. Retrieve the JSON from the old document
2. Change it
3. Delete the old document
4. Index a new document

The only difference is that the `update` API achieves this through a single
client request, instead of requiring separate `get` and `index` requests.

