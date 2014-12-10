[[kagillion-shards]]
=== Kagillion Shards

The first thing that new users do when they learn about
<<overallocation,shard overallocation>> is((("scaling", "shard overallocation", "limiting")))((("shards", "overallocation of", "limiting"))) to say to themselves:

[quote, A new user]
_______________________________
[role="alignmeright"]
I don't know how big this is going to be, and I can't change the index size
later on, so to be on the safe side, I'll just give this index 1,000 shards...

_______________________________

One thousand shards--really? And you don't think that, perhaps, between now
and the time you need to buy _one thousand nodes_, that you may need to
rethink your data model once or twice and have to reindex?

A shard is not free.  Remember:

*   A shard is a Lucene index under the covers, which uses file handles,
    memory, and CPU cycles.

*   Every search request needs to hit a copy of every shard in the index.
    That's fine if every shard is sitting on a different node, but not if many
    shards have to compete for the same resources.

*   Term statistics, used to calculate relevance, are per shard.  Having a small
    amount of data in many shards leads to poor relevance.

[TIP]
===============================

A little overallocation is good. A kagillion shards is bad. It is difficult to
define what constitutes too many shards, as it depends on their size and how
they are being used. A hundred shards that are seldom used may be fine, while
two shards experiencing very heavy usage could be too many. Monitor your nodes
to ensure that they have enough spare capacity to deal with exceptional
conditions.

===============================

Scaling out should be done in phases.  Build in enough capacity to get to the
next phase. Once you get to the next phase, you have time to think about the
changes you need to make to reach the phase after that.


