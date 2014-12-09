[[grandparents]]
=== Grandparents and Grandchildren

The parent-child relationship can extend across more than one generation--grandchildren can ((("parent-child relationship", "grandparents and grandchildren")))((("grandparents and grandchildren")))have grandparents--but it requires an extra step to ensure
that documents from all generations are indexed on the same shard.

Let's change our previous example to make the `country` type a parent of the
`branch` type:

[source,json]
-------------------------
PUT /company
{
  "mappings": {
    "country": {},
    "branch": {
      "_parent": {
        "type": "country" <1>
      }
    },
    "employee": {
      "_parent": {
        "type": "branch" <2>
      }
    }
  }
}
-------------------------
<1> `branch` is a child of `country`.
<2> `employee` is a child of `branch`.

Countries and branches have a simple parent-child relationship, so we use the
same process as we used in <<indexing-parent-child>>:

[source,json]
-------------------------
POST /company/country/_bulk
{ "index": { "_id": "uk" }}
{ "name": "UK" }
{ "index": { "_id": "france" }}
{ "name": "France" }

POST /company/branch/_bulk
{ "index": { "_id": "london", "parent": "uk" }}
{ "name": "London Westmintster" }
{ "index": { "_id": "liverpool", "parent": "uk" }}
{ "name": "Liverpool Central" }
{ "index": { "_id": "paris", "parent": "france" }}
{ "name": "Champs Élysées" }
-------------------------

The `parent` ID has ensured that each `branch` document is routed to the same
shard as its parent `country` document.  However, look what would happen if we
were to use the same technique with the `employee` grandchildren:

[source,json]
-------------------------
PUT /company/employee/1?parent=london
{
  "name":  "Alice Smith",
  "dob":   "1970-10-24",
  "hobby": "hiking"
}
-------------------------

The shard routing of the employee document would be decided by the parent ID&#x2014;`london`&#x2014;but the `london` document was routed to a shard by _its own_
parent ID&#x2014;`uk`.  It is very likely that the grandchild would end up on
a different shard from its parent and grandparent, which would prevent the
same-shard parent-child mapping from functioning.

Instead, we need to add an extra `routing` parameter, set to the ID of the
grandparent, to ensure that all three generations are indexed on the same
shard.  The indexing request should look like this:

[source,json]
-------------------------
PUT /company/employee/1?parent=london&routing=uk <1>
{
  "name":  "Alice Smith",
  "dob":   "1970-10-24",
  "hobby": "hiking"
}
-------------------------
<1> The `routing` value overrides the `parent` value.

The `parent` parameter is still used to link the employee document with its
parent, but the `routing` parameter ensures that it is stored on the same
shard as its parent and grandparent. The `routing` value needs to be provided
for all single-document requests.

Querying and aggregating across generations works, as long as you step through
each generation. For instance, to find countries where employees enjoy hiking,
we need to join countries with branches, and branches with employees:

[source,json]
-------------------------
GET /company/country/_search
{
  "query": {
    "has_child": {
      "type": "branch",
      "query": {
        "has_child": {
          "type": "employee",
          "query": {
            "match": {
              "hobby": "hiking"
            }
          }
        }
      }
    }
  }
}
-------------------------

