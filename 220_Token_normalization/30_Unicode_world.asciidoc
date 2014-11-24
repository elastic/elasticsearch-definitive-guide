[[unicode-normalization]]
=== Living in a Unicode World

When Elasticsearch compares one token with another, it does so at the byte
level. ((("Unicode", "token normalization and")))((("tokens", "normalizing", "Unicode and")))In other words, for two tokens to be considered the same, they need to
consist of exactly the same bytes.  Unicode, however, allows you to write the
same letter in different ways.

For instance, what's the difference between _&#x00e9;_ and _e&#769;_? It
depends on who you ask. According to Elasticsearch, the first one consists of
the two bytes `0xC3 0xA9`, and the second one consists of three bytes, `0x65
0xCC 0x81`.

According to Unicode, the differences in how they are represented as bytes is
irrelevant, and they are the same letter. The first one is the single letter
`é`, while the second is a plain `e` combined with an acute accent +´+.

If you get your data from more than one source, it may happen that you have
the same  letters encoded in different ways, which may result in one form of
++déjà++ not matching another!

Fortunately, a solution is at hand.  There are four Unicode _normalization
forms_, all of which convert Unicode characters into a standard format, making
all characters((("Unicode", "normalization forms"))) comparable at a byte level: `nfc`, `nfd`, `nfkc`, `nfkd`.((("nfkd normalization form")))((("nfkc normalization form")))((("nfd normalization form")))((("nfc normalization form")))

.Unicode Normalization Forms
********************************************

The _composed_ forms&#x2014;`nfc` and `nfkc`&#x2014;represent characters in the fewest
bytes possible.((("composed forms (Unicode normalization)")))  So `é` is represented as the single letter `é`.  The
_decomposed_ forms&#x2014;`nfd` and `nfkd`&#x2014;represent characters by their
constituent parts, that is `e` + `´`.((("decomposed forms (Unicode normalization)")))

The _canonical_ forms&#x2014;`nfc` and `nfd`&#x2014;represent ligatures like `ﬃ` or
`œ` as a single character,((("canonical forms (Unicode normalization)"))) while the _compatibility_ forms&#x2014;`nfkc` and
`nfkd`&#x2014;break down these composed characters into a simpler multiletter
equivalent: `f` + `f` + `i` or `o` + `e`.

********************************************

It doesn't really matter which normalization form you choose, as long as all
your text is in the same form.  That way, the same tokens consist of the
same bytes.  That said, the _compatibility_ forms ((("compatibility forms (Unicode normalization)")))allow you to compare
ligatures like `ﬃ` with their simpler representation, `ffi`.

You can use the `icu_normalizer` token filter to ((("icu_normalizer token filter")))ensure that all of your
tokens are in the same form:

[source,js]
--------------------------------------------------
PUT /my_index
{
  "settings": {
    "analysis": {
      "filter": {
        "nfkc_normalizer": { <1>
          "type": "icu_normalizer",
          "name": "nfkc"
        }
      },
      "analyzer": {
        "my_normalizer": {
          "tokenizer": "icu_tokenizer",
          "filter":  [ "nfkc_normalizer" ]
        }
      }
    }
  }
}
--------------------------------------------------
<1> Normalize all tokens into the `nfkc` normalization form.

[TIP]
==================================================

Besides the `icu_normalizer` token filter mentioned previously, there is also an
`icu_normalizer` _character_ filter, which((("icu_normalizer character filter"))) does the same job as the token
filter, but does so before the text reaches the tokenizer.  When using the
`standard` tokenizer or `icu_tokenizer`, this doesn't really matter.  These
tokenizers know how to deal with all forms of Unicode correctly.

However, if you plan on using a different tokenizer, such as the `ngram`,
`edge_ngram`, or `pattern` tokenizers, it would make sense to use the
`icu_normalizer` character filter in preference to the token filter.

==================================================

Usually, though, you will want to not only normalize the byte order of tokens,
but also lowercase them. This can be done with `icu_normalizer`, using
the custom normalization form `nfkc_cf`, which we discuss in the next section.
