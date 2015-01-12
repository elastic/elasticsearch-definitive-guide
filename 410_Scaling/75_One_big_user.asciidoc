[[one-big-user]]
=== One Big User

Big, popular forums start out as small forums.((("forums, resource allocation for", "one big user")))  One day we will find that one
shard in our shared index is doing a lot more work than the other shards,
because it holds the documents for a forum that has become very popular. That
forum now needs its own index.

The index aliases that we're using to fake an index per user give us a clean
migration path for the big forum.((("indices", "shared", "migrating data to dedicated index")))

The first step is to create a new index dedicated to the forum, and with the
appropriate number of shards to allow for expected growth:

[source,json]
------------------------------
PUT /baking_v1
{
  "settings": {
    "number_of_shards": 3
  }
}
------------------------------

The next step is to migrate the data from the shared index into the dedicated
index, which can be done using <<scan-scroll,scan-and-scroll>> and the
<<bulk,`bulk` API>>.  As soon as the migration is finished, the index alias
can be updated to point to the new index:

[source,json]
------------------------------
POST /_aliases
{
  "actions": [
    { "remove": { "alias": "baking", "index": "forums"    }},
    { "add":    { "alias": "baking", "index": "baking_v1" }}
  ]
}
------------------------------

Updating the alias is atomic; it's like throwing a switch.  Your application
continues talking to the `baking` API and is completely unaware that it now
points to a new dedicated index.

The dedicated index no longer needs the filter or the routing values. We can
just rely on the default sharding that Elasticsearch does using each
document's `_id` field.

The last step is to remove the old documents from the shared index, which can
be done with a `delete-by-query` request, using the original routing value and
forum ID:

[source,json]
------------------------------
DELETE /forums/post/_query?routing=baking
{
  "query": {
    "term": {
      "forum_id": "baking"
    }
  }
}
------------------------------

The beauty of this index-per-user model is that it allows you to reduce
resources, keeping costs low, while still giving you the flexibility to scale
out when necessary, and with zero downtime.
