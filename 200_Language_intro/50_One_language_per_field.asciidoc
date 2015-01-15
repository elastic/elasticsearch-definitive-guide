[[one-lang-fields]]
=== One Language per Field

For documents that represent entities like products, movies, or legal notices, it is common((("fields", "one language per field")))((("languages", "one language per field")))
for the same text to be translated into several languages.  Although each translation
could be represented in a single document in an index per language, another
reasonable approach is to keep all translations in the same document:

[source,js]
--------------------------------------------------
{
   "title":     "Fight club",
   "title_br":  "Clube de Luta",
   "title_cz":  "Klub rvácu",
   "title_en":  "Fight club",
   "title_es":  "El club de la lucha",
   ...
}
--------------------------------------------------

Each translation is stored in a separate field, which is analyzed according
to the language it contains:

[source,js]
--------------------------------------------------
PUT /movies
{
  "mappings": {
    "movie": {
      "properties": {
        "title": { <1>
          "type":       "string"
        },
        "title_br": { <2>
            "type":     "string",
            "analyzer": "brazilian"
        },
        "title_cz": { <2>
            "type":     "string",
            "analyzer": "czech"
        },
        "title_en": { <2>
            "type":     "string",
            "analyzer": "english"
        },
        "title_es": { <2>
            "type":     "string",
            "analyzer": "spanish"
        }
      }
    }
  }
}
--------------------------------------------------
<1> The `title` field contains the original title and uses the
    `standard` analyzer.
<2> Each of the other fields uses the appropriate analyzer for
    that language.

Like the _index-per-language_ approach, the _field-per-language_ approach
maintains clean term frequencies. It is not quite as flexible as having
separate indices.  Although it is easy to add a new field by using the <<updating-a-mapping,`update-mapping` API>>, those new fields may require new
custom analyzers, which can only be set up at index creation time.  As a
workaround, you can http://bit.ly/1B6s0WY[close] the index, add the new
analyzers with the http://bit.ly/1zijFPx[`update-settings` API],
then reopen the index, but closing the index means that it will require some
downtime.

The documents of a((("boosting", "query-time", "boosting a field"))) single language can be queried independently, or queries
can target multiple languages by querying multiple fields.  We can even
specify a preference for particular languages by boosting that field:

[source,js]
--------------------------------------------------
GET /movies/movie/_search
{
    "query": {
        "multi_match": {
            "query":    "club de la lucha",
            "fields": [ "title*", "title_es^2" ], <1>
            "type":     "most_fields"
        }
    }
}
--------------------------------------------------
<1> This search queries any field beginning with `title` but
    boosts the `title_es` field by `2`.  All other fields have
    a neutral boost of `1`.

