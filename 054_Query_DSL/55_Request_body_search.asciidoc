[[full-body-search]]
== Full body search

Search _lite_ -- <<search-lite,query string search>> --  is useful for _ad
hoc_ queries from the command line. To harness the full power of search,
however, you should use the _request body_ `search` API, so called because
most parameters are passed in the JSON request body instead of in the query
string.

Request body search -- henceforth known just as ``search'' -- not only handles
the query itself, but also allows you to return highlighted snippets from your
results, aggregate analytics across all results or subsets of results, and
return _did-you-mean?_ suggestions, which will help guide your users to the
best results quickly.

=== Empty search

Let's start with the simplest form of the `search` API, the empty search,
which returns all documents in all indices.

[source,js]
--------------------------------------------------
GET /_search
{} <1>
--------------------------------------------------
// SENSE: 054_Query_DSL/60_Empty_query.json
<1> This is an empty request body.

Just as with query-string search, you can search on one, many or `_all`
indices, and one, many or all types:

[source,js]
--------------------------------------------------
GET /index_2014*/type1,type2/_search
{}
--------------------------------------------------

And you can use the `from` and `size` parameters for pagination:

[source,js]
--------------------------------------------------
GET /_search
{
  "from": 30,
  "size": 10
}
--------------------------------------------------


.A `GET` request with a body?
*************************************************

The HTTP libraries of certain languages (notably Javascript) don't allow `GET`
requests to have a request body.  In fact, some users are suprised that `GET`
requests are ever allowed to have a body.

The truth is that http://tools.ietf.org/html/rfc7231#page-24[RFC 7231] -- the
RFC which deals with HTTP semantics and content -- does not define what should
happen to a `GET` request with a body!  As a result, some HTTP servers allow
it, and some -- especially caching proxies -- don't.

The authors of Elasticsearch prefer using `GET` for a search request because
they feel that it describes the action -- retrieving information -- better
than the `POST` verb.  However, because `GET` with a request body is not
universally supported, the `search` API also accepts `POST` requests:

[source,js]
--------------------------------------------------
POST /_search
{
  "from": 30,
  "size": 10
}
--------------------------------------------------

The same rule applies to any other `GET` API which requires a request body.

*************************************************

We will talk about aggregations in depth in <<aggregations>>, but for now,
we're going to focus just on the query.

Instead of the cryptic query-string approach, request body search allows us
to write queries using the _Query Domain Specific Language_, or Query DSL.

