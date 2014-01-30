
==== Default values for null fields

Sometimes you need to be able to distinguish between a field that doesn't have
a value, and a field that has been explicitly set to `null`. With the default
behavior that we saw above, this is impossible.  The data is  lost. Luckily,
there is an option that we can set that replaces explicit  `null` values with
a ``placeholder'' value.

Most core types (String, Number, Boolean, Date) support an option to define a
null value with your own placeholder.  This option is called `null_value` and
is set in the mappings of a type.

In this mapping, we define a string as the default when a `null` is encountered.
Let's delete our tagging example and recreate it with `null_value` specified:

[source,js]
--------------------------------------------------
DELETE /my_index <1>

PUT /my_index
{
    "mappings" : {
        "posts" : {
            "properties" : {
                "tags" : {
                    "type" : "string",
                    "index" : "not_analyzed",
                    "null_value" : "NULL" <2>
                }
            }
        }
    }
}

POST /my_index/posts/_bulk
{ "index": { "_id": "1" }}
{"tags" : ["search"] }
{ "index": { "_id": "2" }}
{ "tags" : ["search", "open_source"] }
{ "index": { "_id": "3" }}
{ "other_field" : "some data" }
{ "index": { "_id": "4" }}
{ "tags" : null }
{ "index": { "_id": "5" }}
{ "tags" : ["search", null] }

--------------------------------------------------
<1> Delete the old index, since we cannot update the mapping
<2> The new index now specifies `null_value` for tags

Now, whenever an explicit `null` is encountered, Elasticsearch will replace it
with the term `"NULL"`.  This means the term `"NULL"` is now part of the
inverted index, so Elasticsearch can use the term for more advanced behavior.
It also means that your null-placeholder must be unique and *not used in your
normal data*, otherwise you'll get some very strange results!

After this indexing, our inverted index will look like this:

[width="50%",frame="topbot"]
|==========================
| Token | DocIDs
|`search`| `1`,`2`,`5`
|`open_source` | `2`
|`NULL` | `4`,`5`
|==========================

.Must match the field's type
****
The null-placeholder that you specify must match the field's type.  For example,
you can't set `null_value` to `"NULL"` for a numeric field, since a string cannot
be indexed as a number.

Make sure you specify the correct type of `null_value` for the field.
****

If we re-run our `missing` filter from before:

[source,js]
--------------------------------------------------
GET /my_index/posts/_search
{
    "query" : {
        "filtered" : {
            "filter" : {
                "missing" : {"field" : "tags"}
            }
        }
    }
}
--------------------------------------------------

We get slightly different results: document `4` no longer appears in the hits.
Only document `3` is returned:

[source,js]
--------------------------------------------------
"hits" : [
    {
      "_index" : "my_index",
      "_type" : "posts",
      "_id" : "3",
      "_score" : 1.0, "_source" : { "other_field" : "some data" }
    }
]
--------------------------------------------------

This makes sense when you think about what is happening internally.
Elasticsearch is indexing an actual value for the field (`"NULL"`), which means
the field is not technically missing anymore.

We are now dealing with two different types of "missing" fields.  Fields that
were actually omitted in the original document, and fields that were explicitly
set to `null` but now have a placeholder value.  By default, the `missing` filter
will only show you documents where the field was omitted entirely.

This behavior is modifiable using two different options: `null_value` and
`existence`.  Both values can be set true or false, and the different
combinations of these two options will give you different search results.

`null_value` controls how explicit `nulls` are handled.  By setting this to true,
the filter will treat explicit `null` values (e.g. those with a null-placeholder)
as "missing" and therefore return them as a match.

`existence` controls how entirely missing values are handled.  If set to true,
the filter will match documents where a field was omitted entirely.

You can mix and match `null_value` and `existence` to get different behaviors.
To see an example of each configuration, check the reference documentation.



