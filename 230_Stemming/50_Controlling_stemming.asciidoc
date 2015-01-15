[[controlling-stemming]]
=== Controlling Stemming

Out-of-the-box stemming solutions are never perfect.((("stemming words", "controlling stemming")))  Algorithmic stemmers,
especially, will blithely apply their rules to any words they encounter,
perhaps conflating words that you would prefer to keep separate.  Maybe, for
your use case, it is important to keep `skies` and `skiing` as distinct words
rather than stemming them both down to `ski` (as would happen with the
`english` analyzer).

The http://bit.ly/1IOeXZD[`keyword_marker`] and
http://bit.ly/1ymcioJ[`stemmer_override`] token filters((("stemmer_override token filter")))((("keyword_marker token filter")))
allow us to customize the stemming process.

[[preventing-stemming]]
==== Preventing Stemming

The <<stem-exclusion,`stem_exclusion`>> parameter for language analyzers (see
<<configuring-language-analyzers>>) allowed ((("stemming words", "controlling stemming", "preventing stemming")))us to specify a list of words that
should not be stemmed.  Internally, these language analyzers use the
http://bit.ly/1IOeXZD[`keyword_marker` token filter]
to mark the listed words as _keywords_, which prevents subsequent stemming
token filters from touching those words.((("keyword_marker token filter", "preventing stemming of certain words")))

For instance, we can create a simple custom analyzer that uses the
http://bit.ly/17LseXy[`porter_stem`] token filter,
but prevents the word `skies` from((("porter_stem token filter"))) being stemmed:

[source,json]
------------------------------------------
PUT /my_index
{
  "settings": {
    "analysis": {
      "filter": {
        "no_stem": {
          "type": "keyword_marker",
          "keywords": [ "skies" ] <1>
        }
      },
      "analyzer": {
        "my_english": {
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "no_stem",
            "porter_stem"
          ]
        }
      }
    }
  }
}
------------------------------------------
<1> They `keywords` parameter could accept multiple words.

Testing it with the `analyze` API shows that just the word `skies` has
been excluded from stemming:

[source,json]
------------------------------------------
GET /my_index/_analyze?analyzer=my_english
sky skies skiing skis <1>
------------------------------------------
<1> Returns: `sky`, `skies`, `ski`, `ski`

[[keyword-path]]

[TIP]
==========================================

While the language analyzers allow ((("language analyzers", "stem_exclusion parameter")))us only to specify an array of words in the
`stem_exclusion` parameter, the `keyword_marker` token filter also accepts a
`keywords_path` parameter that allows us to store all of our keywords in a
file. ((("keyword_marker token filter", "keywords_path parameter")))The file should contain one word per line, and must be present on every
node in the cluster. See <<updating-stopwords>> for tips on how to update this
file.

==========================================

[[customizing-stemming]]
==== Customizing Stemming

In the preceding example, we prevented `skies` from being stemmed, but perhaps we
would prefer it to be stemmed to `sky` instead.((("stemming words", "controlling stemming", "customizing stemming")))  The
http://bit.ly/1ymcioJ[`stemmer_override`] token
filter allows us ((("stemmer_override token filter")))to specify our own custom stemming rules. At the same time,
we can handle some irregular forms like stemming `mice` to `mouse` and `feet`
to `foot`:

[source,json]
------------------------------------------
PUT /my_index
{
  "settings": {
    "analysis": {
      "filter": {
        "custom_stem": {
          "type": "stemmer_override",
          "rules": [ <1>
            "skies=>sky",
            "mice=>mouse",
            "feet=>foot"
          ]
        }
      },
      "analyzer": {
        "my_english": {
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "custom_stem", <2>
            "porter_stem"
          ]
        }
      }
    }
  }
}

GET /my_index/_analyze?analyzer=my_english
The mice came down from the skies and ran over my feet <3>
------------------------------------------
<1> Rules take the form `original=>stem`.
<2> The `stemmer_override` filter must be placed before the stemmer.
<3> Returns `the`, `mouse`, `came`, `down`, `from`, `the`, `sky`,
    `and`, `ran`, `over`, `my`, `foot`.

TIP: Just as for the `keyword_marker` token filter, rules can be stored
in a file whose location should be specified with the `rules_path`
parameter.
