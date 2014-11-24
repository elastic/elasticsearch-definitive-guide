[[combining-filters]]
=== Combining Filters

The previous two examples showed a single filter in use.((("structured search", "combining filters")))((("filters", "combining"))) In practice, you
will probably need to filter on multiple values or fields.  For example, how
would you express this SQL in Elasticsearch?

[source,sql]
--------------------------------------------------
SELECT product
FROM   products
WHERE  (price = 20 OR productID = "XHDK-A-1293-#fJ3")
  AND  (price != 30)
--------------------------------------------------

In these situations, you will need the `bool` filter.((("filters", "combining", "in bool filter")))((("bool filter")))  This is a _compound
filter_ that accepts other filters as arguments, combining them in various
Boolean combinations.

[[bool-filter]]
==== Bool Filter

The `bool` filter is composed of three sections:

[source,js]
--------------------------------------------------
{
   "bool" : {
      "must" :     [],
      "should" :   [],
      "must_not" : [],
   }
}
--------------------------------------------------

 `must`::    
   All of these clauses _must_ match. The equivalent of `AND`.
   
 `must_not`:: 
   All of these clauses _must not_ match. The equivalent of `NOT`.
   
 `should`::   
   At least one of these clauses must match. The equivalent of `OR`.

And that's it!((("should clause", "in bool filters")))((("must_not clause", "in bool filters")))((("must clause", "in bool filters"))) When you need multiple filters, simply place them into the
different sections of the `bool` filter.

[NOTE]
====
Each section of the `bool` filter is optional (for example, you can have a `must`
clause and nothing else), and each section can contain a single filter or an
array of filters.
====

To replicate the preceding SQL example, we will take the two `term` filters that
we used((("term filter", "placing inside bool filter")))((("bool filter", "with two term filters in should clause and must_not clause"))) previously and place them inside the `should` clause of a `bool`
filter, and add another clause to deal with the `NOT` condition:

[source,js]
--------------------------------------------------
GET /my_store/products/_search
{
   "query" : {
      "filtered" : { <1>
         "filter" : {
            "bool" : {
              "should" : [
                 { "term" : {"price" : 20}}, <2>
                 { "term" : {"productID" : "XHDK-A-1293-#fJ3"}} <2>
              ],
              "must_not" : {
                 "term" : {"price" : 30} <3>
              }
           }
         }
      }
   }
}
--------------------------------------------------
// SENSE: 080_Structured_Search/10_Bool_filter.json

<1> Note that we still need to use a `filtered` query to wrap everything.
<2> These two `term` filters are _children_ of the `bool` filter, and since they
    are placed inside the `should` clause, at least one of them needs to match.
<3> If a product has a price of `30`, it is automatically excluded because it
    matches a `must_not` clause.

Our search results return two hits, each document satisfying a different clause
in the `bool` filter:

[source,json]
--------------------------------------------------
"hits" : [
    {
        "_id" :     "1",
        "_score" :  1.0,
        "_source" : {
          "price" :     10,
          "productID" : "XHDK-A-1293-#fJ3" <1>
        }
    },
    {
        "_id" :     "2",
        "_score" :  1.0,
        "_source" : {
          "price" :     20, <2>
          "productID" : "KDKE-B-9947-#kL5"
        }
    }
]
--------------------------------------------------
<1> Matches the `term` filter for `productID = "XHDK-A-1293-#fJ3"`
<2> Matches the `term` filter for `price = 20`

==== Nesting Boolean Filters

Even though `bool` is a compound filter and accepts children filters, it is
important to understand that `bool` is just a filter itself.((("filters", "combining", "nesting bool filters")))((("bool filter", "nesting in another bool filter")))  This means you
can nest `bool` filters inside other `bool` filters, giving you the
ability to make arbitrarily complex Boolean logic.

Given this SQL statement:

[source,sql]
--------------------------------------------------
SELECT document
FROM   products
WHERE  productID      = "KDKE-B-9947-#kL5"
  OR (     productID = "JODL-X-1937-#pV7"
       AND price     = 30 )
--------------------------------------------------

We can translate it into a pair of nested `bool` filters:

[source,js]
--------------------------------------------------
GET /my_store/products/_search
{
   "query" : {
      "filtered" : {
         "filter" : {
            "bool" : {
              "should" : [
                { "term" : {"productID" : "KDKE-B-9947-#kL5"}}, <1>
                { "bool" : { <1>
                  "must" : [
                    { "term" : {"productID" : "JODL-X-1937-#pV7"}}, <2>
                    { "term" : {"price" : 30}} <2>
                  ]
                }}
              ]
           }
         }
      }
   }
}
--------------------------------------------------
// SENSE: 080_Structured_Search/10_Bool_filter.json

<1> Because the `term` and the `bool` are sibling clauses inside the first
    Boolean `should`, at least one of these filters must match for a document
    to be a hit.

<2> These two `term` clauses are siblings in a `must` clause, so they both
    have to match for a document to be returned as a hit.

The results show us two documents, one matching each of the `should` clauses:

[source,json]
--------------------------------------------------
"hits" : [
    {
        "_id" :     "2",
        "_score" :  1.0,
        "_source" : {
          "price" :     20,
          "productID" : "KDKE-B-9947-#kL5" <1>
        }
    },
    {
        "_id" :     "3",
        "_score" :  1.0,
        "_source" : {
          "price" :      30, <2>
          "productID" : "JODL-X-1937-#pV7" <2>
        }
    }
]
--------------------------------------------------
<1> This `productID` matches the `term` in the first `bool`.
<2> These two fields match the `term` filters in the nested `bool`.

This was a simple example, but it demonstrates how Boolean filters can be
used as building blocks to construct complex logical conditions.
