[[fuzzy-match-query]]
=== Fuzzy match Query

The `match` query supports ((("typoes and misspellings", "fuzzy match query")))((("match query", "fuzzy matching")))((("fuzzy matching", "match query")))fuzzy matching out of the box:

[source,json]
-----------------------------------
GET /my_index/my_type/_search
{
  "query": {
    "match": {
      "text": {
        "query":     "SURPRIZE ME!",
        "fuzziness": "AUTO",
        "operator":  "and"
      }
    }
  }
}
-----------------------------------

The query string is first analyzed, to produce the terms `[surprize, me]`, and
then each term is fuzzified using the specified `fuzziness`.

Similarly, the `multi_match` query also ((("multi_match queries", "fuzziness support")))supports `fuzziness`, but only when
executing with type `best_fields` or `most_fields`:

[source,json]
-----------------------------------
GET /my_index/my_type/_search
{
  "query": {
    "multi_match": {
      "fields":  [ "text", "title" ],
      "query":     "SURPRIZE ME!",
      "fuzziness": "AUTO"
    }
  }
}
-----------------------------------

Both the `match` and `multi_match` queries  also support the `prefix_length`
and `max_expansions` parameters.

TIP: Fuzziness works only with the basic `match` and `multi_match` queries. It
doesn't work with phrase matching, common terms, or `cross_fields` matches.

