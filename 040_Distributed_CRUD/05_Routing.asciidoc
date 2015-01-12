[[routing-value]]
=== Routing a Document to a Shard

When you index a document, it is stored on a single primary shard.((("shards", "routing a document to")))((("documents", "routing a document to a shard")))((("routing a document to a shard"))) How does
Elasticsearch know which shard a document belongs to?  When we create a new
document, how does it know whether it should store that document on shard 1 or
shard 2?

The process can't be random, since we may need to retrieve the document in the
future. In fact, it is determined by a simple formula:

    shard = hash(routing) % number_of_primary_shards

The `routing` value is an arbitrary string, which defaults to the document's
`_id` but can also be set to a custom value. This `routing` string is passed
through a hashing function to generate a number, which is divided by the
number of primary shards in the index to return the _remainder_. The remainder
will always be in the range `0` to `number_of_primary_shards - 1`, and gives
us the number of the shard where a particular document lives.

This explains why the number of primary shards((("primary shards", "fixed number of, routing and"))) can be set only when an index
is created and never changed:  if the number of primary shards ever changed in
the future, all previous routing values would be invalid and documents would
never be found.

[NOTE]
====
Users sometimes think that having a fixed number of primary shards makes it
difficult to scale out an index later.  In reality, there are techniques
that make it easy to scale out as and when you need. We talk more about these
in <<scale>>.
====

All document APIs (`get`, `index`, `delete`, `bulk`, `update`, and `mget`)
accept a `routing` parameter ((("routing parameter")))that can be used to customize the document-to-
shard mapping. A custom routing value could be used to ensure that all related
documents--for instance, all the documents belonging to the same user--are
stored on the same shard. We discuss in detail why you may want to do this in
<<scale>>.
