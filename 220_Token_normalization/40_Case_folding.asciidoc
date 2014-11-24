[[case-folding]]
=== Unicode Case Folding

Humans are nothing if not inventive,((("tokens", "normalizing", "Unicode case folding")))((("Unicode", "case folding"))) and human language reflects that.
Changing the case of a word seems like such a simple task, until you have to
deal with multiple languages.

Take, for example, the lowercase German letter `ß`.  Converting that to upper
case gives you `SS`, which converted back to lowercase gives you `ss`. Or consider the
Greek letter `ς` (sigma, when used at the end of a word).  Converting it to
uppercase results in `Σ`, which converted back to lowercase, gives you `σ`.

The whole point of lowercasing terms is to make them _more_ likely to match,
not less!  In Unicode, this job is done by case folding rather((("case folding"))) than by lowercasing.  _Case folding_ is the act of converting words into a  (usually lowercase) form that does not necessarily result in the correct spelling, but does
allow case-insensitive comparisons.

For instance, the letter `ß`, which is already lowercase, is _folded_ to
`ss`. Similarly, the lowercase `ς` is folded to `σ`, to make `σ`, `ς`, and `Σ`
comparable, no matter where the letter appears in a word.((("nfkc_cf normalization form")))((("icu_normalizer token filter", "nfkc_cf normalization form")))

The default normalization form that the `icu_normalizer` token filter uses
is `nfkc_cf`. Like the `nfkc` form, this does the following:

* _Composes_ characters into the shortest byte representation
* Uses _compatibility_ mode to convert characters like `ﬃ` into the simpler
  `ffi`

But it also does this:

* _Case-folds_ characters into a form suitable for case comparison

In other words, `nfkc_cf` is the equivalent of the `lowercase` token filter,
but suitable for use with all languages.((("lowercase token filter", "nfkc_cf normalization form and"))) The _on-steroids_ equivalent of the
`standard` analyzer would be the following:

[source,js]
--------------------------------------------------
PUT /my_index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_lowercaser": {
          "tokenizer": "icu_tokenizer",
          "filter":  [ "icu_normalizer" ] <1>
        }
      }
    }
  }
}
--------------------------------------------------
<1> The `icu_normalizer` defaults to the `nfkc_cf` form.

We can compare the results of running `Weißkopfseeadler` and
`WEISSKOPFSEEADLER` (the uppercase equivalent) through the `standard`
analyzer and through our Unicode-aware analyzer:

[source,js]
--------------------------------------------------
GET /_analyze?analyzer=standard <1>
Weißkopfseeadler WEISSKOPFSEEADLER

GET /my_index/_analyze?analyzer=my_lowercaser <2>
Weißkopfseeadler WEISSKOPFSEEADLER
--------------------------------------------------
<1> Emits tokens `weißkopfseeadler`, `weisskopfseeadler`
<2> Emits tokens `weisskopfseeadler`, `weisskopfseeadler`

The `standard` analyzer emits two different, incomparable tokens, while our
custom analyzer produces tokens that are comparable, regardless of the
original case.

