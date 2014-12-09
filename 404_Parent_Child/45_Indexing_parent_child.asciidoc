[[indexing-parent-child]]
=== Indexing Parents and Children

Indexing parent documents is no different from any other document. Parents
don't need to know anything about their children:

[source,json]
-------------------------
POST /company/branch/_bulk
{ "index": { "_id": "london" }}
{ "name": "London Westminster", "city": "London", "country": "UK" }
{ "index": { "_id": "liverpool" }}
{ "name": "Liverpool Central", "city": "Liverpool", "country": "UK" }
{ "index": { "_id": "paris" }}
{ "name": "Champs Élysées", "city": "Paris", "country": "France" }
-------------------------

When indexing child documents, you must specify the ID of the associated
parent document:

[source,json]
-------------------------
PUT /company/employee/1?parent=london <1>
{
  "name":  "Alice Smith",
  "dob":   "1970-10-24",
  "hobby": "hiking"
}
-------------------------
<1> This `employee` document is a child of the `london` branch.

This `parent` ID serves two purposes: it creates the link between the parent
and the child, and it ensures that the child document is stored on the same
shard as the parent.

In <<routing-value>>, we explained how Elasticsearch uses a routing value,
which defaults to the `_id` of the document, to decide which shard a document
should belong to.  The routing value is plugged into this simple formula:

    shard = hash(routing) % number_of_primary_shards

However, if a `parent` ID is specified, it is used as the routing value
instead of the `_id`.  In other words, both the parent and the child use the
same routing value--the `_id` of the parent--and so they are both stored
on the same shard.

The `parent` ID needs to be specified on all single-document requests:
when retrieving a child document with a `GET` request, or when indexing,
updating, or deleting a child document.  Unlike a search request, which is
forwarded to all shards in an index, these single-document requests are
forwarded only to the shard that holds the document--if the `parent` ID is
not specified, the request will probably be forwarded to the wrong shard.

The `parent` ID should also be specified when using the `bulk` API:

[source,json]
-------------------------
POST /company/employee/_bulk
{ "index": { "_id": 2, "parent": "london" }}
{ "name": "Mark Thomas", "dob": "1982-05-16", "hobby": "diving" }
{ "index": { "_id": 3, "parent": "liverpool" }}
{ "name": "Barry Smith", "dob": "1979-04-01", "hobby": "hiking" }
{ "index": { "_id": 4, "parent": "paris" }}
{ "name": "Adrien Grand", "dob": "1987-05-11", "hobby": "horses" }
-------------------------

WARNING: If you want to change the `parent` value of a child document, it is
not sufficient to just reindex or update the child document--the new parent
document may be on a different shard. Instead, you must first delete the old
child, and then index the new child.

