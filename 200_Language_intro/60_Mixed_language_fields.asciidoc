[[mixed-lang-fields]]
=== Mixed-Language Fields

Usually, documents that mix multiple languages in a single field come from
sources beyond your control, such as((("languages", "mixed language fields")))((("fields", "mixed language"))) pages scraped from the Web:

[source,js]
--------------------------------------------------
{ "body": "Page not found / Seite nicht gefunden / Page non trouvée" }
--------------------------------------------------

They are the most difficult type of multilingual document to handle correctly.
Although you can simply use the `standard` analyzer on all fields, your documents
will be less searchable than if you had used an appropriate stemmer. But of
course, you can't choose just one stemmer--stemmers are language specific.
Or rather, stemmers are language and script specific.  As discussed in
<<different-scripts>>, if every language uses a different script, then
stemmers can be combined.

Assuming that your mix of languages uses the same script such as Latin, you have three choices available to you:

* Split into separate fields
* Analyze multiple times
* Use n-grams

==== Split into Separate Fields

The Compact Language Detector ((("languages", "mixed language fields", "splitting into separate fields")))((("Compact Language Detector (CLD)")))mentioned in <<identifying-language>> can tell
you which parts of the document are in which language.  You can split up the
text based on language and use the same approach as was used in
<<one-lang-fields>>.

==== Analyze Multiple Times

If you primarily deal with a limited number of languages, ((("languages", "mixed language fields", "analyzing multiple times")))((("analyzers", "for mixed language fields")))((("multifields", "analying mixed language fields")))you could use
multi-fields to analyze the text once per language:

[source,js]
--------------------------------------------------
PUT /movies
{
  "mappings": {
    "title": {
      "properties": {
        "title": { <1>
          "type": "string",
          "fields": {
            "de": { <2>
              "type":     "string",
              "analyzer": "german"
            },
            "en": { <2>
              "type":     "string",
              "analyzer": "english"
            },
            "fr": { <2>
              "type":     "string",
              "analyzer": "french"
            },
            "es": { <2>
              "type":     "string",
              "analyzer": "spanish"
            }
          }
        }
      }
    }
  }
}
--------------------------------------------------
<1> The main `title` field uses the `standard` analyzer.
<2> Each subfield applies a different language analyzer
    to the text in the `title` field.

==== Use n-grams

You could index all words as n-grams, using the ((("n-grams", "for mixed language fields")))((("languages", "mixed language fields", "n-grams, indexing words as")))same approach as
described in <<ngrams-compound-words>>.  Most inflections involve adding a
suffix (or in some languages, a prefix) to a word, so by breaking each word into n-grams, you have a good chance of matching words that are similar
but not exactly the same. This can be combined with the _analyze-multiple
times_ approach to provide a catchall field for unsupported languages:

[source,js]
--------------------------------------------------
PUT /movies
{
  "settings": {
    "analysis": {...} <1>
  },
  "mappings": {
    "title": {
      "properties": {
        "title": {
          "type": "string",
          "fields": {
            "de": {
              "type":     "string",
              "analyzer": "german"
            },
            "en": {
              "type":     "string",
              "analyzer": "english"
            },
            "fr": {
              "type":     "string",
              "analyzer": "french"
            },
            "es": {
              "type":     "string",
              "analyzer": "spanish"
            },
            "general": { <2>
              "type":     "string",
              "analyzer": "trigrams"
            }
          }
        }
      }
    }
  }
}
--------------------------------------------------
<1> In the `analysis` section, we define the same `trigrams`
    analyzer as described in <<ngrams-compound-words>>.
<2> The `title.general` field uses the `trigrams` analyzer
    to index any language.

When querying the catchall `general` field, you can use
`minimum_should_match` to reduce the number of low-quality matches.  It may
also be necessary to boost the other fields slightly more than the `general`
field, so that matches on the the main language fields are given more weight
than those on the `general` field:

[source,js]
--------------------------------------------------
GET /movies/movie/_search
{
    "query": {
        "multi_match": {
            "query":    "club de la lucha",
            "fields": [ "title*^1.5", "title.general" ], <1>
            "type":     "most_fields",
            "minimum_should_match": "75%" <2>
        }
    }
}
--------------------------------------------------
<1> All `title` or `title.*` fields are given a slight boost over the
    `title.general` field.
<2> The `minimum_should_match` parameter reduces the number of low-quality matches returned, especially important for the `title.general` field.


