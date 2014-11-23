[[standard-tokenizer]]
=== standard Tokenizer

A _tokenizer_ accepts a string as input, processes((("words", "identifying", "using standard tokenizer")))((("standard tokenizer")))((("tokenizers"))) the string to break it
into individual words, or _tokens_ (perhaps discarding some characters like
punctuation), and emits a _token stream_ as output.

What is interesting is the algorithm that is used to _identify_ words. The
`whitespace` tokenizer ((("whitespace tokenizer")))simply breaks on whitespace--spaces, tabs, line
feeds, and so forth--and assumes that contiguous nonwhitespace characters form a
single token. For instance:

[source,js]
--------------------------------------------------
GET /_analyze?tokenizer=whitespace
You're the 1st runner home!
--------------------------------------------------

This request would return the following terms:
`You're`, `the`, `1st`, `runner`, `home!`

The `letter` tokenizer, on the other hand, breaks on any character that is
not a letter, and so would ((("letter tokenizer")))return the following terms: `You`, `re`, `the`,
`st`, `runner`, `home`.

The `standard` tokenizer((("Unicode Text Segmentation algorithm"))) uses the Unicode Text Segmentation algorithm (as
defined in http://unicode.org/reports/tr29/[Unicode Standard Annex #29]) to
find the boundaries _between_ words,((("word boundaries"))) and emits everything in-between. Its
knowledge of Unicode allows it to successfully tokenize text containing a
mixture of languages.

Punctuation may((("punctuation", "in words"))) or may not be considered part of a word, depending on
where it appears:

[source,js]
--------------------------------------------------
GET /_analyze?tokenizer=standard
You're my 'favorite'.
--------------------------------------------------

In this example, the apostrophe in `You're` is treated as part of the
word, while the single quotes in `'favorite'` are not, resulting in the
following terms: `You're`, `my`, `favorite`.

[TIP]
==================================================

The `uax_url_email` tokenizer works((("uax_url_email tokenizer"))) in exactly the same way as the `standard`
tokenizer, except that it recognizes((("email addresses and URLs, tokenizer for"))) email addresses and URLs and emits them as
single tokens. The `standard` tokenizer, on the other hand, would try to
break them into individual words. For instance, the email address
`joe-bloggs@foo-bar.com` would result in the tokens `joe`, `bloggs`, `foo`,
`bar.com`.

==================================================

The `standard` tokenizer is a reasonable starting point for tokenizing most
languages, especially Western languages.  In fact, it forms the basis of most
of the language-specific analyzers like the `english`, `french`, and `spanish`
analyzers. Its support for Asian languages, however, is limited, and you should consider
using the `icu_tokenizer` instead,((("icu_tokenizer"))) which is available in the ICU plug-in.
