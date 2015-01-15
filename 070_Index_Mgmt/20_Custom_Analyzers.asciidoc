[[custom-analyzers]]
=== Custom Analyzers

While Elasticsearch comes with a number of analyzers available out of the box,
the real power comes from the ability to create your own custom analyzers
by combining character filters, tokenizers, and token filters in a
configuration that suits your particular data.

In <<analysis-intro>>, we said that an _analyzer_ is a wrapper that combines
three functions into a single package,((("analyzers", "character filters, tokenizers, and token filters in"))) which are executed in sequence:

Character filters::
+
--
Character filters((("character filters"))) are used to ``tidy up'' a string before it is tokenized.
For instance, if our text is in HTML format, it will contain HTML tags like
`<p>` or `<div>` that we don't want to be indexed. We can use the
http://bit.ly/1B6f4Ay[`html_strip` character filter]
to remove all HTML tags and to convert HTML entities like `&Aacute;` into the
corresponding Unicode character `Á`.

An analyzer may have zero or more character filters.
--

Tokenizers::
+
--
An analyzer _must_ have a single tokenizer.((("tokenizers", "in analyzers")))  The tokenizer breaks up the
string into individual terms or tokens. The
http://bit.ly/1E3Fd1b[`standard` tokenizer],
which is used((("standard tokenizer"))) in the `standard` analyzer, breaks up a string into
individual terms on word boundaries, and removes most punctuation, but
other tokenizers exist that have different behavior.

For instance, the
http://bit.ly/1ICd585[`keyword` tokenizer]
outputs exactly((("keyword tokenizer"))) the same string as it received, without any tokenization. The
http://bit.ly/1xt3t7d[`whitespace` tokenizer]
splits text((("whitespace tokenizer"))) on whitespace only. The
http://bit.ly/1ICdozA[`pattern` tokenizer] can
be used to split text on a ((("pattern tokenizer")))matching regular expression.
--

Token filters::
+
--
After tokenization, the resulting _token stream_ is passed through any
specified token filters,((("token filters"))) in the order in which they are specified.

Token filters may change, add, or remove tokens.  We have already mentioned the
http://bit.ly/1DIeXvZ[`lowercase`] and
http://bit.ly/1INX4tN[`stop` token filters],
but there are many more available in Elasticsearch.
http://bit.ly/1AUfpDN[Stemming token filters]
``stem'' words to ((("stemming token filters")))their root form. The
http://bit.ly/1ylU7Q7[`ascii_folding` filter]
removes diacritics,((("ascii_folding filter"))) converting a term like `"très"` into `"tres"`. The
http://bit.ly/1CbkmYe[`ngram`] and
http://bit.ly/1DIf6j5[`edge_ngram` token filters] can produce((("edge_engram token filter")))((("ngram and edge_ngram token filters")))
tokens suitable for partial matching or autocomplete.
--

In <<search-in-depth>>, we discuss examples of where and how to use these
tokenizers and filters.  But first, we need to explain how to create a custom
analyzer.

==== Creating a Custom Analyzer

In the same way as((("index settings", "analysis", "creating custom analyzers")))((("analyzers", "custom", "creating"))) we configured the `es_std` analyzer previously, we can configure
character filters, tokenizers, and token filters in their respective sections
under `analysis`:

[source,js]
--------------------------------------------------
PUT /my_index
{
    "settings": {
        "analysis": {
            "char_filter": { ... custom character filters ... },
            "tokenizer":   { ...    custom tokenizers     ... },
            "filter":      { ...   custom token filters   ... },
            "analyzer":    { ...    custom analyzers      ... }
        }
    }
}
--------------------------------------------------


As an example, let's set up a custom analyzer that will do the following:

1. Strip out HTML by using the `html_strip` character filter.

2. Replace `&` characters with `" and "`, using a custom `mapping`
   character filter:
+
[source,js]
--------------------------------------------------
"char_filter": {
    "&_to_and": {
        "type":       "mapping",
        "mappings": [ "&=> and "]
    }
}
--------------------------------------------------


3. Tokenize words, using the `standard` tokenizer.

4. Lowercase terms, using the `lowercase` token filter.

5. Remove a custom list of stopwords, using a custom `stop` token filter:
+
[source,js]
--------------------------------------------------
"filter": {
    "my_stopwords": {
        "type":        "stop",
        "stopwords": [ "the", "a" ]
    }
}
--------------------------------------------------

Our analyzer definition combines the predefined tokenizer and filters with the
custom filters that we have configured previously:

[source,js]
--------------------------------------------------
"analyzer": {
    "my_analyzer": {
        "type":           "custom",
        "char_filter":  [ "html_strip", "&_to_and" ],
        "tokenizer":      "standard",
        "filter":       [ "lowercase", "my_stopwords" ]
    }
}
--------------------------------------------------


To put it all together, the whole `create-index` request((("create-index request"))) looks like this:

[source,js]
--------------------------------------------------
PUT /my_index
{
    "settings": {
        "analysis": {
            "char_filter": {
                "&_to_and": {
                    "type":       "mapping",
                    "mappings": [ "&=> and "]
            }},
            "filter": {
                "my_stopwords": {
                    "type":       "stop",
                    "stopwords": [ "the", "a" ]
            }},
            "analyzer": {
                "my_analyzer": {
                    "type":         "custom",
                    "char_filter":  [ "html_strip", "&_to_and" ],
                    "tokenizer":    "standard",
                    "filter":       [ "lowercase", "my_stopwords" ]
            }}
}}}
--------------------------------------------------
// SENSE: 070_Index_Mgmt/20_Custom_analyzer.json


After creating the index, use the `analyze` API to((("analyzers", "testing using analyze API"))) test the new analyzer:

[source,js]
--------------------------------------------------
GET /my_index/_analyze?analyzer=my_analyzer
The quick & brown fox
--------------------------------------------------
// SENSE: 070_Index_Mgmt/20_Custom_analyzer.json


The following abbreviated results show that our analyzer is working correctly:

[source,js]
--------------------------------------------------
{
  "tokens" : [
      { "token" :   "quick",    "position" : 2 },
      { "token" :   "and",      "position" : 3 },
      { "token" :   "brown",    "position" : 4 },
      { "token" :   "fox",      "position" : 5 }
    ]
}
--------------------------------------------------

The analyzer is not much use unless we tell ((("analyzers", "custom", "telling Elasticsearch where to use")))((("mapping (types)", "applying custom analyzer to a string field")))Elasticsearch where to use it. We
can apply it to a `string` field with a mapping such as the following:

[source,js]
--------------------------------------------------
PUT /my_index/_mapping/my_type
{
    "properties": {
        "title": {
            "type":      "string",
            "analyzer":  "my_analyzer"
        }
    }
}
--------------------------------------------------
// SENSE: 070_Index_Mgmt/20_Custom_analyzer.json


