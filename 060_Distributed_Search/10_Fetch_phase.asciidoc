=== Fetch Phase

The query phase identifies which documents satisfy((("distributed search execution", "fetch phase")))((("fetch phase of distributed search"))) the search request, but we
still need to retrieve the documents themselves. This is the job of the fetch
phase, shown in <<img-distrib-fetch>>.

[[img-distrib-fetch]]
.Fetch phase of distributed search
image::images/elas_0902.png["Fetch Phase of distributed search"]

The distributed phase consists of the following steps:

1. The coordinating node identifies which documents need to be fetched and
   issues a multi `GET` request to the relevant shards.

2. Each shard loads the documents and _enriches_ them, if required, and then
   returns the documents to the coordinating node.

3. Once all documents have been fetched, the coordinating node returns the
   results to the client.

The coordinating node first decides which documents _actually_ need to be
fetched. For instance, if our query specified `{ "from": 90, "size": 10 }`,
the first 90 results would be discarded and only the next 10 results would
need to be retrieved. These documents may come from one, some, or all of the
shards involved in the original search request.

The coordinating node builds a <<distrib-multi-doc,multi-get request>> for
each shard that holds a pertinent document and sends the request to the same
shard copy that handled the query phase.

The shard loads the document bodies--the `_source` field--and, if
requested, enriches the results with metadata and
<<highlighting-intro,search snippet highlighting>>.
Once the coordinating node receives all results, it assembles them into a
single response that it returns to the client.

.Deep Pagination
****

The query-then-fetch process supports pagination with the `from` and `size`
parameters, but _within limits_. ((("size parameter")))((("from parameter")))((("pagination", "supported by query-then-fetch process")))((("deep paging, problems with"))) Remember that each shard must build a priority
queue of length `from + size`, all of which need to be passed back to
the coordinating node. And the coordinating node needs to sort through
`number_of_shards * (from + size)` documents in order to find the correct
`size` documents.

Depending on the size of your documents, the number of shards, and the
hardware you are using, paging 10,000 to 50,000 results (1,000 to 5,000 pages)
deep should be perfectly doable. But with big-enough `from` values, the
sorting process can become very heavy indeed, using vast amounts of CPU,
memory, and bandwidth.  For this reason, we strongly advise against deep paging.

In practice, ``deep pagers'' are seldom human anyway.  A human will stop
paging after two  or three pages and will change the search criteria. The
culprits are usually bots or web spiders that tirelessly keep fetching page
after page until your servers crumble at the knees.

If you _do_ need to fetch large numbers of docs from your cluster, you can
do so efficiently by disabling sorting with the `scan` search type,
which we discuss <<scan-scroll,later in this chapter>>.

****
