=== cross-fields Queries

The custom `_all` approach is a good solution, as long as you thought
about setting it up before you indexed your((("multifield search", "cross-fields queries")))((("cross-fields queries"))) documents. However, Elasticsearch
also provides a search-time solution to the problem: the `multi_match` query
with type `cross_fields`.((("multi_match queries", "cross_fields type")))
The `cross_fields` type takes a term-centric approach, quite different from the
field-centric approach taken by `best_fields` and `most_fields`. It treats all
of the fields as one big field, and looks for _each term_ in _any field_.

To illustrate the difference between field-centric and term-centric queries,
look at ((("field-centric queries", "differences between term-centric queries and")))((("most fields queries", "explanation for field-centric approach")))the `explanation` for this field-centric `most_fields` query:

[source,js]
--------------------------------------------------
GET /_validate/query?explain
{
    "query": {
        "multi_match": {
            "query":       "peter smith",
            "type":        "most_fields",
            "operator":    "and", <1>
            "fields":      [ "first_name", "last_name" ]
        }
    }
}
--------------------------------------------------
// SENSE: 110_Multi_Field_Search/50_Cross_field.json

<1> All terms are required.

For a document to match, both `peter` and `smith` must appear in the same
field, either the `first_name` field or the `last_name` field:

    (+first_name:peter +first_name:smith)
    (+last_name:peter  +last_name:smith)

A _term-centric_ approach would use this logic instead:

    +(first_name:peter last_name:peter)
    +(first_name:smith last_name:smith)

In other words, the term `peter` must appear in either field, and the term
`smith` must appear in either field.

The `cross_fields` type first analyzes the query string to produce a list of
terms, and then it searches for each term in any field. That difference alone
solves two of the three problems that we listed in <<field-centric>>, leaving
us just with the issue of differing inverse document frequencies.

Fortunately, the `cross_fields` type solves this too, as can be seen from this
`validate-query` request:

[source,js]
--------------------------------------------------
GET /_validate/query?explain
{
    "query": {
        "multi_match": {
            "query":       "peter smith",
            "type":        "cross_fields", <1>
            "operator":    "and",
            "fields":      [ "first_name", "last_name" ]
        }
    }
}
--------------------------------------------------
// SENSE: 110_Multi_Field_Search/50_Cross_field.json

<1> Use `cross_fields` term-centric matching.

It solves the term-frequency problem by _blending_ inverse document
frequencies across fields: ((("cross-fields queries", "blending inverse document frequencies across fields")))((("inverse document frequency", "blending across fields in cross-fields queries")))

    +blended("peter", fields: [first_name, last_name])
    +blended("smith", fields: [first_name, last_name])

In other words, it looks up the IDF of `smith` in both the `first_name` and
the `last_name` fields and uses the minimum of the two as the IDF for both
fields.  The fact that `smith` is a common last name means that it will be
treated as a common first name too.

[NOTE]
==================================================
For the `cross_fields` query type to work optimally, all fields should have
the same analyzer.((("analyzers", "in cross-fields queries")))((("cross-fields queries", "analyzers in")))  Fields that share an analyzer are grouped together as
blended fields.

If you include fields with a different analysis chain, they will be  added to
the query in the same way as for `best_fields`.  For instance, if we added the
`title` field to the preceding query (assuming it uses a different analyzer), the
explanation would be as follows:

    (+title:peter +title:smith)
    (
      +blended("peter", fields: [first_name, last_name])
      +blended("smith", fields: [first_name, last_name])
    )

This is particularly important when using the `minimum_should_match` and
`operator` parameters.
==================================================

==== Per-Field Boosting

One of the advantages of using the `cross_fields` query over
<<custom-all,custom `_all` fields>> is that you ((("cross-fields queries", "per-field boosting")))((("boosting", "per-field boosting in cross-fields queries")))can boost individual
fields at query time.

For fields of equal value like `first_name` and `last_name`, this generally
isn't required, but if you were searching for books using the `title` and
`description` fields, you might want to give more weight to the `title` field.
This can be done as described before with the caret (`^`) syntax:

[source,js]
--------------------------------------------------
GET /books/_search
{
    "query": {
        "multi_match": {
            "query":       "peter smith",
            "type":        "cross_fields",
            "fields":      [ "title^2", "description" ] <1>
        }
    }
}
--------------------------------------------------

<1> The `title` field has a boost of `2`, while the `description` field
    has the default boost of `1`.

The advantage of being able to boost individual fields should be weighed
against the cost of querying multiple fields instead of querying a single
custom `_all` field. Use whichever of the two solutions that delivers the most
bang for your buck.

