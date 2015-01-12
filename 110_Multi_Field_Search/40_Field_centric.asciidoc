[[field-centric]]
=== Field-Centric Queries

All three of the preceding problems stem from  ((("field-centric queries")))((("multifield search", "field-centric queries, problems with")))((("most fields queries", "problems with field-centric queries")))`most_fields` being
_field-centric_ rather than _term-centric_: it looks for the  most matching
_fields_, when really what we're interested is the most matching _terms_.


NOTE: The `best_fields` type is also field-centric((("best fields queries", "problems with field-centric queries"))) and suffers from similar problems.


First we'll look at why these problems exist, and then how we can combat them.

==== Problem 1: Matching the Same Word in Multiple Fields

Think about how the `most_fields` query is executed: Elasticsearch generates a
separate `match` query for each field and then wraps these match queries in an outer `bool` query.

We can see this by passing our query through the `validate-query` API:

[source,js]
--------------------------------------------------
GET /_validate/query?explain
{
  "query": {
    "multi_match": {
      "query":   "Poland Street W1V",
      "type":    "most_fields",
      "fields":  [ "street", "city", "country", "postcode" ]
    }
  }
}
--------------------------------------------------
// SENSE: 110_Multi_Field_Search/40_Entity_search_problems.json

which yields this `explanation`:

    (street:poland   street:street   street:w1v)
    (city:poland     city:street     city:w1v)
    (country:poland  country:street  country:w1v)
    (postcode:poland postcode:street postcode:w1v)


You can see that a document matching just the word `poland` in _two_ fields
could score higher than a document matching `poland` and `street` in one
field.

==== Problem 2: Trimming the Long Tail

In <<match-precision>>, we talked about((("and operator", "most fields and best fields queries and")))((("minimum_should_match parameter", "most fields and best fields queries"))) using the `and` operator or the
`minimum_should_match` parameter to trim the long tail of almost irrelevant
results. Perhaps we could try this:

[source,js]
--------------------------------------------------
{
    "query": {
        "multi_match": {
            "query":       "Poland Street W1V",
            "type":        "most_fields",
            "operator":    "and", <1>
            "fields":      [ "street", "city", "country", "postcode" ]
        }
    }
}
--------------------------------------------------
// SENSE: 110_Multi_Field_Search/40_Entity_search_problems.json

<1> All terms must be present.

However, with `best_fields` or `most_fields`, these parameters are passed down
to the generated `match` queries. The `explanation` for this query shows the
following:

    (+street:poland   +street:street   +street:w1v)
    (+city:poland     +city:street     +city:w1v)
    (+country:poland  +country:street  +country:w1v)
    (+postcode:poland +postcode:street +postcode:w1v)

In other words, using the `and` operator means that all words must exist _in
the same field_, which is clearly wrong! It is unlikely that any documents
would match this query.

==== Problem 3: Term Frequencies

In <<relevance-intro>>, we explained that the default similarity algorithm
used to calculate the relevance score ((("term frequency", "problems with field-centric queries")))for each term is TF/IDF:

Term frequency::

    The more often a term appears in a field in a single document, the more
    relevant the document.

Inverse document frequency::

    The more often a term appears in a field in all documents in the index,
    the less relevant is that term.

When searching against multiple fields, TF/IDF can((("Term Frequency/Inverse Document Frequency  (TF/IDF) similarity algorithm", "surprising results when searching against multiple fields"))) introduce some surprising
results.

Consider our example of searching for ``Peter Smith'' using the `first_name`
and `last_name` fields.((("inverse document frequency", "field-centric queries and")))  Peter is a common first name and Smith is a common
last name--both will have low IDFs.  But what if we have another person in
the index whose name is Smith Williams?  Smith as a first name is very
uncommon and so will have a high IDF!

A simple query like the following may well return Smith Williams above
Peter Smith in spite of the fact that the second person is a better match
than the first.

[source,js]
--------------------------------------------------
{
    "query": {
        "multi_match": {
            "query":       "Peter Smith",
            "type":        "most_fields",
            "fields":      [ "*_name" ]
        }
    }
}
--------------------------------------------------
// SENSE: 110_Multi_Field_Search/40_Bad_frequencies.json

The high IDF of `smith` in the first name field can overwhelm the two low IDFs
of `peter` as a first name and `smith` as a last name.

==== Solution

These problems only exist because we are dealing with multiple fields. If we
were to combine all of these fields into a single field, the problems would
vanish. We could achieve this by adding a `full_name` field to our `person`
document:

[source,js]
--------------------------------------------------
{
    "first_name":  "Peter",
    "last_name":   "Smith",
    "full_name":   "Peter Smith"
}
--------------------------------------------------

When querying just the `full_name` field:

* Documents with more matching words would trump documents with the same word
  repeated.

* The `minimum_should_match` and `operator` parameters would function as
  expected.

* The inverse document frequencies for first and last names would be combined
  so it wouldn't matter whether Smith were a first or last name anymore.

While this would work, we don't like having to store redundant data.  Instead,
Elasticsearch offers us two solutions--one at index time and one at search
time--which we discuss next.
