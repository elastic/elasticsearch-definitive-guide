[[using-stopwords]]
=== Using Stopwords

The removal of stopwords is ((("stopwords", "removal of")))handled by the
http://bit.ly/1INX4tN[`stop` token filter] which can be used
when ((("stop token filter")))creating a `custom` analyzer (see <<stop-token-filter>>).
However, some out-of-the-box analyzers((("analyzers", "stop filter pre-integrated")))((("pattern analyzer", "stopwords and")))((("standard analyzer", "stop filter")))((("language analyzers", "stop filter pre-integrated"))) come with the `stop` filter pre-integrated:

http://bit.ly/1xtdoJV[Language analyzers]::

    Each language analyzer defaults to using the appropriate stopwords list
    for that language. For instance, the `english` analyzer uses the
    `_english_` stopwords list.

http://bit.ly/14EpXv3[`standard` analyzer]::

    Defaults to the empty stopwords list: `_none_`, essentially disabling
    stopwords.

http://bit.ly/1u9OVct[`pattern` analyzer]::

    Defaults to `_none_`, like the `standard` analyzer.

==== Stopwords and the Standard Analyzer

To use custom stopwords in conjunction with ((("standard analyzer", "stopwords and")))((("stopwords", "using with standard analyzer")))the `standard` analyzer, all we
need to do is to create a configured version of the analyzer and pass in the
list of `stopwords` that we require:

[source,json]
---------------------------------
PUT /my_index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_analyzer": { <1>
          "type": "standard", <2>
          "stopwords": [ "and", "the" ] <3>
        }
      }
    }
  }
}
---------------------------------
<1> This is a custom analyzer called `my_analyzer`.
<2> This analyzer is the `standard` analyzer with some custom configuration.
<3> The stopwords to filter out are `and` and `the`.

TIP: This same technique can be used to configure custom stopword lists for
any of the language analyzers.

[[maintaining-positions]]
==== Maintaining Positions

The output from the `analyze` API((("stopwords", "maintaining position of terms and"))) is quite interesting:

[source,json]
---------------------------------
GET /my_index/_analyze?analyzer=my_analyzer
The quick and the dead
---------------------------------

[source,json]
---------------------------------
{
   "tokens": [
      {
         "token":        "quick",
         "start_offset": 4,
         "end_offset":   9,
         "type":         "<ALPHANUM>",
         "position":     2 <1>
      },
      {
         "token":        "dead",
         "start_offset": 18,
         "end_offset":   22,
         "type":         "<ALPHANUM>",
         "position":     5 <1>
      }
   ]
}
---------------------------------
<1> Note the `position` of each token.

The stopwords have been filtered out, as expected, but the interesting part is
that the `position` of the((("phrase matching", "stopwords and", "positions data"))) two remaining terms is unchanged: `quick` is the
second word in the original sentence, and `dead` is the fifth. This is
important for phrase queries--if the positions of each term had been
adjusted, a phrase query for `quick dead` would have matched the preceding
example incorrectly.

[[specifying-stopwords]]
==== Specifying Stopwords

Stopwords can be passed inline, as we did in ((("stopwords", "specifying")))the previous example, by
specifying an array:

[source,json]
---------------------------------
"stopwords": [ "and", "the" ]
---------------------------------

The default stopword list for a particular language can be specified using the
`_lang_` notation:

[source,json]
---------------------------------
"stopwords": "_english_"
---------------------------------

TIP: The predefined language-specific stopword((("languages", "predefined stopword lists for"))) lists available in
Elasticsearch can be found in the
http://bit.ly/157YLFy[`stop` token filter] documentation.

Stopwords can be disabled by ((("stopwords", "disabling")))specifying the special list: `_none_`.  For
instance, to use the `english` analyzer((("english analyzer", "using without stopwords"))) without stopwords, you can do the
following:

[source,json]
---------------------------------
PUT /my_index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_english": {
          "type":      "english", <1>
          "stopwords": "_none_" <2>
        }
      }
    }
  }
}
---------------------------------
<1> The `my_english` analyzer is based on the `english` analyzer.
<2> But stopwords are disabled.

Finally, stopwords can also be listed in a file with one word per line.  The
file must be present on all nodes in the cluster, and the path can be
specified((("stopwords_path parameter"))) with the `stopwords_path` parameter:

[source,json]
---------------------------------
PUT /my_index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_english": {
          "type":           "english",
          "stopwords_path": "stopwords/english.txt" <1>
        }
      }
    }
  }
}
---------------------------------
<1> The path to the stopwords file, relative to the Elasticsearch `config`
    directory

[[stop-token-filter]]
==== Using the stop Token Filter

The http://bit.ly/1AUzDNI[`stop` token filter] can be combined
with a tokenizer((("stopwords", "using stop token filter")))((("stop token filter", "using in custom analyzer"))) and other token filters when you need to create a `custom`
analyzer.  For instance, let's say that we wanted to ((("Spanish", "custom analyzer for")))((("light_spanish stemmer")))create a Spanish analyzer
with the following:

* A custom stopwords list
* The `light_spanish` stemmer
* The <<asciifolding-token-filter,`asciifolding` filter>> to remove diacritics

We could set that up as follows:

[source,json]
---------------------------------
PUT /my_index
{
  "settings": {
    "analysis": {
      "filter": {
        "spanish_stop": {
          "type":        "stop",
          "stopwords": [ "si", "esta", "el", "la" ]  <1>
        },
        "light_spanish": { <2>
          "type":     "stemmer",
          "language": "light_spanish"
        }
      },
      "analyzer": {
        "my_spanish": {
          "tokenizer": "spanish",
          "filter": [ <3>
            "lowercase",
            "asciifolding",
            "spanish_stop",
            "light_spanish"
          ]
        }
      }
    }
  }
}
---------------------------------
<1> The `stop` token filter takes the same `stopwords` and `stopwords_path`
    parameters as the `standard` analyzer.
<2> See <<algorithmic-stemmers>>.
<3> The order of token filters is important, as explained next.

We have placed the `spanish_stop` filter after the `asciifolding` filter.((("asciifolding token filter", "in custom Spanish analyzer"))) This
means that `esta`, `ésta`, and ++está++ will first have their diacritics
removed to become just `esta`, which will then be removed as a stopword. If,
instead, we wanted to remove `esta` and `ésta`, but not ++está++, we
would have to put the `spanish_stop` filter _before_ the `asciifolding`
filter, and specify both words in the stopwords list.

[[updating-stopwords]]
==== Updating Stopwords

A few techniques can be used to update the list of stopwords
used by an analyzer.((("analyzers", "stopwords list, updating")))((("stopwords", "updating list used by analyzers"))) Analyzers are instantiated at index creation time, when a
node is restarted, or when a closed index is reopened.

If you specify stopwords inline with the `stopwords` parameter, your
only option is to close the index and update the analyzer configuration with the
http://bit.ly/1zijFPx[update index settings API], then reopen
the index.

Updating stopwords is easier if you specify them in a file with the
`stopwords_path` parameter.((("stopwords_path parameter")))  You can just update the file (on every node in
the cluster) and then force the analyzers to be re-created by either of these actions:

* Closing and reopening the index
  (see http://bit.ly/1B6s0WY[open/close index]), or
* Restarting each node in the cluster, one by one

Of course, updating the stopwords list will not change any documents that have
already been indexed. It will apply only to searches and to new or updated
documents.  To apply the changes to existing documents, you will need to
reindex your data. See <<reindex>>.
