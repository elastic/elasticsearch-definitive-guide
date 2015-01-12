=== Most Important Queries and Filters

While Elasticsearch comes with many queries and filters, you will use
just a few frequently. We discuss them in much greater
detail in <<search-in-depth>> but next we give you a quick introduction to
the most important queries and filters.

==== term Filter

The `term` filter is used to filter by((("filters", "important")))((("term filter"))) exact values, be they numbers, dates,
Booleans, or `not_analyzed` exact-value string fields:

[source,js]
--------------------------------------------------
{ "term": { "age":    26           }}
{ "term": { "date":   "2014-09-01" }}
{ "term": { "public": true         }}
{ "term": { "tag":    "full_text"  }}
--------------------------------------------------
// SENSE: 054_Query_DSL/70_Term_filter.json

==== terms Filter

The `terms` filter is((("terms filter"))) the same as the `term` filter, but allows you
to specify multiple values to match. If the field contains any of
the specified values, the document matches:

[source,js]
--------------------------------------------------
{ "terms": { "tag": [ "search", "full_text", "nosql" ] }}
--------------------------------------------------
// SENSE: 054_Query_DSL/70_Terms_filter.json

==== range Filter

The `range` filter allows you to find((("range filters"))) numbers or dates that fall into
a specified range:

[source,js]
--------------------------------------------------
{
    "range": {
        "age": {
            "gte":  20,
            "lt":   30
        }
    }
}
--------------------------------------------------
// SENSE: 054_Query_DSL/70_Range_filter.json

The operators that it accepts are as follows:

 `gt`::     
   Greater than
   
 `gte`::     
   Greater than or equal to
   
 `lt`::     
   Less than
   
 `lte`::     
   Less than or equal to


==== exists and missing Filters

The `exists` and `missing` filters are ((("exists filter")))((("missing filter")))used to find documents in which the
specified field either has one or more values (`exists`) or doesn't have any
values (`missing`). It is similar in nature to `IS_NULL` (`missing`) and `NOT
IS_NULL` (`exists`)in SQL:

[source,js]
--------------------------------------------------
{
    "exists":   {
        "field":    "title"
    }
}
--------------------------------------------------
// SENSE: 054_Query_DSL/70_Exists_filter.json

These filters are frequently used to apply a condition only if a field is
present, and to apply a different condition if it is missing.

==== bool Filter

The `bool` filter is used ((("bool filter")))((("must clause", "in bool filters")))((("must_not clause", "in bool filters")))((("should clause", "in bool filters")))to combine multiple filter clauses using
Boolean logic. ((("bool filter", "must, must_not, and should clauses"))) It accepts three parameters:

 `must`:: 
   These clauses _must_ match, like `and`.
   
 `must_not`:: 
   These clauses _must not_ match, like `not`.
   
 `should`:: 
   At least one of these clauses must match, like `or`.

Each of these parameters can accept a single filter clause or an array
of filter clauses:

[source,js]
--------------------------------------------------
{
    "bool": {
        "must":     { "term": { "folder": "inbox" }},
        "must_not": { "term": { "tag":    "spam"  }},
        "should": [
                    { "term": { "starred": true   }},
                    { "term": { "unread":  true   }}
        ]
    }
}
--------------------------------------------------
// SENSE: 054_Query_DSL/70_Bool_filter.json


==== match_all Query

The `match_all` query simply((("match_all query")))((("queries", "important"))) matches all documents. It is the default
query that is used if no query has been specified:

[source,js]
--------------------------------------------------
{ "match_all": {}}
--------------------------------------------------
// SENSE: 054_Query_DSL/70_Match_all_query.json


This query is frequently used in combination with a filter--for instance, to
retrieve all emails in the inbox folder. All documents are considered to be
equally relevant, so they all receive a neutral `_score` of `1`.

==== match Query

The `match` query should be the standard((("match query"))) query that you reach for whenever
you want to query for a full-text or exact value in almost any field.

If you run a `match` query against a full-text field, it will analyze
the query string by using the correct analyzer for that field before executing
the search:

[source,js]
--------------------------------------------------
{ "match": { "tweet": "About Search" }}
--------------------------------------------------
// SENSE: 054_Query_DSL/70_Match_query.json

If you use it on a field containing an exact value, ((("exact values", "searching for, match queries and")))such as a number, a date,
a Boolean, or a `not_analyzed` string field, then it will search for that
exact value:

[source,js]
--------------------------------------------------
{ "match": { "age":    26           }}
{ "match": { "date":   "2014-09-01" }}
{ "match": { "public": true         }}
{ "match": { "tag":    "full_text"  }}
--------------------------------------------------
// SENSE: 054_Query_DSL/70_Match_query.json

TIP: For exact-value searches, you probably want to use a filter instead of a
query, as a filter will be cached.

Unlike the query-string search that we showed in <<search-lite>>, the `match`
query does not use a query syntax like `+user_id:2 +tweet:search`. It just
looks for the words that are specified. This means that it is safe to expose
to your users via a search field; you control what fields they can query, and
it is not prone to throwing syntax errors.

==== multi_match Query

The `multi_match` query allows((("multi_match queries"))) to run the same `match` query on multiple
fields:

[source,js]
--------------------------------------------------
{
    "multi_match": {
        "query":    "full text search",
        "fields":   [ "title", "body" ]
    }
}
--------------------------------------------------
// SENSE: 054_Query_DSL/70_Multi_match_query.json

==== bool Query

The `bool` query, like the `bool` filter,((("bool query"))) is used to combine multiple
query clauses. However, there are some differences. Remember that while
filters give binary yes/no answers, queries calculate a relevance score
instead. The `bool` query combines the `_score` from each `must` or
`should` clause that matches.((("bool query", "must, must_not, and should clauses")))((("should clause", "in bool queries")))((("must_not clause", "in bool queries")))((("must clause", "in bool queries"))) This query accepts the following parameters:

`must`::        
   Clauses that _must_ match for the document to be included.

`must_not`::    
   Clauses that _must not_ match for the document to be included.

`should`::      
   If these clauses match, they increase the `_score`;
                otherwise, they have no effect. They are simply used to refine
                the relevance score for each document.

The following query finds documents whose `title` field matches
the query string `how to make millions` and that are not marked
as `spam`.  If any documents are `starred` or are from 2014 onward,
they will rank higher than they would have otherwise. Documents that
match _both_ conditions will rank even higher:

[source,js]
--------------------------------------------------
{
    "bool": {
        "must":     { "match": { "title": "how to make millions" }},
        "must_not": { "match": { "tag":   "spam" }},
        "should": [
            { "match": { "tag": "starred" }},
            { "range": { "date": { "gte": "2014-01-01" }}}
        ]
    }
}
--------------------------------------------------
// SENSE: 054_Query_DSL/70_Bool_query.json

TIP: If there are no `must` clauses, at least one `should` clause has to
match. However, if there is at least one `must` clause, no `should` clauses
are required to match.
