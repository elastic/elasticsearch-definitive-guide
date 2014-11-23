[[identifying-words]]
== Identifying Words

A word in English is relatively simple to spot: words are separated by
whitespace or (some) punctuation.((("languages", "identifyig words")))((("words", "identifying"))) Even in English, though, there can be
controversy: is _you're_ one word or two? What about _o'clock_,
_cooperate_, _half-baked_, or _eyewitness_?

Languages like German or Dutch combine individual words to create longer
compound words like _Weißkopfseeadler_ (white-headed sea eagle), but in order
to be able to return `Weißkopfseeadler` as a result for the query `Adler`
(eagle), we need to understand how to break up compound words into their
constituent parts.

Asian languages are even more complex: some have no whitespace between words,
sentences, or even paragraphs.((("Asian languages", "identifying words"))) Some words can be represented by a single
character, but the same single character, when placed next to other
characters, can form just one part of a longer word with a quite different
meaning.

It should be obvious that there is no silver-bullet analyzer that will
miraculously deal with all human languages. Elasticsearch ships with dedicated
analyzers for many languages, and more language-specific analyzers are
available as plug-ins.

However, not all languages have dedicated analyzers, and sometimes you won't
even be sure which language(s) you are dealing with.  For these situations, we
need good standard tools that do a reasonable job regardless of language.
