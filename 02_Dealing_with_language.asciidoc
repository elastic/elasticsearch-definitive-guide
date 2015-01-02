ifndef::es_build[= placeholder2]

[[languages]]
= Dealing with Human Language

[partintro]
--

ifdef::es_build[]
[quote,Matt Groening]
____
``I know all those words, but that sentence makes no sense to me.''
____
endif::es_build[]

ifndef::es_build[]
++++
<blockquote data-type="epigraph">
    <p>I know all those words, but that sentence makes no sense to me.</p>
    <p data-type="attribution">Matt Groening</p>
</blockquote>
++++
endif::es_build[]

Full-text search is a battle between _precision_&#x2014;returning as few
irrelevant documents as possible--and _recall_&#x2014;returning as many relevant
documents as possible.((("recall", "in full text search")))((("precision", "in full text search")))((("full text search", "battle between precision and recall"))) While matching only the exact words that the user has
queried would be precise, it is not enough. We would miss out on many
documents that the user would consider to be relevant. Instead, we need to
spread the net wider, to also search for words that are not exactly the same
as the original but are related.

Wouldn't you expect a search for ``quick brown fox'' to match a document
containing ``fast brown foxes,'' ``Johnny Walker'' to match ``Johnnie
Walker,'' or ``Arnolt Schwarzenneger'' to match ``Arnold Schwarzenegger''?

If documents exist that _do_ contain exactly what the user has queried,
those documents should appear at the top of the result set, but weaker matches
can be included further down the list.  If no documents match
exactly, at least we can show the user potential matches; they may even
be what the user originally intended!

There are several((("full text search", "finding inexact matches"))) lines of attack:

*   Remove diacritics like +´+, `^`, and `¨` so that a search for `rôle` will
    also match `role`, and vice versa. See <<token-normalization>>.

*   Remove the distinction between singular and plural&#x2014;`fox` versus `foxes`&#x2014;or between tenses&#x2014;`jumping` versus `jumped` versus `jumps`&#x2014;by _stemming_ each word to its root form. See <<stemming>>.

*   Remove commonly used words or _stopwords_ like `the`, `and`, and `or`
    to improve search performance.  See <<stopwords>>.

*   Including synonyms so that a query for `quick` could also match `fast`,
    or `UK` could match `United Kingdom`. See <<synonyms>>.

*   Check for misspellings or alternate spellings, or match on _homophones_&#x2014;words that sound the same, like `their` versus `there`, `meat` versus
    `meet`  versus `mete`. See <<fuzzy-matching>>.

Before we can manipulate individual words, we need to divide text into
words, ((("words", "dividing text into")))which means that we need to know what constitutes a _word_. We will
tackle this in <<identifying-words>>.

But first, let's take a look at how to get started quickly and easily.
--

include::200_Language_intro.asciidoc[]

include::210_Identifying_words.asciidoc[]

include::220_Token_normalization.asciidoc[]

include::230_Stemming.asciidoc[]

include::240_Stopwords.asciidoc[]

include::260_Synonyms.asciidoc[]

include::270_Fuzzy_matching.asciidoc[]
