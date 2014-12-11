
== Sorting Multivalue Buckets

Multivalue buckets--the `terms`, `histogram`, and ++date_histogram++&#x2014;dynamically produce many buckets.((("sorting", "of multivalue buckets")))((("buckets", "multivalue, sorting")))((("aggregations", "sorting multivalue buckets")))  How does Elasticsearch decide the order that
these buckets are presented to the user?

By default, buckets are ordered by `doc_count` in((("doc_count", "buckets ordered by"))) descending order.  This is a
good default because often we want to find the documents that maximize some
criteria: price, population, frequency. But sometimes you'll want to modify this sort order, and there are a few ways to
do it, depending on the bucket.

=== Intrinsic Sorts

These sort modes are _intrinsic_ to the bucket: they operate on data that bucket((("sorting", "of multivalue buckets", "intrinsic sorts")))
generates, such as `doc_count`.((("buckets", "multivalue, sorting", "intrinsic sorts")))  They share the same syntax but differ slightly
depending on the bucket being used.

Let's perform a `terms` aggregation but sort by `doc_count`, in ascending order:

[source,js]
--------------------------------------------------
GET /cars/transactions/_search?search_type=count
{
    "aggs" : {
        "colors" : {
            "terms" : {
              "field" : "color",
              "order": {
                "_count" : "asc" <1>
              }
            }
        }
    }
}
--------------------------------------------------
// SENSE: 300_Aggregations/50_sorting_ordering.json
<1> Using the `_count` keyword, we can sort by `doc_count`, in ascending order.

We introduce an +order+ object((("order parameter (aggregations)"))) into the aggregation, which allows us to sort on
one of several values:

`_count`::
Sort by document count.  Works with `terms`, `histogram`, `date_histogram`.

`_term`::
Sort by the string value of a term alphabetically.  Works only with `terms`.

`_key`::
Sort by the numeric value of each bucket's key (conceptually similar to `_term`).
Works only with `histogram` and `date_histogram`.

=== Sorting by a Metric

Often, you'll find yourself wanting to sort based on a metric's calculated value.((("buckets", "multivalue, sorting", "by a metric")))((("metrics", "sorting multivalue buckets by")))((("sorting", "of multivalue buckets", "sorting by a metric")))
For our car sales analytics dashboard, we may want to build a bar chart of
sales by car color, but order the bars by the average price, ascending.

We can do this by adding a metric to our bucket, and then referencing that
metric from the +order+ parameter:

[source,js]
--------------------------------------------------
GET /cars/transactions/_search?search_type=count
{
    "aggs" : {
        "colors" : {
            "terms" : {
              "field" : "color",
              "order": {
                "avg_price" : "asc" <2>
              }
            },
            "aggs": {
                "avg_price": {
                    "avg": {"field": "price"} <1>
                }
            }
        }
    }
}
--------------------------------------------------
// SENSE: 300_Aggregations/50_sorting_ordering.json
<1> The average price is calculated for each bucket.
<2> Then the buckets are ordered by the calculated average in ascending order.

This lets you override the sort order with any metric, simply by referencing
the name of the metric.  Some metrics, however, emit multiple values.  The
`extended_stats` metric is a good example: it provides half a dozen individual
metrics.

If you want to sort on a multivalue metric,((("metrics", "sorting multivalue buckets by", "multivalue metric"))) you just need to use the
dot-path to the metric of interest:

[source,js]
--------------------------------------------------
GET /cars/transactions/_search?search_type=count
{
    "aggs" : {
        "colors" : {
            "terms" : {
              "field" : "color",
              "order": {
                "stats.variance" : "asc" <1>
              }
            },
            "aggs": {
                "stats": {
                    "extended_stats": {"field": "price"}
                }
            }
        }
    }
}
--------------------------------------------------
// SENSE: 300_Aggregations/50_sorting_ordering.json
<1> Using dot notation, we can sort on the metric we are interested in.

In this example we are sorting on the variance of each bucket, so that colors
with the least variance in price will appear before those that have more variance.

=== Sorting Based on "Deep" Metrics

In the prior examples, the metric was a direct child of the bucket.  An average
price was calculated for each term.((("buckets", "multivalue, sorting", "on deeper, nested metrics")))((("metrics", "sorting multivalue buckets by", "deeper, nested metrics")))  It is possible to sort on _deeper_ metrics,
which are grandchildren or great-grandchildren of the bucket--with some limitations.

You can define a path to a deeper, nested metric by using angle brackets (`>`), like
so: `my_bucket>another_bucket>metric`.

The caveat is that each nested bucket in the path must be a _single-value_ bucket.
A `filter` bucket produces((("filter bucket"))) a single bucket:  all documents that match the
filtering criteria.  Multivalue buckets (such as `terms`) generate many
dynamic buckets, which makes it impossible to specify a deterministic path.

Currently, there are only three single-value buckets: `filter`, `global`((("global bucket"))), and `reverse_nested`.  As
a quick example, let's build a histogram of car prices, but order the buckets
by the variance in price of red and green (but not blue) cars in each price range:((("histograms", "buckets generated by, sorting on  a deep metric")))

[source,js]
--------------------------------------------------
GET /cars/transactions/_search?search_type=count
{
    "aggs" : {
        "colors" : {
            "histogram" : {
              "field" : "price",
              "interval": 20000,
              "order": {
                "red_green_cars>stats.variance" : "asc" <1>
              }
            },
            "aggs": {
                "red_green_cars": {
                    "filter": { "terms": {"color": ["red", "green"]}}, <2>
                    "aggs": {
                        "stats": {"extended_stats": {"field" : "price"}} <3>
                    }
                }
            }
        }
    }
}
--------------------------------------------------
// SENSE: 300_Aggregations/50_sorting_ordering.json
<1> Sort the buckets generated by the histogram according to the variance of a nested metric.
<2> Because we are using a single-value `filter`, we can use nested sorting.
<3> Sort on the stats generated by this metric.

In this example, you can see that we are accessing a nested metric.  The `stats`
metric is a child of `red_green_cars`, which is in turn a child of `colors`.  To
sort on that metric, we define the path as `red_green_cars>stats.variance`.
This is allowed because the `filter` bucket is a single-value bucket.



