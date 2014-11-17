[[scan-scroll]]
=== scan and scroll

The `scan` search type and the `scroll` API((("scroll API", "scan and scroll"))) are used together to retrieve
large numbers of documents from Elasticsearch efficiently, without paying the
penalty of deep pagination.

`scroll`::
+
--
A _scrolled search_ allows us to((("scrolled search"))) do an initial search and to keep pulling
batches of results from Elasticsearch until there are no more results left.
It's a bit like a _cursor_ in ((("cursors")))a traditional database.

A scrolled search takes a snapshot in time. It doesn't see any changes that
are made to the index after the initial search request has been made. It does
this by keeping the old data files around, so that it can preserve its ``view''
on what the index looked like at the time it started.

--

`scan`::

The costly part of deep pagination is the global sorting of results, but if we
disable sorting, then we can return all documents quite cheaply. To do this, we
use the `scan` search type.((("scan search type"))) Scan instructs Elasticsearch to do no sorting, but
to just return the next batch of results from every shard that still has
results to return.

To use _scan-and-scroll_, we execute a search((("scan-and-scroll"))) request setting `search_type` to((("search_type", "scan and scroll")))
`scan`, and passing a `scroll` parameter telling Elasticsearch how long it
should keep the scroll open:

[source,js]
--------------------------------------------------
GET /old_index/_search?search_type=scan&scroll=1m <1>
{
    "query": { "match_all": {}},
    "size":  1000
}
--------------------------------------------------
<1> Keep the scroll open for 1 minute.

The response to this request doesn't include any hits, but does include a
`_scroll_id`, which is a long Base-64 encoded((("scroll_id"))) string. Now we can pass the
`_scroll_id` to the `_search/scroll` endpoint to retrieve the first batch of
results:

[source,js]
--------------------------------------------------
GET /_search/scroll?scroll=1m <1>
c2Nhbjs1OzExODpRNV9aY1VyUVM4U0NMd2pjWlJ3YWlBOzExOTpRNV9aY1VyUVM4U0 <2>
NMd2pjWlJ3YWlBOzExNjpRNV9aY1VyUVM4U0NMd2pjWlJ3YWlBOzExNzpRNV9aY1Vy
UVM4U0NMd2pjWlJ3YWlBOzEyMDpRNV9aY1VyUVM4U0NMd2pjWlJ3YWlBOzE7dG90YW
xfaGl0czoxOw==
--------------------------------------------------
<1> Keep the scroll open for another minute.
<2> The `_scroll_id` can be passed in the body, in the URL, or as a
    query parameter.

Note that we again specify `?scroll=1m`.  The scroll expiry time is refreshed
every time we run a scroll request, so it needs to give us only enough time
to process the current batch of results, not all of the documents that match
the query.

The response to this scroll request includes the first batch of results.
Although we specified a `size` of 1,000, we get back many more
documents.((("size parameter", "in scanning")))  When scanning, the `size` is applied to each shard, so you will
get back a maximum of `size * number_of_primary_shards` documents in each
batch.

NOTE: The scroll request also returns  a _new_ `_scroll_id`.  Every time
we make the next scroll request, we must pass the `_scroll_id` returned by the
_previous_ scroll request.

When no more hits are returned, we have processed all matching documents.

TIP: Some of the http://www.elasticsearch.org/guide[official Elasticsearch clients]
provide _scan-and-scroll_ helpers that provide an easy wrapper around this
functionality.((("clients", "providing scan-and-scroll helpers")))

