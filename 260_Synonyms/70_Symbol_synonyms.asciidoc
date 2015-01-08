[[symbol-synonyms]]
=== Symbol Synonyms

The final part of this chapter is devoted to symbol synonyms, which are
unlike the synonyms((("symbol synonyms")))((("synonyms", "symbol"))) we have discussed until now.  _Symbol synonyms_ are
string aliases used to represent symbols that would otherwise be removed
during tokenization.

While most punctuation is seldom important for full-text search, character
combinations like emoticons((("emoticons"))) may be very signficant, even changing the meaning
of the the text.  Compare these:

[role="pagebreak-before"]
* I am thrilled to be at work on Sunday.
* I am thrilled to be at work on Sunday :(

The `standard` tokenizer would simply strip out the emoticon in the second
sentence, conflating two sentences that have quite different intent.

We can use the
http://bit.ly/1ziua5n[`mapping` character filter]
to replace emoticons((("mapping character filter", "replacing emoticons with symbol synonyms")))((("emoticons", "replacing with symbol synonyms"))) with symbol synonyms like `emoticon_happy` and
`emoticon_sad` before the text is passed to the tokenizer:

[source,json]
--------------------------------------
PUT /my_index
{
  "settings": {
    "analysis": {
      "char_filter": {
        "emoticons": {
          "type": "mapping",
          "mappings": [ <1>
            ":)=>emoticon_happy",
            ":(=>emoticon_sad"
          ]
        }
      },
      "analyzer": {
        "my_emoticons": {
          "char_filter": "emoticons",
          "tokenizer":   "standard",
          "filter":    [ "lowercase" ]
          ]
        }
      }
    }
  }
}

GET /my_index/_analyze?analyzer=my_emoticons
I am :) not :( <2>
--------------------------------------
<1> The `mappings` filter replaces the characters to the left of `=>`
    with those to the right.
<2> Emits tokens `i`, `am`, `emoticon_happy`, `not`, `emoticon_sad`.

It is unlikely that anybody would ever search for `emoticon_happy`, but
ensuring that important symbols like emoticons are included in the index can
be helpful when doing sentiment analysis.  Of course, we could equally
have used real words, like `happy` and `sad`.

TIP: The `mapping` character filter is useful for simple replacements of exact
character sequences. ((("mapping character filter", "replacements of exact character sequences")))For more-flexible pattern matching, you can use regular
expressions with the
http://bit.ly/1DK4hgy[`pattern_replace` character filter].
