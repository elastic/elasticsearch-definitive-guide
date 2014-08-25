// I'd limit this list to the metrics and rely on the obvious. You don't need to explain what min/max/avg etc are.  Then say that we'll discusss these more interesting metrics in later chapters: cardinality, percentiles, significant terms. The buckets I'd mention under the relevant section, eg Histo & Range, etc

== Available Buckets and Metrics

There are a number of different buckets and metrics.  The reference documentation
does a great job describing the various parameters and how they affect
the component.  Instead of re-describing them here, we are simply going to
link to the reference docs and provide a brief description.  Skim the list
so that you know what is available, and check the reference docs when you need
exact parameters.

[float]
=== Buckets

    - {ref}search-aggregations-bucket-global-aggregation.html[Global]: includes all documents in your index
    - {ref}search-aggregations-bucket-filter-aggregation.html[Filter]: only includes documents that match
    the filter
    - {ref}search-aggregations-bucket-missing-aggregation.html[Missing]: all documents which _do not_ have
    a particular field
    - {ref}search-aggregations-bucket-terms-aggregation.html[Terms]: generates a new bucket for each unique term
    - {ref}search-aggregations-bucket-range-aggregation.html[Range]: creates arbitrary ranges which documents
    fall into
    - {ref}search-aggregations-bucket-daterange-aggregation.html[Date Range]: similar to Range, but calendar
    aware
    - {ref}search-aggregations-bucket-iprange-aggregation.html[IPV4 Range]: similar to Range, but can handle "IP logic" like CIDR masks, etc
    - {ref}search-aggregations-bucket-geodistance-aggregation.html[Geo Distance]: similar to Range, but operates on
    geo points
    - {ref}search-aggregations-bucket-histogram-aggregation.html[Histogram]: equal-width, dynamic ranges
    - {ref}search-aggregations-bucket-datehistogram-aggregation.html[Date Histogram]: similar to Histogram, but
    calendar aware
    - {ref}search-aggregations-bucket-nested-aggregation.html[Nested]: a special bucket for working with
    nested documents (see <<nested-aggregation>>)
    - {ref}search-aggregations-bucket-geohashgrid-aggregation.html[Geohash Grid]: partitions documents according to
    what geohash grid they fall into (see <<geohash-grid-agg>>)
    - {ref}search-aggregations-metrics-top-hits-aggregation.html[TopHits]: Return the top search results grouped by the value of a field (see <<top-hits>>)

[float]
=== Metrics

    - Individual statistics: {ref}search-aggregations-metrics-min-aggregation.html[Min], {ref}search-aggregations-metrics-max-aggregation.html[Max], {ref}search-aggregations-metrics-avg-aggregation.html[Avg], {ref}search-aggregations-metrics-sum-aggregation.html[Sum]
    - {ref}search-aggregations-metrics-stats-aggregation.html[Stats]: calculates min/mean/max/sum/count of documents in bucket
    - {ref}search-aggregations-metrics-extendedstats-aggregation.html[Extended Stats]: Same as stats, except it also includes variance, std deviation, sum of squares
    - {ref}search-aggregations-metrics-valuecount-aggregation.html[Value Count]: calculates the number of values, which may
    be different from the number of documents (e.g. multi-valued fields)
    - {ref}search-aggregations-metrics-cardinality-aggregation.html[Cardinality]: calculates number of distinct/unique values (see <<cardinality>>)
    - {ref}search-aggregations-metrics-percentile-aggregation.html[Percentiles]: calculates percentiles/quantiles for
    numeric values in a bucket (see <<percentiles>>)
    - {ref}search-aggregations-bucket-significantterms-aggregation.html[Significant Terms]: finds "uncommonly common" terms
    (see <<significant-terms>>)

