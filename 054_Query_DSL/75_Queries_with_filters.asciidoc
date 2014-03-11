=== Combining queries with filters

Queries can be used in _query context_ and filters can be used
in _filter context_.  Throughout the Elasticsearch API you will see parameters
with `query` or `filter` in the name.  These
expect a single argument containing either a single query or filter clause
respectively. In other words, they establish the
outer ``context'' as _query context_ or _filter context_.

Compound query clauses can wrap other query clauses and compound
filter clauses can wrap other filter clauses. However, it is often
useful to apply a filter to a query or, less frequently, to use a full
text query as a filter.

To do this, there are dedicated query clauses which wrap filter clauses and
vice versa, thus allowing us to switch from one context to another. It is
important to choose the correct combination of query and filter clauses
to achieve your goal in the most efficient way.

[[filtered-query]]
==== Filtering a query

Let's say we have this query:

[source,js]
--------------------------------------------------
{ "match": { "email": "business opportunity" }}
--------------------------------------------------

and we want to combine it with the following `term` filter, which will
only match documents which are in our inbox:

[source,js]
--------------------------------------------------
{ "term": { "folder": "inbox" }}
--------------------------------------------------


The `search` API only accepts a single `query` parameter, so we need
to wrap the query and the filter in another query, called the `filtered`
query:

[source,js]
--------------------------------------------------
{
    "filtered": {
        "query":  { "match": { "email": "business opportunity" }},
        "filter": { "term":  { "folder": "inbox" }}
    }
}
--------------------------------------------------


We can now pass this query to the `query` parameter of the `search` API:

[source,js]
--------------------------------------------------
GET /_search
{
    "query": {
        "filtered": {
            "query":  { "match": { "email": "business opportunity" }},
            "filter": { "term": { "folder": "inbox" }}
        }
    }
}
--------------------------------------------------
// SENSE: 054_Query_DSL/75_Filtered_query.json


==== Just a filter

While in query context, if you need to use a filter without a query, for
instance to match all emails in the inbox, then you can just omit the
query:

[source,js]
--------------------------------------------------
GET /_search
{
    "query": {
        "filtered": {
            "filter":   { "term": { "folder": "inbox" }}
        }
    }
}
--------------------------------------------------
// SENSE: 054_Query_DSL/75_Filtered_query.json


If a query is not specified then it defaults to using the `match_all` query, so
the above query is equivalent to the following:

[source,js]
--------------------------------------------------
GET /_search
{
    "query": {
        "filtered": {
            "query":    { "match_all": {}},
            "filter":   { "term": { "folder": "inbox" }}
        }
    }
}
--------------------------------------------------


==== A query as a filter

Occasionally, you will want to use a query while you are in filter context.
This can be achieved with the `query` filter, which just wraps a query. The
example below shows one way we could exclude emails which look like spam:


[source,js]
--------------------------------------------------
GET /_search
{
    "query": {
        "filtered": {
            "filter":   {
                "bool": {
                    "must":     { "term":  { "folder": "inbox" }},
                    "must_not": {
                        "query": { <1>
                            "match": { "email": "urgent business proposal" }
                        }
                    }
                }
            }
        }
    }
}
--------------------------------------------------
// SENSE: 054_Query_DSL/75_Filtered_query.json
<1> Note the `query` filter, which is allowing us to use the `match` *query*
    inside a `bool` *filter*.


NOTE: You seldom need to use a query as a filter, but we have included it for
completeness' sake.  The only time you may need it is when you need to use
full text matching while in filter context.

