=== wildcard and regexp Queries

The `wildcard` query is a low-level, term-based query ((("wildcard query")))((("partial matching", "wildcard and regexp queries")))similar in nature to the
`prefix` query, but it allows you to specify a pattern instead of just a prefix.
It uses the standard shell wildcards: `?` matches any character, and `*`
matches zero or more characters.((("postcodes (UK), partial matching with", "wildcard queries")))

This query would match the documents containing `W1F 7HW` and `W2F 8HW`:

[source,js]
--------------------------------------------------
GET /my_index/address/_search
{
    "query": {
        "wildcard": {
            "postcode": "W?F*HW" <1>
        }
    }
}
--------------------------------------------------
// SENSE: 130_Partial_Matching/15_Wildcard_regexp.json

<1> The `?` matches the `1` and the `2`, while the `*` matches the space
    and the `7` and `8`.

Imagine now that you want to match all postcodes just in the `W` area.  A
prefix match would also include postcodes starting with `WC`, and you would
have a similar problem with a wildcard match.  We want to match only postcodes
that begin with a `W`, followed by a number.((("postcodes (UK), partial matching with", "regexp query")))((("regexp query")))  The `regexp` query allows you to
write these more complicated patterns:

[source,js]
--------------------------------------------------
GET /my_index/address/_search
{
    "query": {
        "regexp": {
            "postcode": "W[0-9].+" <1>
        }
    }
}
--------------------------------------------------
// SENSE: 130_Partial_Matching/15_Wildcard_regexp.json

<1> The regular expression says that the term must begin with a `W`, followed
    by any number from 0 to 9, followed by one or more other characters.

The `wildcard` and `regexp` queries work in exactly the same way as the
`prefix` query.  They also have to scan the list of terms in the inverted
index to find all matching terms, and gather document IDs term by term.  The
only difference between them and the `prefix` query is that they support more-complex patterns.

This means that the same caveats apply.  Running these queries on a field with
many unique terms can be resource intensive indeed.  Avoid using a
pattern that starts with a wildcard (for example, `*foo` or, as a regexp, `.*foo`).

Whereas prefix matching can be made more efficient by preparing your data at
index time, wildcard and regular expression matching can be done only
at query time. These queries have their place but should be used sparingly.

[CAUTION]
=================================================

The `prefix`, `wildcard`, and `regexp` queries operate on terms. If you use
them to query an `analyzed` field, they will examine each term in the
field, not the field as a whole.((("prefix query", "on analyzed fields")))((("wildcard query", "on analyzed fields")))((("regexp query", "on analyzed fields")))((("analyzed fields", "prefix, wildcard, and regexp queries on")))

For instance, let's say that our `title` field contains ``Quick brown fox''
which produces the terms `quick`, `brown`, and `fox`.

This query would match:

[source,json]
--------------------------------------------------
{ "regexp": { "title": "br.*" }}
--------------------------------------------------

But neither of these queries would match:

[source,json]
--------------------------------------------------
{ "regexp": { "title": "Qu.*" }} <1>
{ "regexp": { "title": "quick br*" }} <2>
--------------------------------------------------
<1> The term in the index is `quick`, not `Quick`.
<2> `quick` and `brown` are separate terms.

=================================================
