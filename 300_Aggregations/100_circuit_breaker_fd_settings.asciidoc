
=== Limiting Memory Usage

In order for aggregations (or any operation that requires access to field
values) to be fast, ((("aggregations", "limiting memory usage")))access to fielddata must be fast, which is why it is
loaded into memory. ((("fielddata")))((("memory usage", "limiting for aggregations", id="ix_memagg"))) But loading too much data into memory will cause slow
garbage collections as the JVM tries to find extra space in the heap, or
possibly even an OutOfMemory exception.

It may surprise you to find that Elasticsearch does not load into fielddata
just the values for the documents that match your query. It loads the values
for _all documents in your index_, even documents with a different `_type`!

The logic is: if you need access to documents X, Y, and Z for this query, you
will probably need access to other documents in the next query.  It is cheaper
to load all values once, and to _keep them in memory_, than to have to scan
the inverted index on every request.

The JVM heap ((("JVM (Java Virtual Machine)", "heap usage, fielddata and")))is a limited resource that should be used wisely. A number of
mechanisms exist to limit the impact of fielddata on heap usage. These limits
are important because abuse of the heap will cause node instability (thanks to
slow garbage collections) or even node death (with an OutOfMemory exception).

.Choosing a Heap Size
******************************************

There are two rules to apply when setting ((("heap", rules for setting size of")))the Elasticsearch heap size, with
the `$ES_HEAP_SIZE` environment variable:

No more than 50% of available RAM::
Lucene makes good use of the filesystem caches, which are managed by the
kernel.  Without enough filesystem cache space, performance will suffer.

No more than 32 GB:
If the heap is less than 32 GB, the JVM can use compressed pointers, which
saves a lot of memory: 4 bytes per pointer instead of 8 bytes.
+
Increasing the heap from 32 GB to 34 GB would mean that you have much _less_
memory available, because all pointers are taking double the space.  Also,
with bigger heaps, garbage collection becomes more costly and can result in
node instability.

This limit has a direct impact on the amount of memory that can be devoted to fielddata.

******************************************

[[fielddata-size]]
==== Fielddata Size

The `indices.fielddata.cache.size` controls how much heap space is allocated
to fielddata.((("fielddata", "size")))((("aggregations", "limiting memory usage", "fielddata size")))  When you run a query that requires access to new field values,
it will load the values into memory and then try to add them to fielddata. If
the resulting fielddata size  would exceed the specified `size`, other
values would be evicted in order to make space.

By default, this setting is _unbounded_&#x2014;Elasticsearch will never evict data
from fielddata.

This default was chosen deliberately: fielddata is not a transient cache. It
is an in-memory data structure that must be accessible for fast execution, and
it is expensive to build. If you have to reload data for every request,
performance is going to be awful.

A bounded size forces the data structure to evict data.  We will look at when
to set this value, but first a warning:

[WARNING]
=======================================
This setting is a safeguard, not a solution for insufficient memory.

If you don't have enough memory to keep your fielddata resident in memory,
Elasticsearch will constantly have to reload data from disk, and evict other
data to make space. Evictions cause heavy disk I/O  and generate a large
amount of garbage in memory, which must be garbage collected later on.

=======================================

Imagine that you are indexing logs, using a new index every day.  Normally you
are interested in data from only the last day or two.  Although you keep older
indices around, you seldom need to query them.  However, with the default
settings, the fielddata from the old indices is never evicted! fielddata
will just keep on growing until you trip the fielddata circuit breaker (see
<<circuit-breaker>>), which will prevent you from loading any more
fielddata.

At that point, you're stuck. While you can still run queries that access
fielddata from the old indices, you can't load any new values.  Instead, we
should evict old values to make space for the new values.

To prevent this scenario, place an upper limit on the fielddata by adding this
setting to the `config/elasticsearch.yml` file:

[source,yaml]
-----------------------------
indices.fielddata.cache.size:  40% <1>
-----------------------------
<1> Can be set to a percentage of the heap size, or a concrete
    value like `5gb`

With this setting in place, the least recently used fielddata will be evicted
to make space for newly loaded data.((("fielddata", "expiry")))

[WARNING]
====
There is another setting that you may see online:  `indices.fielddata.cache.expire`.

We beg that you _never_ use this setting!  It will likely be deprecated in the
future.

This setting tells Elasticsearch to evict values from fielddata if they are older
than `expire`, whether the values are being used or not.

This is _terrible_ for performance.  Evictions are costly, and this effectively
_schedules_ evictions on purpose, for no real gain.

There isn't a good reason to use this setting; we literally cannot theory-craft
a hypothetically useful situation. It exists only for backward compatibility at
the moment.  We mention the setting in this book only since, sadly, it has been
recommended in various articles on the Internet as a good performance tip.

It is not. Never use it!
====

[[monitoring-fielddata]]
==== Monitoring fielddata

It is important to keep a close watch on how much memory((("fielddata", "monitoring")))((("aggregations", "limiting memory usage", "moitoring fielddata"))) is being used by
fielddata, and whether any data is being evicted.  High eviction counts can
indicate a serious resource issue and a reason for poor performance.

Fielddata usage can be monitored:

* per-index using the http://bit.ly/1BwZ61b[`indices-stats` API]:
+
[source,json]
-------------------------------
GET /_stats/fielddata?fields=*
-------------------------------

* per-node using the http://bit.ly/1586yDn[`nodes-stats` API]:
+
[source,json]
-------------------------------
GET /_nodes/stats/indices/fielddata?fields=*
-------------------------------

* Or even per-index per-node:

[source,json]
-------------------------------
GET /_nodes/stats/indices/fielddata?level=indices&fields=*
-------------------------------

By setting `?fields=*`, the memory usage is broken down for each field.


[[circuit-breaker]]
==== Circuit Breaker

An astute reader might have noticed a problem with the fielddata size settings.
fielddata size is checked _after_ the data is loaded.((("aggregations", "limiting memory usage", "fielddata circuit breaker")))  What happens if a query
arrives that tries to load more into fielddata than available memory?  The
answer is ugly: you would get an OutOfMemoryException.((("OutOfMemoryException")))((("circuit breakers")))

Elasticsearch includes a _fielddata circuit breaker_ that is designed to deal
with this situation.((("fielddata circuit breaker")))  The circuit breaker estimates the memory requirements of
a query by introspecting the fields involved (their type, cardinality, size,
and so forth). It then checks to see whether loading the required fielddata would push
the total fielddata size over the configured percentage of the heap.

If the estimated query size is larger than the limit, the circuit breaker is
_tripped_ and the query will be aborted and return an exception.  This happens
_before_ data is loaded, which means that you won't hit an
OutOfMemoryException.

.Available Circuit Breakers
***************************************

Elasticsearch has a family of circuit breakers, all of which work to ensure
that memory limits are not exceeded:

`indices.breaker.fielddata.limit`::

    The `fielddata` circuit breaker limits the size of fielddata to 60% of the
    heap, by default.

`indices.breaker.request.limit`::

    The `request` circuit breaker estimates the size of structures required to
    complete other parts of a request, such as creating aggregation buckets,
    and limits them to 40% of the heap, by default.

`indices.breaker.total.limit`::

    The `total` circuit breaker wraps the `request` and `fielddata` circuit
    breakers to ensure that the combination of the two doesn't use more than
    70% of the heap by default.

***************************************

The circuit breaker limits can be specified in the `config/elasticsearch.yml`
file, or can be updated dynamically on a live cluster:

[source,js]
----
PUT /_cluster/settings
{
  "persistent" : {
    "indices.breaker.fielddata.limit" : "40%" <1>
  }
}
----
<1> The limit is a percentage of the heap.


It is best to configure the circuit breaker with a relatively conservative
value. Remember that fielddata needs to share the heap with the `request`
circuit breaker, the indexing memory buffer, the filter cache, Lucene data
structures for open indices, and various other transient data structures. For
this reason, it defaults to a fairly conservative 60%.  Overly optimistic
settings can cause potential OOM exceptions, which will take down an entire
node.

On the other hand, an overly conservative value will simply return a query
exception that can be handled by your application.  An exception is better
than a crash. These exceptions should also encourage you to reassess your
query: why _does_ a single query need more than 60% of the heap?

[TIP]
==================================================

In <<fielddata-size>>, we spoke about adding a limit to the size of fielddata,
to ensure that old unused fielddata can be evicted.  The relationship between
`indices.fielddata.cache.size` and `indices.breaker.fielddata.limit` is an
important one.  If the circuit-breaker limit is lower than the cache size, no data will ever be evicted.  In order for it to work properly, the
circuit breaker limit _must_ be higher than the cache size.

==================================================

It is important to note that the circuit breaker compares estimated query size
against the total heap size, _not_ against the actual amount of heap memory
used.  This is done for a variety of technical reasons (for example, the heap may look
full but is actually just garbage waiting to be collected, which is hard to
estimate properly). But as the end user, this means the setting needs to be
conservative, since it is comparing against total heap, not _free_ heap.
((("memory usage", "limiting for aggregations", startref ="ix_memagg")))



