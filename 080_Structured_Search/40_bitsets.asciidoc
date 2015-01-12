[[filter-caching]]
=== All About Caching

Earlier in this chapter (<<_internal_filter_operation>>), we briefly discussed
how filters are calculated.((("structured search", "caching of filter results")))((("caching", "bitsets representing documents matching filters")))((("bitsets, caching of")))((("filters", "bitsets representing documents matching, caching of")))  At their heart is a bitset representing which
documents match the filter. Elasticsearch aggressively caches these bitsets for later use.  Once cached,
these bitsets can be reused _wherever_ the same filter is used, without having
to reevaluate the entire filter again.

These cached bitsets are ``smart'': they are updated incrementally. As you
index new documents, only those new documents need to be added to the existing
bitsets, rather than having to recompute the entire cached filter over and
over. Filters are real-time like the rest of the system; you don't need to
worry about cache expiry.

==== Independent Filter Caching

Each filter is calculated and cached independently, regardless of where it is
used.((("filters", "independent caching of"))) If two different queries use the same filter, the same filter bitset
will be reused.  Likewise, if a single query uses the same filter in multiple
places, only one bitset is calculated and then reused.

Let's look at this example query, which looks for emails that are either of the following:

* In the inbox and have not been read
* _Not_ in the inbox but have been marked as important

[source,js]
--------------------------------------------------
"bool": {
   "should": [
      { "bool": {
            "must": [
               { "term": { "folder": "inbox" }}, <1>
               { "term": { "read": false }}
            ]
      }},
      { "bool": {
            "must_not": {
               "term": { "folder": "inbox" } <1>
            },
            "must": {
               "term": { "important": true }
            }
      }}
   ]
}
--------------------------------------------------
<1> These two filters are identical and will use the same bitset.

Even though one of the inbox clauses is a `must` clause and the other is a
`must_not` clause, the two clauses themselves are identical. This means that
the bitset is calculated once for the first clause that is executed, and then
the cached bitset is used for the other clause.  By the time this query is run
a second time, the inbox filter is already cached and so both clauses will use
the cached bitset.

This ties in nicely with the composability of the query DSL.  It is easy to
move filters around, or reuse the same filter in multiple places within the
same query.  This isn't just convenient to the developer--it has direct
performance benefits.

==== Controlling Caching

Most _leaf filters_&#x2014;those dealing directly with fields like the `term`
filter--are cached, while((("leaf filters, caching of")))((("caching", "of leaf filters, controlling")))((("filters", "controlling caching of"))) compound filters, like the `bool` filter, are not.

[NOTE]
====
Leaf filters have to consult the inverted index on disk, so it makes sense to
cache them. Compound filters, on the other hand, use fast bit logic to combine
the bitsets resulting from their inner clauses, so it is efficient to
recalculate them every time.
====

Certain leaf filters, however, are not cached by default, because it
doesn't make sense to do so:

Script filters::

The results((("script filters, no caching of results"))) from http://www.elasticsearch.org/guide/en/elasticsearch/guide/current/filter-caching.html#_controlling_caching[`script` filters] cannot
be cached because the meaning of the script is opaque to Elasticsearch.

Geo-filters::

The geolocation filters, which((("geolocation filters, no caching of results"))) we cover in more detail in <<geoloc>>, are
usually used to filter results based on the geolocation of a specific user.
Since each user has a unique geolocation, it is unlikely that geo-filters will be reused, so it makes no sense to cache them.

Date ranges::

Date ranges that ((("date ranges", "using now function, no caching of")))((("now function", "date ranges using")))use the `now` function (for example `"now-1h"`), result in values
accurate to the millisecond. Every time the filter is run, `now` returns a new
time. Older filters will never be reused, so caching is disabled by default.
However, when using `now` with rounding (for example, `now/d` rounds to the nearest day),
caching is enabled by default.

Sometimes the default caching strategy is not correct. Perhaps you have a
complicated `bool` expression that is reused several times in the same query.
Or you have a filter on a `date` field that will never be reused.  The default
caching strategy ((("_cache flag", sortas="cache flag")))((("filters", "overriding default caching strategy on")))can be overridden on almost any filter by setting the
`_cache` flag:

[source,js]
--------------------------------------------------
{
    "range" : {
        "timestamp" : {
            "gt" : "2014-01-02 16:15:14" <1>
        },
        "_cache": false <2>
    }
}
--------------------------------------------------
<1> It is unlikely that we will reuse this exact timestamp.
<2> Disable caching of this filter.

Later chapters provide examples of when it can make sense to
override the default caching strategy.
