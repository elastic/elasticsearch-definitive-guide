[[character-folding]]
=== Unicode Character Folding

In the same way as the `lowercase` token filter is a good starting point for
many languages((("Unicode", "character folding")))((("tokens", "normalizing", "Unicode character folding"))) but falls short when exposed to the entire tower of Babel, so
the <<asciifolding-token-filter,`asciifolding` token filter>> requires a more
effective Unicode _character-folding_ counterpart((("character folding"))) for dealing with the many
languages of the world.((("asciifolding token filter")))

The `icu_folding` token filter (provided by the <<icu-plugin,`icu` plug-in>>)
does the same job as the `asciifolding` filter, ((("icu_folding token filter")))but extends the transformation
to scripts that are not ASCII-based, such as Greek, Hebrew, Han, conversion
of numbers in other scripts into their Latin equivalents, plus various other
numeric, symbolic, and punctuation transformations.

The `icu_folding` token filter applies Unicode normalization and case folding
from `nfkc_cf` automatically,((("nfkc_cf normalization form"))) so the `icu_normalizer` is not required:

[source,js]
--------------------------------------------------
PUT /my_index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_folder": {
          "tokenizer": "icu_tokenizer",
          "filter":  [ "icu_folding" ]
        }
      }
    }
  }
}

GET /my_index/_analyze?analyzer=my_folder
١٢٣٤٥ <1>
--------------------------------------------------
<1> The Arabic numerals `١٢٣٤٥` are folded to their Latin equivalent: `12345`.

If there are particular characters that you would like to protect from
folding, you can use a
http://icu-project.org/apiref/icu4j/com/ibm/icu/text/UnicodeSet.html[_UnicodeSet_]
(much like a character class in regular expressions) to specify which Unicode
characters may be folded.  For instance, to exclude the Swedish letters `å`,
`ä`, `ö`, ++Å++, `Ä`, and `Ö` from folding, you would specify a character class
representing all Unicode characters, except for those letters: `[^åäöÅÄÖ]`
(`^` means _everything except_).((("swedish_folding filter")))((("swedish analyzer")))

[source,js]
--------------------------------------------------
PUT /my_index
{
  "settings": {
    "analysis": {
      "filter": {
        "swedish_folding": { <1>
          "type": "icu_folding",
          "unicodeSetFilter": "[^åäöÅÄÖ]"
        }
      },
      "analyzer": {
        "swedish_analyzer": { <2>
          "tokenizer": "icu_tokenizer",
          "filter":  [ "swedish_folding", "lowercase" ]
        }
      }
    }
  }
}
--------------------------------------------------
<1> The `swedish_folding` token filter customizes the
    `icu_folding` token filter to exclude Swedish letters,
    both uppercase and lowercase.
<2> The `swedish` analyzer first tokenizes words, then folds
    each token by using the `swedish_folding` filter, and then
    lowercases each token in case it includes some of
    the uppercase excluded letters: ++Å++, `Ä`, or `Ö`.

