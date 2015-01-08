=== Finding Exact Values

When working with exact values,((("structured search", "finding exact values")))((("exact values", "finding"))) you will be working with filters. Filters are
important because they are very, very fast.  Filters do not calculate
relevance (avoiding the entire scoring phase) and are easily cached. We'll
talk about the performance benefits of filters later in <<filter-caching>>,
but for now, just keep in mind that you should use filters as often as you
can.

==== term Filter with Numbers

We are going to explore the `term` filter ((("term filter", "with numbers")))((("structured search", "finding exact values", "using term filter with numbers")))first because you will use it often.
This filter is capable of handling numbers, Booleans, dates, and text.

Let's look at an example using numbers first by indexing some products.  These
documents have a `price` and a `productID`:

[source,js]
--------------------------------------------------
POST /my_store/products/_bulk
{ "index": { "_id": 1 }}
{ "price" : 10, "productID" : "XHDK-A-1293-#fJ3" }
{ "index": { "_id": 2 }}
{ "price" : 20, "productID" : "KDKE-B-9947-#kL5" }
{ "index": { "_id": 3 }}
{ "price" : 30, "productID" : "JODL-X-1937-#pV7" }
{ "index": { "_id": 4 }}
{ "price" : 30, "productID" : "QQPX-R-3956-#aD8" }
--------------------------------------------------
// SENSE: 080_Structured_Search/05_Term_number.json

Our goal is to find all products with a certain price.  You may be familiar
with SQL if you are coming from a relational database background.  If we
expressed this query as an SQL query, it would look like this:

[source,sql]
--------------------------------------------------
SELECT document
FROM   products
WHERE  price = 20
--------------------------------------------------

In the Elasticsearch query DSL, we use a `term` filter to accomplish the same
thing.  The `term` filter will look for the exact value that we specify.  By
itself, a `term` filter is simple. It accepts a field name and the value
that we wish to find:

[source,js]
--------------------------------------------------
{
    "term" : {
        "price" : 20
    }
}
--------------------------------------------------

The `term` filter isn't very useful on its own, though.  As discussed in
<<query-dsl-intro>>, the `search` API expects a `query`, not a `filter`. To
use our `term` filter, ((("filtered query")))we need to wrap it with a
<<filtered-query,`filtered` query>>:

[source,js]
--------------------------------------------------
GET /my_store/products/_search
{
    "query" : {
        "filtered" : { <1>
            "query" : {
                "match_all" : {} <2>
            },
            "filter" : {
                "term" : { <3>
                    "price" : 20
                }
            }
        }
    }
}
--------------------------------------------------
// SENSE: 080_Structured_Search/05_Term_number.json

<1> The `filtered` query accepts both a `query` and a `filter`.
<2> A `match_all` is used to return all matching documents.((("match_all query clause")))  This is the default
behavior, so in future examples we will simply omit the `query` section.
<3> The `term` filter that we saw previously.  Notice how it is placed inside
the `filter` clause.

Once executed, the search results from this query are exactly what you would
expect: only document 2 is returned as a hit (because only `2` had a price
of `20`):

[source,json]
--------------------------------------------------
"hits" : [
    {
        "_index" : "my_store",
        "_type" :  "products",
        "_id" :    "2",
        "_score" : 1.0, <1>
        "_source" : {
          "price" :     20,
          "productID" : "KDKE-B-9947-#kL5"
        }
    }
]
--------------------------------------------------
<1> Filters do not perform scoring or relevance. The score comes from the
    `match_all` query, which treats all docs as equal, so all results receive
    a neutral score of `1`.

==== term Filter with Text

As mentioned at the top of ((("structured search", "finding exact values", "using term filter with text")))((("term filter", "with text")))this section, the `term` filter can match strings
just as easily as numbers.  Instead of price, let's try to find products that
have a certain UPC identification code. To do this with SQL, we might use a
query like this:

[source,sql]
--------------------------------------------------
SELECT product
FROM   products
WHERE  productID = "XHDK-A-1293-#fJ3"
--------------------------------------------------

Translated into the query DSL, we can try a similar query with the `term`
filter, like so:

[source,js]
--------------------------------------------------
GET /my_store/products/_search
{
    "query" : {
        "filtered" : {
            "filter" : {
                "term" : {
                    "productID" : "XHDK-A-1293-#fJ3"
                }
            }
        }
    }
}
--------------------------------------------------
// SENSE: 080_Structured_Search/05_Term_text.json

Except there is a little hiccup: we don't get any results back!  Why is
that? The problem isn't with the the `term` query; it is with the way
the data has been indexed. ((("analyze API, using to understand tokenization"))) If we use the `analyze` API (<<analyze-api>>), we
can see that our UPC has been tokenized into smaller tokens:

[source,js]
--------------------------------------------------
GET /my_store/_analyze?field=productID
XHDK-A-1293-#fJ3
--------------------------------------------------
[source,js]
--------------------------------------------------
{
  "tokens" : [ {
    "token" :        "xhdk",
    "start_offset" : 0,
    "end_offset" :   4,
    "type" :         "<ALPHANUM>",
    "position" :     1
  }, {
    "token" :        "a",
    "start_offset" : 5,
    "end_offset" :   6,
    "type" :         "<ALPHANUM>",
    "position" :     2
  }, {
    "token" :        "1293",
    "start_offset" : 7,
    "end_offset" :   11,
    "type" :         "<NUM>",
    "position" :     3
  }, {
    "token" :        "fj3",
    "start_offset" : 13,
    "end_offset" :   16,
    "type" :         "<ALPHANUM>",
    "position" :     4
  } ]
}
--------------------------------------------------
// SENSE: 080_Structured_Search/05_Term_text.json

There are a few important points here:

* We have four distinct tokens instead of a single token representing the UPC.
* All letters have been lowercased.
* We lost the hyphen and the hash (`#`) sign.

So when our `term` filter looks for the exact value `XHDK-A-1293-#fJ3`, it
doesn't find anything, because that token does not exist in our inverted index.
Instead, there are the four tokens listed previously.

Obviously, this is not what we want to happen when dealing with identification
codes, or any kind of precise enumeration.

To prevent this from happening, we need to tell Elasticsearch that this field
contains an exact value by  setting it to be `not_analyzed`.((("not_analyzed string fields"))) We saw this
originally in <<custom-field-mappings>>.  To do this, we need to first delete
our old index (because it has the incorrect mapping) and create a new one with
the correct mappings:

[source,js]
--------------------------------------------------
DELETE /my_store <1>

PUT /my_store <2>
{
    "mappings" : {
        "products" : {
            "properties" : {
                "productID" : {
                    "type" : "string",
                    "index" : "not_analyzed" <3>
                }
            }
        }
    }

}
--------------------------------------------------
// SENSE: 080_Structured_Search/05_Term_text.json
<1> Deleting the index first is required, since we cannot change mappings that
    already exist.
<2> With the index deleted, we can re-create it with our custom mapping.
<3> Here we explicitly say that we don't want `productID` to be analyzed.

Now we can go ahead and reindex our documents:

[source,js]
--------------------------------------------------
POST /my_store/products/_bulk
{ "index": { "_id": 1 }}
{ "price" : 10, "productID" : "XHDK-A-1293-#fJ3" }
{ "index": { "_id": 2 }}
{ "price" : 20, "productID" : "KDKE-B-9947-#kL5" }
{ "index": { "_id": 3 }}
{ "price" : 30, "productID" : "JODL-X-1937-#pV7" }
{ "index": { "_id": 4 }}
{ "price" : 30, "productID" : "QQPX-R-3956-#aD8" }
--------------------------------------------------
// SENSE: 080_Structured_Search/05_Term_text.json

Only now will our `term` filter work as expected.  Let's try it again on the
newly indexed data (notice, the query and filter have not changed at all, just
how the data is mapped):

[source,js]
--------------------------------------------------
GET /my_store/products/_search
{
    "query" : {
        "filtered" : {
            "filter" : {
                "term" : {
                    "productID" : "XHDK-A-1293-#fJ3"
                }
            }
        }
    }
}
--------------------------------------------------
// SENSE: 080_Structured_Search/05_Term_text.json

Since the `productID` field is not analyzed, and the `term` filter performs no
analysis, the query finds the exact match and returns document 1 as a hit.
Success!

[[_internal_filter_operation]]
==== Internal Filter Operation

Internally, Elasticsearch is((("structured search", "finding exact values", "intrnal filter operations")))((("filters", "internal filter operation"))) performing several operations when executing a
filter:

1. _Find matching docs_.
+
The `term` filter looks up the term `XHDK-A-1293-#fJ3` in the inverted index
and retrieves the list of documents that contain that term.  In this case,
only document 1 has the term we are looking for.

2. _Build a bitset_.
+
The filter then builds a _bitset_--an array of 1s and 0s--that
describes which documents contain the term.  Matching documents receive a  `1`
bit.  In our example, the bitset would be `[1,0,0,0]`.

3. _Cache the bitset_.
+
Last, the bitset is stored in memory, since we can use this in the future
and skip steps 1 and 2.  This adds a lot of performance and makes filters very
fast.

When executing a `filtered` query, the `filter` is executed before the
`query`. The resulting bitset is given to the `query`, which uses it to simply
skip over any documents that have already been excluded by the filter. This is
one of the ways that filters can improve performance.  Fewer documents
evaluated by the query  means faster response times.


