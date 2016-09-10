[[distributed-search]]
== Distributed Search Execution

Before moving on, we are going to take a detour and talk about how search is
executed in a distributed environment.((("distributed search execution")))  It is a bit more complicated than the
basic _create-read-update-delete_ (CRUD) requests((("CRUD (create-read-update-delete) operations"))) that we discussed in
<<distributed-docs>>.

.Content Warning
****

The information presented in this chapter is for your interest. You are not required to
understand and remember all the detail in order to use Elasticsearch.

Read this chapter to gain a taste for how things work, and to know where the
information is in case you need to refer to it in the future, but don't be
overwhelmed by the detail.

****

A CRUD operation deals with a single document that has a unique combination of
`_index`, `_type`, and <<routing-value,`routing` values>> (which defaults to the
document's `_id`). This means that we know exactly which shard in the cluster
holds that document.

Search requires a more complicated execution model because we don't know which
documents will match the query: they could be on any shard in the cluster. A
search request has to consult a copy of every shard in the index or indices
we're interested in to see if they have any matching documents.

But finding all matching documents is only half the story. Results from
multiple shards must be combined into a single sorted list before the `search`
API can return a ``page'' of results. For this reason, search is executed in a
two-phase process called _query then fetch_.
