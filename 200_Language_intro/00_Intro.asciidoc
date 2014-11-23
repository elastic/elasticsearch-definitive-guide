[[language-intro]]
== Getting Started with Languages

Elasticsearch ships with a collection of language analyzers that provide
good, basic, out-of-the-box ((("language analyzers")))((("languages", "getting started with")))support for many of the world's most common
languages:

Arabic, Armenian, Basque, Brazilian, Bulgarian, Catalan, Chinese,
Czech, Danish, Dutch, English, Finnish, French, Galician, German, Greek,
Hindi, Hungarian, Indonesian, Irish, Italian, Japanese, Korean, Kurdish, 
Norwegian, Persian, Portuguese, Romanian, Russian, Spanish, Swedish, 
Turkish, and Thai.

These analyzers typically((("language analyzers", "roles performed by"))) perform four roles:

* Tokenize text into individual words:
+
`The quick brown foxes` -> [`The`, `quick`, `brown`, `foxes`]

* Lowercase tokens:
+
`The` -> `the`

* Remove common _stopwords_:
+
&#91;`The`, `quick`, `brown`, `foxes`] -> [`quick`, `brown`, `foxes`]

* Stem tokens to their root form:
+
`foxes` -> `fox`

Each analyzer may also apply other transformations specific to its language in
order to make words from that((("language analyzers", "other transformations specific to the language"))) language more searchable:

* The `english` analyzer ((("english analyzer")))removes the possessive `'s`:
+
`John's` -> `john`

* The `french` analyzer ((("french analyzer")))removes _elisions_ like `l'` and `qu'` and
  _diacritics_ like `¨` or `^`:
+
`l'église` -> `eglis`

* The `german` analyzer normalizes((("german analyzer"))) terms, replacing `ä` and `ae` with `a`, or
  `ß` with `ss`, among others:
+
`äußerst` -> `ausserst`

