[[configuring-analyzers]]
=== Configuring Analyzers

The third important index setting is the `analysis` section,((("index settings", "analysis"))) which is used
to configure existing analyzers or to create new custom analyzers
specific to your index.

In <<analysis-intro>>, we introduced some of the built-in ((("analyzers", "built-in")))analyzers,
which are used to convert full-text strings into an inverted index,
suitable for searching.

The `standard` analyzer, which is the default analyzer
used for full-text fields,((("standard analyzer", "components of"))) is a good choice for most Western languages.((("tokenization", "in standard analyzer")))((("standard token filter")))((("stop token filter")))((("standard tokenizer")))((("lowercase token filter")))
It consists of the following:

* The `standard` tokenizer, which splits the input text on word boundaries
* The `standard` token filter, which is intended to tidy up the tokens
  emitted by the tokenizer (but currently does nothing)
* The `lowercase` token filter, which converts all tokens into lowercase
* The `stop` token filter, which removes stopwords--common words
  that have little impact on search relevance, such as `a`, `the`, `and`,
  `is`.

By default, the stopwords filter is disabled.  You can enable it by creating a
custom analyzer based on the `standard` analyzer and setting the `stopwords`
parameter.((("stopwords parameter"))) Either provide a list of stopwords or tell it to use a predefined
stopwords list from a particular language.

In the following example, we create a new analyzer called the `es_std`
analyzer, which uses the predefined list of ((("Spanish", "analyzer using Spanish stopwords")))Spanish stopwords:

[source,js]
--------------------------------------------------
PUT /spanish_docs
{
    "settings": {
        "analysis": {
            "analyzer": {
                "es_std": {
                    "type":      "standard",
                    "stopwords": "_spanish_"
                }
            }
        }
    }
}
--------------------------------------------------
// SENSE: 070_Index_Mgmt/15_Configure_Analyzer.json

The `es_std` analyzer is not global--it exists only in the `spanish_docs`
index where we have defined it. To test it with the `analyze` API, we must
specify the index name:

[source,js]
--------------------------------------------------
GET /spanish_docs/_analyze?analyzer=es_std
El veloz zorro marrón
--------------------------------------------------
// SENSE: 070_Index_Mgmt/15_Configure_Analyzer.json

The abbreviated results show that the Spanish stopword `El` has been
removed correctly:

[source,js]
--------------------------------------------------
{
  "tokens" : [
    { "token" :    "veloz",   "position" : 2 },
    { "token" :    "zorro",   "position" : 3 },
    { "token" :    "marrón",  "position" : 4 }
  ]
}
--------------------------------------------------

