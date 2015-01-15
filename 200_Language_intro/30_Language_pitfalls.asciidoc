[[language-pitfalls]]
=== Pitfalls of Mixing Languages

If you have to deal with only a single language,((("languages", "mixing, pitfalls of"))) count yourself lucky.
Finding the right strategy for handling documents written in several languages
can be challenging.((("indexing", "mixed languages, pitfalls of")))

==== At Index Time

Multilingual documents come in three main varieties:

 * One predominant language per _document_, which may contain snippets from
   other languages (See <<one-lang-docs>>.)
 * One predominant language per _field_, which may contain snippets from
   other languages (See <<one-lang-fields>>.)
 * A mixture of languages per field (See <<mixed-lang-fields>>.)

The goal, although not always achievable, should be to keep languages
separate.  Mixing languages in the same inverted index can be problematic.

===== Incorrect stemming

The stemming rules for German are different from those for English, French,
Swedish, and so on.((("stemming words", "incorrect stemming in multilingual documents"))) Applying the same stemming rules to different languages
will result in some words being stemmed correctly, some  incorrectly, and some
not being stemmed at all. It may even result in words from different languages with different meanings
being stemmed to the same root word, conflating their meanings and producing
confusing search results for the user.

Applying multiple stemmers in turn to the same text is likely to result in
rubbish, as the next stemmer may try to stem an already stemmed word,
compounding the problem.

[[different-scripts]]
.Stemmer per Script
************************************************
The one exception to the _only-one-stemmer_ rule occurs when each language
is written in a different script.  For instance, in Israel it is quite
possible that a single document may contain Hebrew, Arabic, Russian (Cyrillic),
and English:

    אזהרה - Предупреждение - تحذير - Warning

Each language uses a different script, so the stemmer for one language will not
interfere with another, allowing multiple stemmers to be applied to the same
text.
************************************************

===== Incorrect inverse document frequencies

In <<relevance-intro>>, we explained that the more frequently a term appears
in a collection of documents, the less weight that term has.((("inverse document frequency", "incorrect, in multilingual documents")))  For accurate
relevance calculations, you need accurate term-frequency statistics.

A short snippet of German appearing in predominantly English text would give
more weight to the German words, given that they are relatively uncommon. But
mix those with documents that are predominantly German, and the short German
snippets now have much less weight.

==== At Query Time

It is not sufficient just to think about your documents, though.((("queries", "mixed languages and")))  You also need
to think about how your users will query those documents.  Often you will be able
to identify the main language of the user either from the language of that user's chosen
interface (for example, `mysite.de` versus `mysite.fr`) or from the
http://bit.ly/1BwEl61[`accept-language`]
HTTP header from the user's browser.

User searches also come in three main varieties:

* Users search for words in their main language.
* Users search for words in a different language, but expect results in
  their main language.
* Users search for words in a different language, and expect results in
  that language (for example, a bilingual person, or a foreign visitor in a web cafe).

Depending on the type of data that you are searching, it may be appropriate to
return results in a single language (for example, a user searching for products on
the Spanish version of the website) or to combine results in the identified
main language of the user with results from other languages.

Usually, it makes sense to give preference to the user's language.  An English-speaking
user searching the Web for ``deja vu'' would probably prefer to see
the English Wikipedia page rather than the French Wikipedia page.

[[identifying-language]]
==== Identifying Language

You may already know the language of your documents.  Perhaps your documents
are created within your organization and translated into a list of predefined
languages.  Human pre-identification is probably the most reliable method of
classifying language correctly.

Perhaps, though, your documents come from an external source without any
language classification, or possibly with incorrect classification. In these
cases, you need to use a heuristic to identify the predominant language.
Fortunately, libraries are available in several languages to help with this problem.

Of particular note is the
http://bit.ly/1AUr3i2[chromium-compact-language-detector]
library from
http://bit.ly/1AUr85k[Mike McCandless],
which uses the open source (http://bit.ly/1u9KKgI[Apache License 2.0])
https://code.google.com/p/cld2/[Compact Language Detector] (CLD) from Google.  It is
small, fast, ((("Compact Language Detector (CLD)")))and accurate, and can detect 160+ languages from as little as two
sentences. It can even detect multiple languages within a single block of
text. Bindings exist for several languages including Python, Perl, JavaScript,
PHP, C#/.NET, and R.

Identifying the language of the user's search request is not quite as simple.
The CLD is designed for text that is at least 200 characters in length.
Shorter amounts of text, such as search keywords, produce much less accurate
results. In these cases, it may be preferable to take simple heuristics into
account such as the country of origin, the user's selected language, and the
HTTP `accept-language` headers.

