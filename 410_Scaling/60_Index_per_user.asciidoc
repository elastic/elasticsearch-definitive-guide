[[user-based]]
=== User-Based Data

Often, users start using Elasticsearch because they need to add full-text
search or analytics to an existing application.((("scaling", "user-based data")))((("user-based data")))  They create a single index
that holds all of their documents.  Gradually, others in the company realize
how much benefit Elasticsearch brings, and they want to add their data to
Elasticsearch as well.

Fortunately, Elasticsearch supports
http://en.wikipedia.org/wiki/Multitenancy[multitenancy] so each new user can
have her own index in the same cluster.((("mulltitenancy")))  Occasionally, somebody will want to
search across the documents for all users, which they can do by searching
across all indices, but most of the time, users are interested in only their
own documents.

Some users have more documents than others, and some users will have heavier
search loads than others, so the ability to specify the number of primary shards
and replica shards that each index should have fits well with the index-per-user
model.((("indices", "index-per-user model")))((("primary shards", "number per-index"))) Similarly, busier indices can be allocated to stronger boxes with shard
allocation filtering. (See <<migrate-indices>>.)

TIP: Don't just use the default number of primary shards for every index.
Think about how much data that index needs to hold.  It may be that all you
need is one shard--any more is a waste of resources.

Most users of Elasticsearch can stop here.  A simple index-per-user approach
is sufficient for the majority of cases.

In exceptional cases, you may find that you need to support a large number of
users, all with similar needs.  An example might be hosting a search engine
for thousands of email forums. ((("forums, resource allocation for"))) Some forums may have a huge amount of traffic,
but the majority of forums are quite small.  Dedicating an index with a single
shard to a small forum is overkill--a single shard could hold the data for
many forums.

What we need is a way to share resources across users, to give the impression
that each user has his own index without wasting resources on small users.

