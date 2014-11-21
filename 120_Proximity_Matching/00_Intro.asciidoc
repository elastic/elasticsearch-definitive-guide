[[proximity-matching]]
== Proximity Matching

Standard full-text search with TF/IDF treats documents, or at least each field
within a document, as a big _bag of words_.((("proximity matching")))  The `match` query can tell us whether
that bag contains our search terms, but that is only part of the story.
It can't tell us anything about the relationship between words.

Consider the difference between these sentences:

* Sue ate the alligator.
* The alligator ate Sue.
* Sue never goes anywhere without her alligator-skin purse.

A `match` query for `sue alligator` would match all three documents, but it
doesn't tell us whether the two words form part of the same idea, or even the same
paragraph.

Understanding how words relate to each other is a complicated problem, and
we can't solve it by just using another type of query,
but we can at least find words that appear to be related because they appear
near each other or even right next to each other.

Each document may be much longer than the examples we have presented: `Sue`
and `alligator` may be separated by paragraphs of other text. Perhaps we still
want to return these documents in which the words are widely separated, but we
want to give documents in which the words are close together a higher relevance
score.

This is the province of _phrase matching_, or _proximity matching_.

[TIP]
==================================================

In this chapter, we are using the same example documents that we used for
the <<match-test-data,`match` query>>.

==================================================
