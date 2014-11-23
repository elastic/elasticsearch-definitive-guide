[[icu-tokenizer]]
=== icu_tokenizer

The `icu_tokenizer` uses the same Unicode Text Segmentation algorithm as the
`standard` tokenizer,((("words", "identifying", "using icu_tokenizer")))((("Unicode Text Segmentation algorithm")))((("icu_tokenizer"))) but adds better support for some Asian languages by
using a dictionary-based approach to identify words in Thai, Lao, Chinese,
Japanese, and Korean, and using custom rules to break Myanmar and Khmer text
into syllables.

For instance, compare the tokens ((("standard tokenizer", "icu_tokenizer versus")))produced by the `standard` and
`icu_tokenizers`, respectively, when tokenizing ``Hello. I am from Bangkok.'' in
Thai:

[source,js]
--------------------------------------------------
GET /_analyze?tokenizer=standard
สวัสดี ผมมาจากกรุงเทพฯ
--------------------------------------------------

The `standard` tokenizer produces two tokens, one for each sentence: `สวัสดี`,
`ผมมาจากกรุงเทพฯ`.  That is useful only if you want to search for the whole
sentence ``I am from Bangkok.'', but not if you want to search for just
``Bangkok.''

[source,js]
--------------------------------------------------
GET /_analyze?tokenizer=icu_tokenizer
สวัสดี ผมมาจากกรุงเทพฯ
--------------------------------------------------

The `icu_tokenizer`, on the other hand, is able to break up the text into the
individual words (`สวัสดี`, `ผม`, `มา`, `จาก`, `กรุงเทพฯ)`, making them
easier to search.

In contrast, the `standard` tokenizer ``over-tokenizes'' Chinese and Japanese
text, often breaking up whole words into single characters. Because there
are no spaces between words, it can be difficult to tell whether consecutive
characters are separate words or form a single word.  For instance:

* 向 means _facing_, 日 means _sun_, and 葵 means _hollyhock_. When
  written together, 向日葵 means _sunflower_.

* 五 means _five_ or _fifth_, 月 means _month_, and 雨 means _rain_.
  The first two characters written together as 五月 mean _the month
  of May_, and adding the third character, 五月雨 means
  _continuous rain_. When combined with a fourth character, 式,
  meaning _style_, the word 五月雨式 becomes an adjective for anything
  consecutive or unrelenting.

Although each character may be a word in its own right, tokens are more
meaningful when they retain the bigger original concept instead of just the
component parts:

[source,js]
--------------------------------------------------
GET /_analyze?tokenizer=standard
向日葵

GET /_analyze?tokenizer=icu_tokenizer
向日葵
--------------------------------------------------

The `standard` tokenizer in the preceding example would emit each character
as a separate token: `向`, `日`, `葵`. The `icu_tokenizer` would
emit the single token `向日葵` (sunflower).

Another difference between the `standard` tokenizer and the `icu_tokenizer` is
that the latter will break a word containing characters written in different
scripts (for example, `βeta`) into separate tokens&#x2014;`β`, `eta`&#x2014;while the
former will emit the word as a single token: `βeta`.




