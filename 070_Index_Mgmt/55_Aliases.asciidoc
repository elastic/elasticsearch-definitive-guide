[[index-aliases]]
=== Index Aliases and Zero Downtime

The problem with the reindexing process described previously is that you need
to update your application to use the new index name.((("index aliases")))  Index aliases
to the rescue!

An index _alias_ is like a shortcut or symbolic link, which can point to
one or more indices, and can be used in any API that expects an index name.
Aliases((("aliases, index"))) give us an enormous amount of flexibility. They allow us to do the following:

 * Switch transparently between one index and another on a running cluster
 * Group multiple indices (for example, `last_three_months`)
 * Create ``views'' on a subset of the documents in an index

We will talk more about the other uses for aliases later in the book. For now
we will explain how to use them to switch from an old index to a new index
with zero downtime.

There are two endpoints for managing aliases: `_alias` for single
operations, and `_aliases` to perform multiple operations atomically.

In this scenario, we will assume that your application is talking to an
index called `my_index`. In reality, `my_index` will be an alias that
points to the current real index.  We will include a version number in the
name of the real index: `my_index_v1`, `my_index_v2`, and so forth.

To start off, create the index `my_index_v1`, and set up the alias
`my_index` to point to it:

[source,js]
--------------------------------------------------
PUT /my_index_v1 <1>
PUT /my_index_v1/_alias/my_index <2>
--------------------------------------------------
// SENSE: 070_Index_Mgmt/55_Aliases.json

<1> Create the index `my_index_v1`.
<2> Set the `my_index` alias to point to `my_index_v1`.

You can check which index the alias points to:

[source,js]
--------------------------------------------------
GET /*/_alias/my_index
--------------------------------------------------
// SENSE: 070_Index_Mgmt/55_Aliases.json

Or which aliases point to the index:

[source,js]
--------------------------------------------------
GET /my_index_v1/_alias/*
--------------------------------------------------
// SENSE: 070_Index_Mgmt/55_Aliases.json

Both of these return the following:

[source,js]
--------------------------------------------------
{
    "my_index_v1" : {
        "aliases" : {
            "my_index" : { }
        }
    }
}
--------------------------------------------------


Later, we decide that we want to change the mappings for a field in our index.
Of course, we can't change the existing mapping, so we have to reindex
our data.((("reindexing", "using index aliases")))  To start, we create `my_index_v2` with the new mappings:

[source,js]
--------------------------------------------------
PUT /my_index_v2
{
    "mappings": {
        "my_type": {
            "properties": {
                "tags": {
                    "type":   "string",
                    "index":  "not_analyzed"
                }
            }
        }
    }
}
--------------------------------------------------
// SENSE: 070_Index_Mgmt/55_Aliases.json

Then we reindex our data from `my_index_v1` to `my_index_v2`, following
the process described in <<reindex>>.  Once we are satisfied that our
documents have been reindexed correctly, we switch our alias
to point to the new index.

An alias can point to multiple indices, so we need to remove the alias
from the old index at the same time as we add it to the new index.  The
change needs to be atomic, which means that we must use the `_aliases`
endpoint:

[source,js]
--------------------------------------------------
POST /_aliases
{
    "actions": [
        { "remove": { "index": "my_index_v1", "alias": "my_index" }},
        { "add":    { "index": "my_index_v2", "alias": "my_index" }}
    ]
}
--------------------------------------------------
// SENSE: 070_Index_Mgmt/55_Aliases.json


Your application has switched from using the old index to the new
index transparently, with zero downtime.

[TIP]
====
Even when you think that your current index design is perfect, it is likely
that you will need to make some change later, when your index
is already being used in production.

Be prepared: use aliases instead of indices in your application. Then you
will be able to reindex whenever you need to. Aliases are cheap and should
be used liberally.
====
