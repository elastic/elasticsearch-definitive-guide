=== Query-Time Search-as-You-Type

Leaving postcodes behind, let's take a look at how prefix matching can help
with full-text queries. ((("partial matching", "query time search-as-you-type"))) Users have become accustomed to seeing search results
before they have finished typing their query--so-called _instant search_, or
_search-as-you-type_. ((("search-as-you-type")))((("instant search"))) Not only do users receive their search results in less
time, but we can guide them toward results that actually exist in our index.

For instance, if a user types in `johnnie walker bl`, we would like to show results for Johnnie Walker Black Label and Johnnie Walker Blue
Label before they can finish typing their query.

As always, there are more ways than one to skin a cat! We will start by
looking at the way that is simplest to implement.  You don't need to prepare your
data in any way; you can implement _search-as-you-type_ at query time on any
full-text field.

In <<phrase-matching>>, we introduced the `match_phrase` query, which matches
all the specified words in the same positions relative to each other.  For-query time search-as-you-type, we can use a specialization of this query,
called ((("prefix query", "match_phrase_prefix query")))((("match_phrase_prefix query")))the `match_phrase_prefix` query:

[source,js]
--------------------------------------------------
{
    "match_phrase_prefix" : {
        "brand" : "johnnie walker bl"
    }
}
--------------------------------------------------
// SENSE: 130_Partial_Matching/20_Match_phrase_prefix.json

This query behaves in the same way as the `match_phrase` query, except that it
treats the last word in the query string as a prefix.  In other words, the
preceding example would look for the following:

* `johnnie`
* Followed by `walker`
* Followed by words beginning with `bl`

If you were to run this query through the `validate-query` API, it would
produce this explanation:

    "johnnie walker bl*"

Like the `match_phrase` query, it accepts a `slop` parameter (see <<slop>>) to
make the word order and relative positions ((("slop parameter", "match_prhase_prefix query")))((("match_phrase_prefix query", "slop parameter")))somewhat less rigid:

[source,js]
--------------------------------------------------
{
    "match_phrase_prefix" : {
        "brand" : {
            "query": "walker johnnie bl", <1>
            "slop":  10
        }
    }
}
--------------------------------------------------
// SENSE: 130_Partial_Matching/20_Match_phrase_prefix.json

<1> Even though the words are in the wrong order, the query still matches
    because we have set a high enough `slop` value to allow some flexibility
    in word positions.

However, it is always only the last word in the query string that is treated
as a prefix.

Earlier, in <<prefix-query>>, we warned about the perils of the prefix--how
`prefix` queries can be resource intensive.  The same is true in this
case.((("match_phrase_prefix query", "caution with")))  A prefix of `a` could match hundreds of thousands of terms. Not only
would matching on this many terms be resource intensive, but it would also not be
useful to the user.

We can limit the impact ((("match_phrase_prefix query", "max_expansions")))((("max_expansions parameter")))of the prefix expansion by setting `max_expansions` to
a reasonable number, such as 50:

[source,js]
--------------------------------------------------
{
    "match_phrase_prefix" : {
        "brand" : {
            "query":          "johnnie walker bl",
            "max_expansions": 50
        }
    }
}
--------------------------------------------------
// SENSE: 130_Partial_Matching/20_Match_phrase_prefix.json

The `max_expansions` parameter controls how many terms the prefix is allowed
to match.  It will find the first term starting with `bl` and keep collecting
terms (in alphabetical order) until it either runs out of terms with prefix
`bl`, or it has more terms than `max_expansions`.

Don't forget that we have to run this query every time the user types another
character, so it needs to be fast.  If the first set of results isn't what users are after, they'll keep typing until they get the results that they want.

