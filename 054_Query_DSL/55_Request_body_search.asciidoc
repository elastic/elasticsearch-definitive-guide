[[full-body-search]]
== Full-Body Search

Search _lite_&#x2014;a <<search-lite,query-string search>>&#x2014;is useful for ad
hoc queries from the command line. ((("searching", "request body search", id="ix_reqbodysearch")))To harness the full power of search,
however, you should use the _request body_ `search` API,((("request body search"))) so called because
most parameters are passed in the HTTP request body instead of in the query
string.

Request body search--henceforth known as _search_&#x2014;not only handles
the query itself, but also allows you to return highlighted snippets from your
results, aggregate analytics across all results or subsets of results, and
return _did-you-mean_ suggestions, which will help guide your users to the
best results quickly.

=== Empty Search

Let's start with the simplest form of ((("request body search", "empty search")))((("empty search")))the `search` API, the empty search,
which returns all documents in all indices:

[source,js]
--------------------------------------------------
GET /_search
{} <1>
--------------------------------------------------
// SENSE: 054_Query_DSL/60_Empty_query.json
<1> This is an empty request body.

Just as with a query-string search, you can search on one, many, or `_all`
indices, and one, many, or all types:

[source,js]
--------------------------------------------------
GET /index_2014*/type1,type2/_search
{}
--------------------------------------------------

And you can use the `from` and `size` parameters((("pagination")))((("size parameter")))((("from parameter"))) for pagination:

[source,js]
--------------------------------------------------
GET /_search
{
  "from": 30,
  "size": 10
}
--------------------------------------------------


[[get_vs_post]]
.A GET Request with a Body?
*************************************************

The HTTP libraries of certain languages (notably JavaScript) don't allow `GET`
requests to have a request body. ((("searching", "using GET and POST HTTP methods for search requests")))((("HTTP methods", "GET and POST, use for search requests")))((("GET method", "no body for GET requests"))) In fact, some users are suprised that `GET`
requests are ever allowed to have a body.

The truth is that http://tools.ietf.org/html/rfc7231#page-24[RFC 7231]&#x2014;the
RFC that deals with HTTP semantics and content--does not define what should
happen to a `GET` request with a body!  As a result, some HTTP servers allow
it, and some--especially caching proxies--don't.

The authors of Elasticsearch prefer using `GET` for a search request because
they feel that it describes the action--retrieving information--better
than the `POST` verb.  However, because `GET` with a request body is not
universally supported, the `search` API also((("POST method", "use for search requests"))) accepts `POST` requests:

[source,js]
--------------------------------------------------
POST /_search
{
  "from": 30,
  "size": 10
}
--------------------------------------------------

The same rule applies to any other `GET` API that requires a request body.

*************************************************

We present aggregations in depth in <<aggregations>>, but for now,
we're going to focus just on the query.

Instead of the cryptic query-string approach, a request body search allows us
to write queries by using the _query domain-specific language_, or query DSL.
((("searching", "request body search", startref ="ix_reqbodysearch")))

