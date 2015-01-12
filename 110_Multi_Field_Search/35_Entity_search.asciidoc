=== Cross-fields Entity Search

Now we come to a common pattern: cross-fields entity search. ((("cross-fields entity search")))((("multifield search", "cross-fields entity search"))) With entities
like `person`, `product`, or `address`, the identifying information is spread
across several fields.  We may have a `person` indexed as follows:

[source,js]
--------------------------------------------------
{
    "firstname":  "Peter",
    "lastname":   "Smith"
}
--------------------------------------------------

Or an address like this:

[source,js]
--------------------------------------------------
{
    "street":   "5 Poland Street",
    "city":     "London",
    "country":  "United Kingdom",
    "postcode": "W1V 3DG"
}
--------------------------------------------------

This sounds a lot like the example we described in <<multi-query-strings>>,
but there is a big difference between these two scenarios.  In
<<multi-query-strings>>, we used a separate query string for each field. In
this scenario, we want to search across multiple fields with a _single_ query
string.

Our user might search for the person ``Peter Smith'' or for the address
``Poland Street W1V.'' Each of those words appears in a different field, so
using a `dis_max` / `best_fields` query to find the _single_ best-matching
field is clearly the wrong approach.

==== A Naive Approach

Really, we want to query each field in turn and add up the scores of every
field that matches, which sounds like a job for the `bool` query:

[source,js]
--------------------------------------------------
{
  "query": {
    "bool": {
      "should": [
        { "match": { "street":    "Poland Street W1V" }},
        { "match": { "city":      "Poland Street W1V" }},
        { "match": { "country":   "Poland Street W1V" }},
        { "match": { "postcode":  "Poland Street W1V" }}
      ]
    }
  }
}
--------------------------------------------------

Repeating the query string for every field soon becomes tedious. We can use
the `multi_match` query instead, ((("most fields queries", "problems for entity search")))((("multi_match queries", "most_fields type")))and set the `type` to `most_fields` to tell it to
combine the scores of all matching fields:

[source,js]
--------------------------------------------------
{
  "query": {
    "multi_match": {
      "query":       "Poland Street W1V",
      "type":        "most_fields",
      "fields":      [ "street", "city", "country", "postcode" ]
    }
  }
}
--------------------------------------------------

==== Problems with the most_fields Approach

The `most_fields` approach to entity search has some problems that are not
immediately obvious:

* It is designed to find the most fields matching _any_ words, rather than to
  find the most matching words _across all fields_.

* It can't use the `operator` or `minimum_should_match` parameters
  to reduce the long tail of less-relevant results.

* Term frequencies are different in each field and could interfere with each
  other to produce badly ordered results.



