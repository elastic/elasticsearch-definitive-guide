[[stemming-in-situ]]
=== Stemming in situ

For the sake of completeness, we will ((("stemming words", "stemming in situ")))finish this chapter by explaining how to
index stemmed words into the same field as unstemmed words. As an example,
analyzing the sentence _The quick foxes jumped_ would produce the following
terms:

[source,text]
------------------------------------
Pos 1: (the)
Pos 2: (quick)
Pos 3: (foxes,fox) <1>
Pos 4: (jumped,jump) <1>
------------------------------------

<1> The stemmed and unstemmed forms occupy the same position.

WARNING: Read <<stemming-in-situ-good-idea>> before using this approach.

To achieve stemming _in situ_, we will use the
http://bit.ly/1ynIBCe[`keyword_repeat`]
token filter,((("keyword_repeat token filter"))) which, like the `keyword_marker` token filter (see
<<preventing-stemming>>), marks each term as a keyword to prevent the subsequent
stemmer from touching it.  However, it also repeats the term in the same
position, and this repeated term *is* stemmed.

Using the `keyword_repeat` token filter alone would result in the following:

[source,text]
------------------------------------
Pos 1: (the,the) <1>
Pos 2: (quick,quick) <1>
Pos 3: (foxes,fox)
Pos 4: (jumped,jump)
------------------------------------
<1> The stemmed and unstemmed forms are the same, and so are repeated
    needlessly.

To prevent the useless repetition of terms that are the same in their stemmed
and unstemmed forms, we add the
http://bit.ly/1B6xHUY[`unique`] token filter((("unique token filter"))) into the mix:

[source,json]
------------------------------------
PUT /my_index
{
  "settings": {
    "analysis": {
      "filter": {
        "unique_stem": {
          "type": "unique",
          "only_on_same_position": true <1>
        }
      },
      "analyzer": {
        "in_situ": {
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "keyword_repeat", <2>
            "porter_stem",
            "unique_stem" <3>
          ]
        }
      }
    }
  }
}
------------------------------------
<1> The `unique` token filter is set to remove duplicate tokens
    only when they occur in the same position.
<2> The `keyword_repeat` token filter must appear before the
    stemmer.
<3> The `unique_stem` filter removes duplicate terms after the
    stemmer has done its work.

[[stemming-in-situ-good-idea]]
==== Is Stemming in situ a Good Idea

People like the ((("stemming words", "stemming in situ", "good idea, or not")))idea of stemming _in situ_: ``Why use an unstemmed field
_and_ a stemmed field if I can just use one combined field?'' But is it a
good idea? The answer is almost always no.  There are two problems.

The first is the inability to separate exact matches from inexact matches.  In
this chapter, we have seen that words with different meanings are often
conflated to the same stem word: `organs` and `organization` both stem to
`organ`.

In <<using-language-analyzers>>, we demonstrated how to combine a query on a
stemmed field (to increase recall) with a query on an unstemmed field (to
improve relevance).((("language analyzers", "combining query on stemmed and unstemmed field")))  When the stemmed and unstemmed fields are separate, the
contribution of each field can be tuned by boosting one field over another
(see <<prioritising-clauses>>).  If, instead, the stemmed and unstemmed forms
appear in the same field, there is no way to tune your search results.

The second issue has to do with how the ((("relevance scores", "stemming in situ and")))relevance score is calculated.  In
<<relevance-intro>>, we explained that part of the calculation depends on the
_inverse document frequency_ -- how often a word appears in all the documents
in our index.((("inverse document frequency", "stemming in situ and")))  Using in situ stemming for a document that contains  the text
`jump jumped jumps` would result in these terms:

[source,text]
------------------------------------
Pos 1: (jump)
Pos 2: (jumped,jump)
Pos 3: (jumps,jump)
------------------------------------

While `jumped` and `jumps` appear once each and so would have the correct IDF,
`jump` appears three times, greatly reducing its value as a search term in
comparison with the unstemmed forms.

For these reasons, we recommend against using stemming in situ.
