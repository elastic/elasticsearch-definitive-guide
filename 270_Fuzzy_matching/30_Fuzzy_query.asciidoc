[[fuzzy-query]]
=== Fuzzy Query

The http://bit.ly/1ymh8Cu[`fuzzy` query] is ((("typoes and misspellings", "fuzzy query")))((("fuzzy queries")))the fuzzy equivalent of
the `term` query. You will seldom use it directly yourself, but understanding
how it works will help you to use fuzziness in the higher-level `match` query.

To understand how it works, we will first index some documents:

[source,json]
-----------------------------------
POST /my_index/my_type/_bulk
{ "index": { "_id": 1 }}
{ "text": "Surprise me!"}
{ "index": { "_id": 2 }}
{ "text": "That was surprising."}
{ "index": { "_id": 3 }}
{ "text": "I wasn't surprised."}
-----------------------------------

Now we can run a `fuzzy` query for the term `surprize`:

[source,json]
-----------------------------------
GET /my_index/my_type/_search
{
  "query": {
    "fuzzy": {
      "text": "surprize"
    }
  }
}
-----------------------------------

The `fuzzy` query is a term-level query, so it doesn't do any analysis.  It
takes a single term and finds all terms in the term dictionary that are
within the specified `fuzziness`. The default `fuzziness` is `AUTO`.

In our example, `surprize` is within an edit distance of 2 from both
`surprise` and `surprised`, so documents 1 and 3 match. We could reduce the
matches to just `surprise` with the following query:

[source,json]
-----------------------------------
GET /my_index/my_type/_search
{
  "query": {
    "fuzzy": {
      "text": {
        "value": "surprize",
        "fuzziness": 1
      }
    }
  }
}
-----------------------------------

==== Improving Performance

The `fuzzy` query works by taking the original term and building a
_Levenshtein automaton_&#x2014;like a((("fuzzy queries", "improving performance")))((("Levenshtein automation"))) big graph representing all the strings
that are within the specified edit distance of the original string.

The fuzzy query then uses the automation to step efficiently through all of the terms
in the term dictionary to see if they match.  Once it has collected all of the
matching terms that exist in the term dictionary, it can compute the list of
matching documents.

Of course, depending on the type of data stored in the index, a fuzzy query
with an edit distance of 2 can match a very large number of terms and
perform very badly. Two parameters can be used to limit the
performance impact:

`prefix_length`::

The number of initial characters((("prefix_length parameter"))) that will not be ``fuzzified.''  Most
spelling errors occur toward the end of the word, not toward the beginning.
By using a `prefix_length` of `3`, for example, you can signficantly reduce
the number of matching terms.

`max_expansions`::

If a fuzzy query expands to three or four fuzzy options,((("max_expansions parameter"))) the new options may be
meaningful.  If it produces 1,000 options, they are essentially
meaningless.  Use `max_expansions` to limit the total number of options that
will be produced. The fuzzy query will collect matching terms until it
runs out of terms or reaches the `max_expansions` limit.

