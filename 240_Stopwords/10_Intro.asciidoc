[[stopwords]]
== Stopwords: Performance Versus Precision

Back in the early days of information retrieval,((("stopwords", "performance versus precision")))  disk space and memory were
limited to a tiny fraction of what we are accustomed to today. It was
essential to make your index as small as possible.  Every kilobyte saved meant
a significant improvement in performance. Stemming (see <<stemming>>) was
important, not just for making searches broader and increasing retrieval in
the same way that we use it today, but also as a tool for compressing index
size.

Another way to reduce index size is simply to _index fewer words_.  For search
purposes, some words are more important than others. A significant reduction
in index size can be achieved by indexing only the more important terms.

So which terms can be left out? ((("term frequency", "high and low"))) We can divide terms roughly into two groups:

Low-frequency terms::

Words that appear in relatively few documents in the collection.  Because of their
rarity,((("weight", "low frequency terms"))) they have a high value, or _weight_.

High-frequency terms::

Common words that appear in many documents in the index, such as `the`, `and`, and
`is`. These words  have a low weight and contribute little to the relevance
score.

[TIP]
==================================================

Of course, frequency is really a scale rather than just two points labeled
_low_ and _high_. We just draw a line at some arbitrary point and say that any
terms below that line are low frequency and above the line are high frequency.

==================================================

Which terms are low or high frequency depend on the documents themselves.  The
word `and` may be a low-frequency term if all the documents are in Chinese.
In a collection of documents about databases, the word `database` may be a
high-frequency term with little value as a search term for that particular
collection.

That said, for any language there are words that occur very
commonly and that seldom add value to a search.((("English", "stopwords")))  The default English
stopwords used in Elasticsearch are as follows:

    a, an, and, are, as, at, be, but, by, for, if, in, into, is, it,
    no, not, of, on, or, such, that, the, their, then, there, these,
    they, this, to, was, will, with

These _stopwords_ can usually be filtered out before indexing with little
negative impact on retrieval. But is it a good idea to do so?

[[pros-cons-stopwords]]
[float="true"]
=== Pros and Cons of Stopwords

We have more disk space, more RAM, and ((("stopwords", "pros and cons of")))better compression algorithms than
existed back in the day. Excluding the preceding 33 common words from the index
will save only about 4MB per million documents.  Using stopwords for the sake
of reducing index size is no longer a valid reason. (However, there is one
caveat to this statement, which we discuss in <<stopwords-phrases>>.)

On top of that, by removing words from the index, we are reducing our ability
to perform certain types of searches.  Filtering out the words listed previously
prevents us from doing the following:

* Distinguishing _happy_ from _not happy_.
* Searching for the band The The.
* Finding Shakespeare's quotation ``To be, or not to be''
* Using the country code for Norway: `no`

The primary advantage of removing stopwords is performance.  Imagine that we
search an index with one million documents for the word `fox`.  Perhaps `fox`
appears in only 20 of them, which means that Elastisearch has to calculate the
relevance `_score` for 20 documents in order to return the top 10. Now, we
change that to a search for `the OR fox`. The word `the` probably occurs in
almost all the documents, which means that Elasticsearch has to calculate
the `_score` for all one million documents.  This second query simply cannot
perform as well as the first.

Fortunately, there are techniques that we can use to keep common words
searchable, while still maintaining good performance. First, we'll start with
how to use stopwords.



