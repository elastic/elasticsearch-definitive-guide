[[choosing-a-stemmer]]
=== Choosing a Stemmer

The documentation for the
http://bit.ly/1AUfpDN[`stemmer`] token filter
lists multiple stemmers for some languages.((("stemming words", "choosing a stemmer")))((("English", "stemmers for")))  For English we have the following:

`english`::

    The http://bit.ly/17LseXy[`porter_stem`] token filter.

`light_english`::

    The http://bit.ly/1IObUjZ[`kstem`] token filter.

`minimal_english`::

    The `EnglishMinimalStemmer` in Lucene, which removes plurals

`lovins`::

    The http://bit.ly/1Cr4tNI[Snowball] based
    http://bit.ly/1ICyTjR[Lovins]
    stemmer, the first stemmer ever produced.

`porter`::

    The http://bit.ly/1Cr4tNI[Snowball] based
    http://bit.ly/1sCWihj[Porter] stemmer

`porter2`::

    The http://bit.ly/1Cr4tNI[Snowball] based
    http://bit.ly/1zip3lK[Porter2] stemmer

`possessive_english`::

    The `EnglishPossessiveFilter` in Lucene which removes `'s`

Add to that list the Hunspell stemmer with the various English dictionaries
that are available.

One thing is for sure: whenever more than one solution exists for a problem,
it means that none of the solutions solves the problem adequately. This
certainly applies to stemming -- each stemmer uses a different approach that
overstems and understems words to a different degree.

The `stemmer` documentation page ((("languages", "stemmers for")))highlights the recommended stemmer for
each language in bold, usually because it offers a reasonable compromise
between performance and quality. That said, the recommended stemmer may not be
appropriate for all use cases. There is no single right answer to the question
of which is the best stemmer -- it depends very much on your requirements.
There are three factors to take into account when making a choice:
performance, quality, and degree.

[[stemmer-performance]]
==== Stemmer Performance

Algorithmic stemmers are typically four or ((("stemming words", "choosing a stemmer", "stemmer performance")))((("Hunspell stemmer", "performance")))five times faster than Hunspell
stemmers. ``Handcrafted'' algorithmic stemmers are usually, but not always,
faster than their Snowball equivalents.  For instance, the `porter_stem` token
filter is significantly faster than the Snowball implementation of the Porter
stemmer.

Hunspell stemmers have to load all words, prefixes, and suffixes into memory,
which can consume a few megabytes of RAM.  Algorithmic stemmers, on the other
hand, consist of a small amount of code and consume very little memory.

[[stemmer-quality]]
==== Stemmer Quality

All languages, except Esperanto, are irregular.((("stemming words", "choosing a stemmer", "stemmer quality"))) While more-formal words tend
to follow a regular pattern, the most commonly used words often have irregular rules. Some stemming algorithms have been developed over years of
research and produce reasonably high-quality results. Others have been
assembled more quickly with less research and deal only with the most common
cases.

While Hunspell offers the promise of dealing precisely with irregular words,
it often falls short in practice. A dictionary stemmer is only as good as its
dictionary.   If Hunspell comes across a word that isn't in its dictionary, it
can do nothing with it. Hunspell requires an extensive, high-quality, up-to-date dictionary in order to produce good results; dictionaries of this
caliber are few and far between. An algorithmic stemmer, on the other hand,
will happily deal with new words that didn't exist when the designer created
the algorithm.

If a good algorithmic stemmer is available for your language, it makes sense
to use it rather than Hunspell.  It will be faster, will consume less memory, and
will generally be as good or better than the Hunspell equivalent.

If accuracy and customizability is important to you, and you need (and
have the resources) to maintain a custom dictionary, then Hunspell gives you
greater flexibility than the algorithmic stemmers. (See
<<controlling-stemming>> for customization techniques that can be used with
any stemmer.)

[[stemmer-degree]]
==== Stemmer Degree

Different stemmers overstem and understem((("stemming words", "choosing a stemmer", "stemmer degree"))) to a different degree.  The `light_`
stemmers stem less aggressively than the standard stemmers, and the `minimal_`
stemmers less aggressively still.  Hunspell stems aggressively.

Whether you want aggressive or light stemming depends on your use case.  If
your search results are being consumed by a clustering algorithm, you may
prefer to match more widely (and, thus, stem more aggressively).  If your
search results are intended for human consumption, lighter stemming usually
produces better results.  Stemming nouns and adjectives is more important for
search than stemming verbs, but this also depends on the language.

The other factor to take into account is the size of your document collection.
With a small collection such as a catalog of 10,000 products, you probably want to
stem more aggressively to ensure that you match at least some documents.  If
your collection is large, you likely will get good matches with lighter
stemming.

==== Making a Choice

Start out with a recommended stemmer.  If it works well enough, there is
no need to change it.  If it doesn't, you will need to spend some time
investigating and comparing the stemmers available for language in order to
find the one that best suits your purposes.
