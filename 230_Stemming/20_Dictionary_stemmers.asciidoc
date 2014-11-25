[[dictionary-stemmers]]
=== Dictionary Stemmers

_Dictionary stemmers_ work quite differently from
<<algorithmic-stemmers,algorithmic stemmers>>.((("stemming words", "dictionary stemmers")))((("dictionary stemmers"))) Instead
of applying a standard set of rules to each word, they simply look up the
word in the dictionary.  Theoretically, they could produce much better
results than an algorithmic stemmer. A dictionary stemmer should be able to do the following:

* Return the correct root word for irregular forms such as `feet` and `mice`
* Recognize the distinction between words that are similar but have
  different word senses&#x2014;for example, `organ` and `organization`

In practice, a good algorithmic stemmer usually outperforms a dictionary
stemmer. There are a couple of reasons this should be so:

Dictionary quality::
+
--
A dictionary stemmer is only as good as its dictionary. ((("dictionary stemmers", "dictionary quality and"))) The Oxford English
Dictionary website estimates that the English language contains approximately
750,000 words (when inflections are included). Most English dictionaries
available for computers contain about 10% of those.

The meaning of words changes with time.  While stemming `mobility` to `mobil`
may have made sense previously, it now conflates the idea of mobility with a
mobile phone. Dictionaries need to be kept current, which is a time-consuming
task.  Often, by the time a dictionary has been made available, some of its
entries are already out-of-date.

If a dictionary stemmer encounters a word not in its dictionary, it doesn't
know how to deal with it.  An algorithmic stemmer, on the other hand, will
apply the same rules as before, correctly or incorrectly.
--

Size and performance::
+
--

A dictionary stemmer needs to load all words,((("dictionary stemmers", "size and performance"))) all prefixes, and all suffixes
into memory. This can use a significant amount of RAM. Finding the right stem
for a word is often considerably more complex than the equivalent process with
an algorithmic stemmer.

Depending on the quality of the dictionary, the process of removing prefixes
and suffixes may be more or less efficient.  Less-efficient forms can slow
the stemming process significantly.

Algorithmic stemmers, on the other hand, are usually simple, small, and fast.
--

TIP: If a good algorithmic stemmer exists for your language, it is usually a
better choice than a dictionary-based stemmer.  Languages with poor (or nonexistent) algorithmic stemmers can use the Hunspell dictionary stemmer, which
we discuss in the next section.

