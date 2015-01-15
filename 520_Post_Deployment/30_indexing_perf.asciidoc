[[indexing-performance]]
=== Indexing Performance Tips

If you are in an indexing-heavy environment,((("indexing", "performance tips")))((("post-deployment", "indexing performance tips"))) such as indexing infrastructure
logs, you may be willing to sacrifice some search performance for faster indexing
rates.  In these scenarios, searches tend to be relatively rare and performed
by people internal to your organization.  They are willing to wait several
seconds for a search, as opposed to a consumer facing a search that must
return in milliseconds.

Because of this unique position, certain trade-offs can be made
that will increase your indexing performance.

.These Tips Apply Only to Elasticsearch 1.3+
****
This book is written for the most recent versions of Elasticsearch, although much
of the content works on older versions.

The tips presented in this section, however, are _explicitly_ for version 1.3+.  There
have been multiple performance improvements and bugs fixed that directly impact
indexing.  In fact, some of these recommendations will _reduce_ performance on
older versions because of the presence of bugs or performance defects.
****

==== Test Performance Scientifically

Performance testing is always difficult, so try to be as scientific as possible
in your approach.((("performance testing")))((("indexing", "performance tips", "performance testing")))  Randomly fiddling with knobs and turning on ingestion is not
a good way to tune performance.  If there are too many _causes_, it is impossible
to determine which one had the best _effect_. A reasonable approach to testing is as follows:

1. Test performance on a single node, with a single shard and no replicas.
2. Record performance under 100% default settings so that you have a baseline to
measure against.
3. Make sure performance tests run for a long time (30+ minutes) so you can
evaluate long-term performance, not short-term spikes or latencies.  Some events
(such as segment merging, and GCs) won't happen right away, so the performance
profile can change over time.
4. Begin making single changes to the baseline defaults.  Test these rigorously,
and if performance improvement is acceptable, keep the setting and move on to the
next one.

==== Using and Sizing Bulk Requests

This should be fairly obvious, but use bulk indexing requests for optimal performance.((("indexing", "performance tips", "bulk requests, using and sizing")))((("bulk API", "using and sizing bulk requests")))
Bulk sizing is dependent on your data, analysis, and cluster configuration, but
a good starting point is 5&#x2013;15 MB per bulk.  Note that this is physical size.
Document count is not a good metric for bulk size.  For example, if you are
indexing 1,000 documents per bulk, keep the following in mind:

- 1,000 documents at 1 KB each is 1 MB.
- 1,000 documents at 100 KB each is 100 MB.

Those are drastically different bulk sizes.  Bulks need to be loaded into memory
at the coordinating node, so it is the physical size of the bulk that is more
important than the document count.

Start with a bulk size around 5&#x2013;15 MB and slowly increase it until you do not
see performance gains anymore.  Then start increasing the concurrency of your
bulk ingestion (multiple threads, and so forth).

Monitor your nodes with Marvel and/or tools such as `iostat`, `top`, and `ps` to see
when resources start to bottleneck.  If you start to receive `EsRejectedExecutionException`,
your cluster can no longer keep up: at least one resource has reached capacity. Either reduce concurrency, provide more of the limited resource (such as switching from spinning disks to SSDs), or add more nodes.

[NOTE]
====
When ingesting data, make sure bulk requests are round-robined across all your
data nodes.  Do not send all requests to a single node, since that single node
will need to store all the bulks in memory while processing.
====

==== Storage

Disks are usually the bottleneck of any modern server.  Elasticsearch heavily uses disks, and the more throughput your disks can handle, the more stable your nodes will be. Here are some tips for optimizing disk I/O:

- Use SSDs.  As mentioned elsewhere, ((("storage")))((("indexing", "performance tips", "storage")))they are superior to spinning media.
- Use RAID 0.  Striped RAID will increase disk I/O, at the obvious expense of
potential failure if a drive dies.  Don't use mirrored or parity RAIDS since
replicas provide that functionality.
- Alternatively, use multiple drives and allow Elasticsearch to stripe data across
them via multiple `path.data` directories.
- Do not use remote-mounted storage, such as NFS or SMB/CIFS.  The latency introduced
here is antithetical to performance.
- If you are on EC2, beware of EBS.  Even the SSD-backed EBS options are often slower
than local instance storage.

[[segments-and-merging]]
==== Segments and Merging

Segment merging is computationally expensive,((("indexing", "performance tips", "segments and merging")))((("merging segments")))((("segments", "merging"))) and can eat up a lot of disk I/O.
Merges are scheduled to operate in the background because they can take a long
time to finish, especially large segments.  This is normally fine, because the
rate of large segment merges is relatively rare.

But sometimes merging falls behind the ingestion rate.  If this happens, Elasticsearch
will automatically throttle indexing requests to a single thread.  This prevents
a _segment explosion_ problem, in which hundreds of segments are generated before
they can be merged. Elasticsearch will log `INFO`-level messages stating `now
throttling indexing` when it detects merging falling behind indexing.

Elasticsearch defaults here are conservative: you don't want search performance
to be impacted by background merging.  But sometimes (especially on SSD, or logging
scenarios), the throttle limit is too low.

The default is 20 MB/s, which is a good setting for spinning disks.  If you have
SSDs, you might consider increasing this to 100&#x2013;200 MB/s.  Test to see what works
for your system:

[source,js]
----
PUT /_cluster/settings
{
    "persistent" : {
        "indices.store.throttle.max_bytes_per_sec" : "100mb"
    }
}
----

If you are doing a bulk import and don't care about search at all, you can disable
merge throttling entirely.  This will allow indexing to run as fast as your
disks will allow:

[source,js]
----
PUT /_cluster/settings
{
    "transient" : {
        "indices.store.throttle.type" : "none" <1>
    }
}
----
<1> Setting the throttle type to `none` disables merge throttling entirely.  When
you are done importing, set it back to `merge` to reenable throttling.

If you are using spinning media instead of SSD, you need to add this to your
`elasticsearch.yml`:

[source,yaml]
----
index.merge.scheduler.max_thread_count: 1
----

Spinning media has a harder time with concurrent I/O, so we need to decrease
the number of threads that can concurrently access the disk per index.  This setting
will allow `max_thread_count + 2` threads to operate on the disk at one time,
so a setting of `1` will allow three threads.

For SSDs, you can ignore this setting.  The default is
`Math.min(3, Runtime.getRuntime().availableProcessors() / 2)`, which works well
for SSD.

Finally, you can increase `index.translog.flush_threshold_size` from the default
200 MB to something larger, such as 1 GB.  This allows larger segments to accumulate
in the translog before a flush occurs.  By letting larger segments build, you
flush less often, and the larger segments merge less often.  All of this adds up
to less disk I/O overhead and better indexing rates.

==== Other

Finally, there are some other considerations to keep in mind:

- If you don't need near real-time accuracy on your search results, consider
dropping the `index.refresh_interval` of((("indexing", "performance tips", "other considerations")))((("refresh_interval setting"))) each index to `30s`.  If you are doing
a large import, you can disable refreshes by setting this value to `-1` for the
duration of the import.  Don't forget to reenable it when you are finished!

- If you are doing a large bulk import, consider disabling replicas by setting
`index.number_of_replicas: 0`.((("replicas, disabling during large bulk imports")))  When documents are replicated, the entire document
is sent to the replica node and the indexing process is repeated verbatim.  This
means each replica will perform the analysis, indexing, and potentially merging
process.
+
In contrast, if you index with zero replicas and then enable replicas when ingestion
is finished, the recovery process is essentially a byte-for-byte network transfer.
This is much more efficient than duplicating the indexing process.

- If you don't have a natural ID for each document, use Elasticsearch's auto-ID
functionality.((("id", "auto-ID functionality of Elasticsearch")))  It is optimized to avoid version lookups, since the autogenerated
ID is unique.

- If you are using your own ID, try to pick an ID that is http://bit.ly/1sDiR5t[friendly to Lucene]. ((("UUIDs (universally unique identifiers)"))) Examples include zero-padded
sequential IDs, UUID-1, and nanotime; these IDs have consistent, sequential
patterns that compress well.  In contrast, IDs such as UUID-4 are essentially
random, which offer poor compression and slow down Lucene.








