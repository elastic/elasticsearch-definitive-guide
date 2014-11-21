[[relevance-is-broken]]
=== Relevance Is Broken!

Before we move on to discussing more-complex queries in
<<multi-field-search>>, let's make a quick detour to explain why we
<<match-test-data,created our test index>> with just one primary shard.

Every now and again a new user opens an issue claiming that sorting by
relevance((("relevance", "differences in IDF producing incorrect results"))) is broken and offering a short reproduction: the user indexes a few
documents, runs a simple query, and finds apparently less-relevant results
appearing above more-relevant results.

To understand why this happens, let's imagine that we create an index with two
primary shards and we index ten documents, six of which contain the word `foo`.
It may happen that shard 1 contains three of the `foo` documents and shard
2 contains the other three.  In other words, our documents are well distributed.

In <<relevance-intro>>, we described the default similarity algorithm used in
Elasticsearch, ((("Term Frequency/Inverse Document Frequency  (TF/IDF) similarity algorithm")))called _term frequency / inverse document frequency_ or TF/IDF.
Term frequency counts the number of times a term appears within the field we are
querying in the current document.  The more times it appears, the more
relevant is this document. The _inverse document frequency_ takes((("inverse document frequency")))((("IDF", see="inverse document frequency"))) into account
how often a term appears as a percentage of _all the documents in the index_.
The more frequently the term appears, the less weight it has.

However, for performance reasons, Elasticsearch doesn't calculate the IDF
across all documents in the index.((("shards", "local inverse document frequency (IDF)"))) Instead, each shard calculates a local IDF
for the documents contained _in that shard_.

Because our documents are well distributed, the IDF for both shards will be
the same.  Now imagine instead that five of the `foo` documents are on shard 1,
and the sixth document is on shard 2.  In this scenario, the term `foo` is
very common on one shard (and so of little importance), but rare on the other
shard (and so much more important). These differences in IDF can produce
incorrect results.

In practice, this is not a problem. The differences between local and  global
IDF diminish the more documents that you add to the index. With real-world
volumes of data, the local IDFs soon even out. The problem is not that
relevance is broken but that there is too little data.

For testing purposes, there are two ways we can work around this issue. The
first is to create an index with one primary shard, as we did in the section
introducing the <<match-query,`match` query>>. If you have only one shard, then
the local IDF _is_ the global IDF.

The second workaround is to add `?search_type=dfs_query_then_fetch` to your
search requests. The `dfs` stands((("search_type", "dfs_query_then_fetch")))((("dfs_query_then_fetch search type")))((("DFS (Distributed Frequency Search)"))) for _Distributed Frequency Search_, and it
tells Elasticsearch to first retrieve the local IDF from each shard in order
to calculate the global IDF across the whole index.

TIP: Don't use `dfs_query_then_fetch` in production.  It really isn't
required. Just having enough data will ensure that your term frequencies are
well distributed. There is no reason to add this extra DFS step to every query
that you run.

