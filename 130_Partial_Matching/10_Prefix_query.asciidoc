[[prefix-query]]
=== prefix Query

To find all postcodes beginning with `W1`, we could use a ((("prefix query")))((("postcodes (UK), partial matching with", "prefix query")))simple `prefix`
query:

[source,js]
--------------------------------------------------
GET /my_index/address/_search
{
    "query": {
        "prefix": {
            "postcode": "W1"
        }
    }
}
--------------------------------------------------
// SENSE: 130_Partial_Matching/10_Prefix_query.json

The `prefix` query is a low-level query that works at the term level.  It
doesn't analyze the query string before searching. It assumes that you have
passed it the exact prefix that you want to find.

[TIP]
==================================================

By default, the `prefix` query does no relevance scoring.  It just finds
matching documents and gives them all a score of `1`.  Really, it behaves more
like a filter than a query.  The only practical difference between the
`prefix` query and the `prefix` filter is that the filter can be cached.

==================================================


Previously, we said that ``you can find only terms that exist in the inverted
index,'' but we haven't done anything special to index these postcodes; each
postcode is simply indexed as the exact value specified in each document.  So
how does the `prefix` query work?

[role="pagebreak-after"]
Remember that the inverted index consists((("inverted index", "for postcodes"))) of a sorted list of unique terms (in
this case, postcodes).  For each term, it lists the IDs of the documents
containing that term in the _postings list_.  The inverted index for our
example documents looks something like this:

    Term:          Doc IDs:
    -------------------------
    "SW5 0BE"    |  5
    "W1F 7HW"    |  3
    "W1V 3DG"    |  1
    "W2F 8HW"    |  2
    "WC1N 1LZ"   |  4
    -------------------------

To support prefix matching on the fly, the query does the following:

1. Skips through the terms list to find the first term beginning with `W1`.
2. Collects the associated document IDs.
3. Moves to the next term.
4. If that term also begins with `W1`, the query repeats from step 2; otherwise, we're finished.

While this works fine for our small example, imagine that our inverted index
contains a million postcodes beginning with `W1`. The prefix query
would need to visit all one million terms in order to calculate the result!

And the shorter the prefix, the more terms need to be visited. If we were to
look for the prefix `W` instead of `W1`, perhaps we would match 10 million
terms instead of just one million.

CAUTION: The `prefix` query or filter are useful for ad hoc prefix matching, but
should be used with care. ((("prefix query", "caution with"))) They can be used freely on fields with a small
number of terms, but they scale poorly and can put your cluster under a lot of
strain.  Try to limit their impact on your cluster by using a long prefix;
this reduces the number of terms that need to be visited.

Later in this chapter, we present an alternative index-time solution that
makes prefix matching much more efficient.  But first, we'll take a look at
two related queries: the `wildcard` and `regexp` queries.
