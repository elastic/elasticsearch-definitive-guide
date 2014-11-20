=== Finding Multiple Exact Values

The `term` filter is useful for finding a single value, but often you'll  want
to search for multiple values.((("exact values", "finding multiple")))((("structured search", "finding multiple exact values")))  What if you want to find documents that have a
price of $20 or $30?

Rather than using multiple `term` filters, you can instead use a single `terms`
filter (note the _s_ at the end).  The `terms` filter((("terms filter"))) is simply the plural
version of the singular `term` filter.

It looks nearly identical to a vanilla `term` too.  Instead of
specifying a single price, we are now specifying an array of values:

[source,js]
--------------------------------------------------
{
    "terms" : {
        "price" : [20, 30]
    }
}
--------------------------------------------------

And like the `term` filter, we will place it inside a `filtered` query to
((("filtered query", "terms filter in"))) use it:

[source,js]
--------------------------------------------------
GET /my_store/products/_search
{
    "query" : {
        "filtered" : {
            "filter" : {
                "terms" : { <1>
                    "price" : [20, 30]
                }
            }
        }
    }
}
--------------------------------------------------
// SENSE: 080_Structured_Search/15_Terms_filter.json

<1> The `terms` filter as seen previously, but placed inside the `filtered` query

The query will return the second, third, and fourth documents:

[source,json]
--------------------------------------------------
"hits" : [
    {
        "_id" :    "2",
        "_score" : 1.0,
        "_source" : {
          "price" :     20,
          "productID" : "KDKE-B-9947-#kL5"
        }
    },
    {
        "_id" :    "3",
        "_score" : 1.0,
        "_source" : {
          "price" :     30,
          "productID" : "JODL-X-1937-#pV7"
        }
    },
    {
        "_id":     "4",
        "_score":  1.0,
        "_source": {
           "price":     30,
           "productID": "QQPX-R-3956-#aD8"
        }
     }
]
--------------------------------------------------




