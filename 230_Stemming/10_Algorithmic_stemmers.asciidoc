[[algorithmic-stemmers]]
=== Algorithmic Stemmers

Most of the stemmers available in Elasticsearch are algorithmic((("stemming words", "algorithmic stemmers"))) in that they
apply a series of rules to a word in order to reduce it to its root form, such
as stripping the final `s` or `es` from plurals.   They don't have to know
anything about individual words in order to stem them.

These algorithmic stemmers have the advantage that they are available out of
the box, are fast, use little memory, and work well for regular words.  The
downside is that they don't cope well with irregular words like `be`, `are`,
and `am`, or `mice` and `mouse`.

One of the earliest stemming algorithms((("English", "stemmers for")))((("Porter stemmer for English"))) is the Porter stemmer for English,
which is still the recommended English stemmer today.  Martin Porter
subsequently went on to create the
http://snowball.tartarus.org/[Snowball language] for creating stemming
algorithms, and a number((("Snowball langauge (stemmers)"))) of the stemmers available in Elasticsearch are
written in Snowball.

[TIP]
==================================================

The http://bit.ly/1IObUjZ[`kstem` token filter] is a stemmer
for English which((("kstem token filter"))) combines the algorithmic approach with a built-in
dictionary. The dictionary contains a list of root words and exceptions in
order to avoid conflating words incorrectly. `kstem` tends to stem less
aggressively than the Porter stemmer.

==================================================

==== Using an Algorithmic Stemmer

While you ((("stemming words", "algorithmic stemmers", "using")))can use the
http://bit.ly/17LseXy[`porter_stem`] or
http://bit.ly/1IObUjZ[`kstem`] token filter directly, or
create a language-specific Snowball stemmer with the
http://bit.ly/1Cr4tNI[`snowball`] token filter, all of the
algorithmic stemmers are exposed via a single unified interface:
the http://bit.ly/1AUfpDN[`stemmer` token filter], which
accepts the `language` parameter.

For instance, perhaps you find the default stemmer used by the `english`
analyzer to be too aggressive and ((("english analyzer", "default stemmer, examining")))you want to make it less aggressive.
The first step is to look up the configuration for the `english` analyzer
in the http://bit.ly/1xtdoJV[language analyzers]
documentation, which shows the following:

[source,js]
--------------------------------------------------
{
  "settings": {
    "analysis": {
      "filter": {
        "english_stop": {
          "type":       "stop",
          "stopwords":  "_english_"
        },
        "english_keywords": {
          "type":       "keyword_marker", <1>
          "keywords":   []
        },
        "english_stemmer": {
          "type":       "stemmer",
          "language":   "english" <2>
        },
        "english_possessive_stemmer": {
          "type":       "stemmer",
          "language":   "possessive_english" <2>
        }
      },
      "analyzer": {
        "english": {
          "tokenizer":  "standard",
          "filter": [
            "english_possessive_stemmer",
            "lowercase",
            "english_stop",
            "english_keywords",
            "english_stemmer"
          ]
        }
      }
    }
  }
}
--------------------------------------------------
<1> The `keyword_marker` token filter lists words that should not be
    stemmed.((("keyword_marker token filter")))  This defaults to the empty list.

<2> The `english` analyzer uses two stemmers: the `possessive_english`
    and the `english` stemmer. The ((("english stemmer")))((("possessive_english stemmer")))possessive stemmer removes `'s`
    from any words before passing them on to the `english_stop`,
    `english_keywords`, and `english_stemmer`.

Having reviewed the current configuration, we can use it as the basis for
a new analyzer, with((("english analyzer", "customizing the stemmer"))) the following changes:

*   Change the `english_stemmer` from `english` (which maps to the
    http://bit.ly/17LseXy[`porter_stem`] token filter)
    to `light_english` (which maps to the less aggressive
    http://bit.ly/1IObUjZ[`kstem`] token filter).

*   Add the <<asciifolding-token-filter,`asciifolding`>> token filter to
    remove any diacritics from foreign words.((("asciifolding token filter")))

*   Remove the `keyword_marker` token filter, as we don't need it.
    (We discuss this in more detail in <<controlling-stemming>>.)

Our new custom analyzer would look like this:

[source,js]
--------------------------------------------------
PUT /my_index
{
  "settings": {
    "analysis": {
      "filter": {
        "english_stop": {
          "type":       "stop",
          "stopwords":  "_english_"
        },
        "light_english_stemmer": {
          "type":       "stemmer",
          "language":   "light_english" <1>
        },
        "english_possessive_stemmer": {
          "type":       "stemmer",
          "language":   "possessive_english"
        }
      },
      "analyzer": {
        "english": {
          "tokenizer":  "standard",
          "filter": [
            "english_possessive_stemmer",
            "lowercase",
            "english_stop",
            "light_english_stemmer", <1>
            "asciifolding" <2>
          ]
        }
      }
    }
  }
}
--------------------------------------------------
<1> Replaced the `english` stemmer with the less aggressive
    `light_english` stemmer
<2> Added the `asciifolding` token filter

