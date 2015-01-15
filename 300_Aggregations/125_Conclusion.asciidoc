
== Closing Thoughts

This section covered a lot of ground, and a lot of deeply technical issues.
Aggregations bring a power and flexibility to Elasticsearch that is hard to 
overstate. The ability to nest buckets and metrics, to quickly approximate
cardinality and percentiles, to find statistical anomalies in your data, all 
while operating on near-real-time data and in parallel to full-text search--these are game-changers to many organizations.

It is a feature that, once you start using it, you'll find dozens
of other candidate uses.  Real-time reporting and analytics is central to many
 organizations (be it over business intelligence or server logs).

But with great power comes great responsibility, and for Elasticsearch that often
means proper memory stewardship. Memory is often the limiting factor in 
Elasticsearch deployments, particularly those that heavily utilize aggregations.  
Because aggregation data is loaded to fielddata--and this is an in-memory data 
structure--managing ((("aggregations", "managing efficient memory usage")))efficient memory usage is important.

The management of this memory can take several forms, depending on your
particular use-case:

- At a data level, by making sure you analyze (or `not_analyze`) your data appropriately
so that it is memory-friendly
- During indexing, by configuring heavy fields to use disk-based doc values instead
of in-memory fielddata
- At search time, by utilizing approximate aggregations and data filtering
- At a node level, by setting hard memory and dynamic circuit-breaker limits
- At an operations level, by monitoring memory usage and controlling slow garbage-collection cycles, potentially by adding more nodes to the cluster

Most deployments will use one or more of the preceding methods.  The exact combination
is highly dependent on your particular environment.  Some organizations need
blisteringly fast responses and opt to simply add more nodes.  Other organizations
are limited by budget and choose doc values and approximate aggregations.

Whatever the path you take, it is important to assess the available options and
create both a short- and long-term plan.  Decide how your memory situation exists
today and what (if anything) needs to be done.  Then decide what will happen in
six months or one year as your data grows. What methods will you use to continue
scaling?

It is better to plan out these life cycles of your cluster ahead of time, rather
than panicking at 3 a.m. because your cluster is at 90% heap utilization.
