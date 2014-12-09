[[parent-child]]
== Parent-Child Relationship

The _parent-child_ relationship is ((("relationships", "parent-child")))((("parent-child relationship")))similar in nature to the
<<nested-objects,nested model>>: both allow you to associate one entity
with another. ((("nested objects", "parent-child relationships versus")))The difference is that, with nested objects, all entities live
within the same document while, with parent-child, the parent and children
are completely separate documents.

The parent-child functionality allows you to associate one document type with
another, in a _one-to-many_ relationship--one parent to many children.((("one-to-many relationships")))   The
advantages that parent-child has over <<nested-objects,`nested` objects>> are as follows:

* The parent document can be updated without reindexing the children.

* Child documents can be added, changed, or deleted without affecting either
  the parent or other children. This is especially useful when child documents
  are large in number and need to be added or changed frequently.

* Child documents can be returned as the results of a search request.

Elasticsearch maintains a map of which parents are associated with
which children.  It is thanks to this map that query-time joins are fast, but
it does place a limitation on the parent-child relationship: _the parent
document and all of its children must live on the same shard_.

[NOTE]
==================================================

At the time of going to press, the parent-child ID map is held in memory as
part of <<fielddata,fielddata>>.  There are plans afoot to change the default
setting to use <<doc-values,doc values>> by default instead.

==================================================


[[parent-child-mapping]]
=== Parent-Child Mapping

All that is needed in order to establish the parent-child relationship is to
specify which document type should be the parent of a child type.((("mapping (types)", "parent-child")))((("parent-child relationship", "parent-child mapping")))  This must
be done at index creation time, or with the `update-mapping` API before the
child type has been created.

As an example, let's say that we have a company that has branches in many
cities.  We would like to associate employees with the branch where they work.
We need to be able to search for branches, individual employees, and employees
who work for particular branches, so the nested model will not help.  We
could, of course,
use <<application-joins,application-side-joins>> or
<<denormalization,data denormalization>> here instead, but for demonstration
purposes we will use parent-child.

All that we have to do is to tell Elasticsearch that the `employee` type has
the `branch` document type as its `_parent`, which we can do when we create
the index:

[source,json]
-------------------------
PUT /company
{
  "mappings": {
    "branch": {},
    "employee": {
      "_parent": {
        "type": "branch" <1>
      }
    }
  }
}
-------------------------
<1> Documents of type `employee` are children of type `branch`.


