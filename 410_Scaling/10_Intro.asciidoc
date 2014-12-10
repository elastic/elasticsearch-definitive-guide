[[scale]]
== Designing for Scale

Elasticsearch is used by some companies to index ((("scaling", "designing for scale")))and search petabytes of data
every day, but most of us start out with something a little more humble in
size. Even if we aspire to be the next Facebook, it is unlikely that our bank
balance matches our aspirations.  We need to build for what we have today, but
in a way that will allow us to scale out flexibly and rapidly.

Elasticsearch is built to scale.  It will run very happily on your laptop or
in a cluster containing hundreds of nodes, and the experience is almost
identical. Growing from a small cluster to a large cluster is almost entirely
automatic and painless. Growing from a large cluster to a very large cluster
requires a bit more planning and design, but it is still relatively painless.

Of course, it is not magic.  Elasticsearch has its limitations too.  If you
are aware of those limitations and work with them, the growing process will be
pleasant.  If you treat Elasticsearch badly, you could be in for a world of
pain.

The default settings in Elasticsearch will take you a long way, but to get the
most bang for your buck, you need to think about how data flows through your
system.  We will talk about two common data flows: time-based data (such as log
events or social network streams, where relevance is driven by recency), and
user-based data (where a large document collection can be subdivided by user or
customer).

This chapter will help you make the right decisions up front, to avoid
nasty surprises later.
