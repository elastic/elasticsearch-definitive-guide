=== Filter Order

The order of filters in a `bool` clause is important for performance.((("structured search", "filter order")))((("filters", "order of"))) More-specific filters should be placed before less-specific filters in order to
exclude as many documents as possible, as early as possible.

If Clause A could match 10 million documents, and Clause B could match
only 100 documents, then Clause B should be placed before Clause A.

Cached filters are very fast, so they should be placed before filters that
are not cacheable.((("caching", "cached filters, order of")))  Imagine that we have an index that contains one month's
worth of log events. However, we're mostly interested only in log events from
the previous hour:

[source,js]
--------------------------------------------------
GET /logs/2014-01/_search
{
    "query" : {
        "filtered" : {
            "filter" : {
                "range" : {
                    "timestamp" : {
                        "gt" : "now-1h"
                    }
                }
            }
        }
    }
}
--------------------------------------------------

This filter is not cached because it uses the `now` function,((("now function", "filters using, caching and"))) the value of
which changes every millisecond. That means that we have to examine one
month's worth of log events every time we run this query!

We could make this much more efficient by combining it with a cached filter:
we can exclude most of the month's data by adding a filter that uses a fixed
point in time, such as midnight last night:

[source,js]
--------------------------------------------------
"bool": {
    "must": [
        { "range" : {
            "timestamp" : {
                "gt" : "now-1h/d" <1>
            }
        }},
        { "range" : {
            "timestamp" : {
                "gt" : "now-1h" <2>
            }
        }}
    ]
}
--------------------------------------------------
<1> This filter is cached because it uses `now` rounded to midnight.

<2> This filter is not cached because it uses `now` _without_ rounding.

The `now-1h/d` clause rounds to the previous midnight and so excludes all documents
created before today.  The resulting bitset is cached because `now` is used
with rounding, which means that it is executed only once a day, when the value
for _midnight-last-night_ changes.  The `now-1h` clause isn't cached because
`now` produces a time accurate to the nearest millisecond. However, thanks to
the first filter, this second filter need only check documents that have been
created since midnight.

The order of these clauses is important. This approach works only because the
_since-midnight_ clause comes before the _last-hour_ clause. If they were the
other  way around, then the _last-hour_ clause would need to examine all
documents in the index, instead of just documents created since midnight.

