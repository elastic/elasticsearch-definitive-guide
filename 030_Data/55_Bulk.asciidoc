[[bulk]]
=== Cheaper in bulk

In the same way that `mget` allows us to retrieve multiple documents at once,
the `bulk` API allows us to make multiple `create`, `index`, `update` or
`delete`  requests in a single step. This is particularly useful if you need
to index a data stream such as log events, which can be queued up and indexed
in batches of hundreds or thousands.

The `bulk` request body has the following, slightly unusual, format:

[source,js]
--------------------------------------------------
{ action: { metadata }}\n
{ request body        }\n
{ action: { metadata }}\n
{ request body        }\n
...
--------------------------------------------------

This format is like a _stream_ of valid one-line JSON documents joined
together by newline `"\n"` characters. Two important points to note:

* Every line must end with a newline character `"\n"`, *including the last
  line*. These are used as markers to allow for efficient line separation.

* The lines cannot contain unescaped newline characters, as they would
  interfere with parsing -- that means that the JSON must *not* be
  pretty-printed.

TIP: In <<bulk-format>> we explain why the `bulk` API uses this format.

The _action/metadata_ line specifies *what action* to do to *which document*.

The _action_ must be one of the following:

[horizontal]
`create`:: Create a document only if the document not already exist.
           See <<create-doc>>.
`index`::  Create a new document or replace an existing document.
           See <<index-doc>> and <<update-doc>>.
`update`:: Do a partial update on a document. See <<partial-updates>>.
`delete`:: Delete a document. See <<delete-doc>>.

The _metadata_ should specify the `_index`, `_type` and `_id` of the document
to be indexed, created, updated or deleted.

For instance, a `delete` request could look like this:

[source,js]
--------------------------------------------------
{ "delete": { "_index": "website", "_type": "blog", "_id": "123" }}
--------------------------------------------------

The _request body_ line consists of the document `_source` itself -- the fields
and values that the document contains.  It is required for `index` and
`create` operations, which makes sense: you must supply the document to index.

It is also required for `update` operations and should consist of the same
request body that you would pass to the `update` API: `doc`, `upsert`,
`script` etc. No _request body_ line is required for a delete.

[source,js]
--------------------------------------------------
{ "create":  { "_index": "website", "_type": "blog", "_id": "123" }}
{ "title":    "My first blog post" }
--------------------------------------------------

If no `_id` is specified, then an ID will be auto-generated:

[source,js]
--------------------------------------------------
{ "index": { "_index": "website", "_type": "blog" }}
{ "title":    "My second blog post" }
--------------------------------------------------

To put it all together, a complete `bulk` request has this form:

[source,js]
--------------------------------------------------
POST /_bulk
{ "delete": { "_index": "website", "_type": "blog", "_id": "123" }} <1>
{ "create": { "_index": "website", "_type": "blog", "_id": "123" }}
{ "title":    "My first blog post" }
{ "index":  { "_index": "website", "_type": "blog" }}
{ "title":    "My second blog post" }
{ "update": { "_index": "website", "_type": "blog", "_id": "123", "_retry_on_conflict" : 3} }
{ "doc" : {"title" : "My updated blog post"} } <2>
--------------------------------------------------
// SENSE: 030_Data/55_Bulk.json

<1> Notice how the `delete` _action_ does not have a _request body_, it is
    followed immediately by another _action_.
<2> Remember the final newline character.

The Elasticsearch response contains the `items` array which lists the result of
each request, in the same order as we requested them:

[source,js]
--------------------------------------------------
{
   "took": 4,
   "errors": false, <1>
   "items": [
      {  "delete": {
            "_index":   "website",
            "_type":    "blog",
            "_id":      "123",
            "_version": 2,
            "status":   200,
            "found":    true
      }},
      {  "create": {
            "_index":   "website",
            "_type":    "blog",
            "_id":      "123",
            "_version": 3,
            "status":   201
      }},
      {  "create": {
            "_index":   "website",
            "_type":    "blog",
            "_id":      "EiwfApScQiiy7TIKFxRCTw",
            "_version": 1,
            "status":   201
      }},
      {  "update": {
            "_index":   "website",
            "_type":    "blog",
            "_id":      "123",
            "_version": 4,
            "status":   200
      }}
   ]
}}
--------------------------------------------------
// SENSE: 030_Data/55_Bulk.json

<1> All sub-requests completed successfully.

Each sub-request is executed independently, so the failure of one sub-request
won't affect the success of the others. If any of the requests fail, then the
top-level  `error` flag is set to `true` and the error details will be
reported under the relevant request:


[source,js]
--------------------------------------------------
POST /_bulk
{ "create": { "_index": "website", "_type": "blog", "_id": "123" }}
{ "title":    "Cannot create - it already exists" }
{ "index":  { "_index": "website", "_type": "blog", "_id": "123" }}
{ "title":    "But we can update it" }
--------------------------------------------------
// SENSE: 030_Data/55_Bulk_independent.json

In the response we can see that it failed to `create` document `123` because
it already exists, but the subsequent `index` request, also on document `123`,
succeeded:

[source,js]
--------------------------------------------------
{
   "took": 3,
   "errors": true, <1>
   "items": [
      {  "create": {
            "_index":   "website",
            "_type":    "blog",
            "_id":      "123",
            "status":   409, <2>
            "error":    "DocumentAlreadyExistsException <3>
                        [[website][4] [blog][123]:
                        document already exists]"
      }},
      {  "index": {
            "_index":   "website",
            "_type":    "blog",
            "_id":      "123",
            "_version": 5,
            "status":   200 <4>
      }}
   ]
}
--------------------------------------------------
// SENSE: 030_Data/55_Bulk_independent.json

<1> One or more requests has failed.
<2> The HTTP status code for this request reports `409 CONFLICT`.
<3> The error message explaining why the request failed.
<4> The second request succeeded with an HTTP status code of `200 OK`.

That also means that `bulk` requests are not atomic -- they cannot be used to
implement transactions.  Each request is processed separately, so the success
or failure of one request will not interfere with the others.

==== Don't repeat yourself

Perhaps you are batch indexing logging data into the same `index`, and with the
same `type`. Having to specify the same metadata for every document is a waste.
Instead, just as for the `mget` API, the `bulk` request accepts a default `/_index` or
`/_index/_type` in the URL:

[source,js]
--------------------------------------------------
POST /website/_bulk
{ "index": { "_type": "log" }}
{ "event": "User logged in" }
--------------------------------------------------
// SENSE: 030_Data/55_Bulk_defaults.json


You can still override the `_index` and `_type` in the metadata line, but it
will use the values in the URL as defaults:

[source,js]
--------------------------------------------------
POST /website/log/_bulk
{ "index": {}}
{ "event": "User logged in" }
{ "index": { "_type": "blog" }}
{ "title": "Overriding the default type" }
--------------------------------------------------
// SENSE: 030_Data/55_Bulk_defaults.json

==== How big is too big?

The entire bulk request needs to be loaded into memory by the node which
receives our request, so the bigger the request, the less memory available for
other requests. There is an optimal size of `bulk` request. Above that size,
performance no longer improves and may even drop off.

The optimal size, however, is not a fixed number. It depends entirely on your
hardware, your document size and complexity, and your indexing and search
load.  Fortunately, it is easy to find this _sweetspot_:

Try indexing typical documents in batches of increasing size. When performance
starts to drop off, your batch size is too big. A good place to start is with
batches of between 1,000 and 5,000 documents or, if your documents are very
large, with even smaller batches.

It is often useful to keep an eye on the physical size of your bulk requests.
One thousand 1kB documents is very different than one thousand 1MB documents.
A good bulk size to start playing with is around 5-15MB in size.
