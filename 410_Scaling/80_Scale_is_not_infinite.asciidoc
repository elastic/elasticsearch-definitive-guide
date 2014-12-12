[[finite-scale]]
=== Scale Is Not Infinite

Throughout this chapter we have spoken about many of the ways that
Elasticsearch can scale. ((("scaling", "scale is not infinite")))Most scaling problems can be solved by adding more
nodes. But one resource is finite and should be treated with
respect: the cluster state.((("cluster state")))

The _cluster state_ is a data structure that holds the following cluster-level information:

* Cluster-level settings
* Nodes that are part of the cluster
* Indices, plus their settings, mappings, analyzers, warmers, and aliases
* The shards associated with each index, plus the node on which they are
  allocated

You can view the current cluster state with this request:

[source,json]
------------------------------
GET /_cluster/state
------------------------------

The cluster state exists on every node in the cluster,((("nodes", "cluster state"))) including client nodes.
This is how any node can forward a request directly to the node that holds the
requested data--every node knows where every document lives.

Only the master node is allowed to update the cluster state.  Imagine that an
indexing request introduces a previously unknown field.  The node holding the
primary shard for the document must forward the new mapping to the master
node.  The master node incorporates the changes in the cluster state, and
publishes a new version to all of the nodes in the cluster.

Search requests _use_ the cluster state, but they don't change it.  The same
applies to document-level CRUD requests unless, of course, they introduce a
new field that requires a mapping update. By and large, the cluster state is
static and is not a bottleneck.

However, remember that this same data structure has to exist in memory on
every node, and must be published to every node whenever it is updated.  The
bigger it is, the longer that process will take.

The most common problem that we see with the cluster state is the introduction
of too many fields. A user might decide to use a separate field for every IP
address, or every referer URL.  The following example keeps track of the number of
times a page has been visited by using a different field name for every unique
referer:

[role="pagebreak-before"]
[source,json]
------------------------------
POST /counters/pageview/home_page/_update
{
  "script": "ctx._source[referer]++",
  "params": {
    "referer": "http://www.foo.com/links?bar=baz"
  }
}
------------------------------

This approach is catastrophically bad! It will result in millions of fields,
all of which have to be stored in the cluster state.  Every time a new referer
is seen, a new field is added to the already bloated cluster state, which then
has to be published to every node in the cluster.

A much better approach ((("nested objects")))((("objects", "nested")))is to use <<nested-objects,nested objects>>, with one
field for the parameter name&#x2014;`referer`&#x2014and another field for its
associated value&#x2014;`count`:

[source,json]
------------------------------
    "counters": [
      { "referer": "http://www.foo.com/links?bar=baz",  "count": 2 },
      { "referer": "http://www.linkbait.com/article_3", "count": 10 },
      ...
    ]
------------------------------

The nested approach may increase the number of documents, but Elasticsearch is
built to handle that.  The important thing is that it keeps the cluster state
small and agile.

Eventually, despite your best intentions, you may find that the number of
nodes and indices and mappings that you have is just too much for one cluster.
At this stage, it is probably worth dividing the problem into multiple
clusters.  Thanks to http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/modules-tribe.html[`tribe` nodes], you can even run
searches across multiple clusters, as if they were one big cluster.


