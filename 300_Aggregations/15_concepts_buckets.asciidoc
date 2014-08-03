
== High-level concepts

Like the query DSL, aggregations have a _composable_ syntax: independent units
of functionality can be mixed and matched to provide the custom behavior that 
you need. This means that there are only a few basic concepts to learn, but 
nearly limitless combinations of those basic components.

To master aggregations, you only need to understand two main concepts:

_Buckets_:: Collections of documents which meet a criterion.
_Metrics_:: Statistics calculated on the documents in a bucket.

That's it!  Every aggregation is simply a combination of one or more buckets
and zero or more metrics. To translate into rough SQL terms:

[source,sql]
--------------------------------------------------
SELECT COUNT(color) <1>
FROM table 
GROUP BY color <2>
--------------------------------------------------
<1> `COUNT(color)` is equivalent to a metric
<2> `GROUP BY color` is equivalent to a bucket

Buckets are conceptually similar to grouping in SQL, while metrics are similar
to `COUNT()`, `SUM()`, `MAX()`, etc.


Let's dig into both of these concepts and see what they entail.

=== Buckets

A bucket is simply a collection of documents that meet a certain criteria.

- An employee would land in either the "male" or "female" bucket.
- The city of Albany would land in the "New York" state bucket.
- The date "2014-10-28" would land within the "October" bucket.

As aggregations are executed, the values inside each document are evaluated to
determine if they match a bucket's criteria.  If they match, the document is placed
inside the bucket and the aggregation continues.

Buckets can also be nested inside of other buckets, giving you a hierarchy or
conditional partitioning scheme.  For example, "Cincinnati" would be placed inside
the "Ohio" state bucket, and the _entire_ "Ohio" bucket would be placed inside the
"USA" country bucket.

There are a variety of different buckets in Elasticsearch, which allow you to
partition documents in many different ways (by hour, by most popular terms, by
age ranges, by geographical location, etc.).  But fundamentally they all operate 
on the same principle: partitioning documents based on a criteria.

=== Metrics

Buckets allow us to partition documents into useful subsets, but ultimately what
we want is some kind of _metric_ calculated on those documents in each bucket.  
Bucketing is the means to an end - it provides a way to group documents in a way 
that you can calculate interesting metrics.

Most metrics are simple mathematical operations (min, mean, max, sum, etc.)
which are calculated using the document values.  In practical terms, metrics allow
you to calculate quantities such as the average salary, or the maximum sale price,
or the 95th percentile for query latency.

=== Combining the two

An aggregation is a combination of buckets and metrics.  An aggregation may have
a single bucket, or a single metric, or one of each.  It may even have multiple
buckets nested inside of other buckets.

For example, we can partition documents by which country they belong to (a bucket),
then calculate the average salary per country (a metric).

Because buckets can be nested, we can derive a much more complex aggregation:

1. Partition documents by country (bucket)
2. Then partition each country bucket by gender (bucket)
3. Then partition each gender bucket by age ranges (bucket)
4. Finally, calculate the average salary for each age range (metric)

This will give you the average salary per <country, gender, age> combination.  All in
one request and with one pass over the data!





