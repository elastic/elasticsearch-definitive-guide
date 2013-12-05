
==== Caching bitsets on a per-segment basis

As if filter bitsets weren't cool enough already, the real magic comes from the
organization of data in Lucene. Remember that each Lucene segment is
immutable - once it is written to disk, it is never changed.

When Elasticsearch builds filter bitsets, they are built on a per-segment basis.
And since segments are immutable, that means the associated filter bitsets are
also immutable.

This has huge performance implications.  Cached filters will remain useful until
the segment is merged.  Once segments grow to a certain size, they rarely merge
with other segments.  This means the filter caches associated with the segment
will have a very long life-time.  Ultimately, a long lifetime
equates to less CPU and disk I/O wasted on evictions and reloading the same data.

Per-segment bitsets also allow fast incremental updates.  In a B-Tree index (like
those used in relational databases), every insert updates the B-Tree.  For very
large indices, this operation becomes very slow.

In Lucene, bitsets are only built for new segments.  Time (and computational
resources) are not wasted on updating the index of older segments.  The segments
are immutable, which means nothing ever needs updating including the bitsets.

Lastly, a nice side-effect of per-segment bitsets is if a particular segment 
doesn't contain any documents that match the filter (a bitset entirely of zeros). 
In these cases, Elasticsearch can completely ignore that segment in the search.

This crash-course section on bitsets should impress upon you the reason to use
filters.  They are fast, fast, fast!  When constructing your queries, spend 
time thinking about which components can be replaced with filters.  Your
query response times will almost always improve when optimized to use filters.

