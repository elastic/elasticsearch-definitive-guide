=== Ngrams for Partial Matching

As we have said before, ``You can find only terms that exist in the inverted
index.'' Although the `prefix`, `wildcard`, and `regexp` queries demonstrated that
that is not strictly true, it _is_ true that doing a single-term lookup is
much faster than iterating through the terms list to find matching terms on
the fly.((("partial matching", "index time optimizations", "n-grams"))) Preparing your data for partial matching ahead of time will increase
your search performance.

Preparing your data at index time means choosing the right analysis chain, and
the tool that we use for partial matching is the _n-gram_.((("n-grams"))) An n-gram can be
best thought of as a _moving window on a word_. The _n_ stands for a length.
If we were to n-gram the word `quick`, the results would depend on the length
we have chosen:

[horizontal]
* Length 1 (unigram):    [ `q`, `u`, `i`, `c`, `k` ]
* Length 2 (bigram):     [ `qu`, `ui`, `ic`, `ck` ]
* Length 3 (trigram):    [ `qui`, `uic`, `ick` ]
* Length 4 (four-gram):  [ `quic`, `uick` ]
* Length 5 (five-gram):  [ `quick` ]

Plain n-grams are useful for matching _somewhere within a word_, a technique
that we will use in <<ngrams-compound-words>>. However, for search-as-you-type,
we use a specialized form of n-grams called _edge n-grams_. ((("edge n-grams"))) Edge
n-grams are anchored to the beginning of the word. Edge n-gramming the word
`quick` would result in this:

* `q`
* `qu`
* `qui`
* `quic`
* `quick`

You may notice that this conforms exactly to the letters that a user searching for ``quick'' would type. In other words, these are the
perfect terms to use for instant search!
