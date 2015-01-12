=== Exact-Value Fields

The final topic that we should touch on before leaving multifield queries is
that of exact-value `not_analyzed` fields. ((("not_analyzed fields", "exact value, in multi-field queries")))((("multifield search", "exact value fields")))((("exact values", "exact value not_analyzed fields in multifield search")))((("analyzed fields", "avoiding mixing with not analyzed fields in multi_match queries"))) It is not useful to mix
`not_analyzed` fields with `analyzed` fields in `multi_match` queries.

The reason for this can be demonstrated easily by looking at a query
explanation.  Imagine that we have set the `title` field to be `not_analyzed`:

[source,js]
--------------------------------------------------
GET /_validate/query?explain
{
    "query": {
        "multi_match": {
            "query":       "peter smith",
            "type":        "cross_fields",
            "fields":      [ "title", "first_name", "last_name" ]
        }
    }
}
--------------------------------------------------
// SENSE: 110_Multi_Field_Search/55_Not_analyzed.json

Because the `title` field is not analyzed, it searches that field for a single
term consisting of the whole query string!

    title:peter smith
    (
        blended("peter", fields: [first_name, last_name])
        blended("smith", fields: [first_name, last_name])
    )

That term clearly does not exist in the inverted index of the `title` field,
and can never be found. Avoid using `not_analyzed` fields in `multi_match`
queries.
