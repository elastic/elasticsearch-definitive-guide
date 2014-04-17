[[sorting]]
== Sorting and relevance

By default, results are returned sorted by _relevance_ -- with the most
relevant docs first. Later in this chapter we will explain what we mean by
_relevance_ and how it is calculated, but let's start by looking at the `sort`
parameter and how to use it.

=== Sorting

In order to sort by relevance, we need to represent relevance as a value. In
Elasticsearch  the _relevance score_ is represented by the floating point
number returned in the search results as the `_score`, so the default sort
order is: `_score` descending.

Sometimes, though, you don't have a meaningful relevance score. For instance,
the following query just returns all tweets whose `user_id` field has the
value `1`:

[source,js]
--------------------------------------------------
GET /_search
{
    "query" : {
        "filtered" : {
            "filter" : {
                "term" : {
                    "user_id" : 1
                }
            }
        }
    }
}
--------------------------------------------------

Filters have no bearing on `_score`, and the missing-but-implied `match_all`
query just sets the `_score` to a neutral value of `1` for all documents. In
other words, all documents are considered to be equally relevant.

==== Sorting by field values

In this case, it probably makes sense to sort tweets by recency, with the most
recent tweets first.  We can do this with the `sort` parameter:

[source,js]
--------------------------------------------------
GET /_search
{
    "query" : {
        "filtered" : {
            "filter" : { "term" : { "user_id" : 1 }}
        }
    },
    "sort": { "date": { "order": "desc" }}
}
--------------------------------------------------
// SENSE: 056_Sorting/85_Sort_by_date.json

You will notice two differences in the results:

[source,js]
--------------------------------------------------
"hits" : {
    "total" :           6,
    "max_score" :       null, <1>
    "hits" : [ {
        "_index" :      "us",
        "_type" :       "tweet",
        "_id" :         "14",
        "_score" :      null, <1>
        "_source" :     {
             "date":    "2014-09-24",
             ...
        },
        "sort" :        [ 1411516800000 ] <2>
    },
    ...
}
--------------------------------------------------
<1> The `_score` is not calculated because it is not being used for sorting.
<2> The value of the `date` field, expressed as milliseconds since the epoch,
    is returned in the `sort` values.

The first is that we have a new element in each result called `sort`, which
contains the value(s) that was used for sorting.  In this case, we sorted on
`date` which internally is indexed as _milliseconds-since-the-epoch_. The long
number `1411516800000` is equivalent to the date string `2014-09-24 00:00:00
UTC`.

The second is that the `_score` and `max_score` are both `null`.  Calculating
the `_score` can be quite expensive and usually its only purpose is for
sorting -- we're not sorting by relevance, so it doesn't make sense to keep
track of the `_score`.  If you want the `_score` to be calculated regardless,
then you can set the `track_scores` parameter to `true`.

.Default ordering
****

As a shortcut, you can specify just the name of the field to sort on:

[source,js]
--------------------------------------------------
    "sort": "number_of_children"
--------------------------------------------------

Fields will be sorted in ascending order by default, and
the `_score` value in descending order.

****

==== Multi-level sorting

Perhaps we want to combine the `_score` from a query with the `date`, and
show all matching results sorted first by date, then by relevance:

[source,js]
--------------------------------------------------
GET /_search
{
    "query" : {
        "filtered" : {
            "query":   { "match": { "tweet": "manage text search" }},
            "filter" : { "term" : { "user_id" : 2 }}
        }
    },
    "sort": [
        { "date":   { "order": "desc" }},
        { "_score": { "order": "desc" }}
    ]
}
--------------------------------------------------
// SENSE: 056_Sorting/85_Multilevel_sort.json

Order is important.  Results are sorted by the first criterion first. Only
results whose first `sort` value is identical will then be sorted by the
second criterion, and so on.

Multi-level sorting doesn't have to involve the `_score` -- you could sort
using several different fields, on geo-distance or on a custom value
calculated in a script.

.Sorting and query string search
****
Query string search also supports custom sorting, using the `sort` parameter
in the query string:

[source,js]
--------------------------------------------------
GET /_search?sort=date:desc&sort=_score&q=search
--------------------------------------------------
****

==== Sorting on multi-value fields

When sorting on field with more than one value, remember that the values do
not have any intrinsic order -- a multi-value field is just a bag of values.
Which one do you choose to sort on?

For numbers and dates, you can reduce a multi-value field to a single value
using the `min`, `max`, `avg` or `sum` _sort modes_. For instance, you
could sort on the earliest date in each `dates` field using:

[source,js]
--------------------------------------------------
"sort": {
    "dates": {
        "order": "asc",
        "mode":  "min"
    }
}
--------------------------------------------------




