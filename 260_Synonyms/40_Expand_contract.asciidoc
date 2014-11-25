[[synonyms-expand-or-contract]]
=== Expand or contract

In <<synonym-formats>>, we have seen that it is((("synonyms", "expanding or contracting"))) possible to replace synonyms by
_simple expansion_, _simple contraction_, or _generic expansion_.  We will look
at the trade-offs of each of these techniques in this section.

TIP: This section deals with single-word synonyms only.  Multiword
synonyms add another layer of complexity and are discussed later in
<<multi-word-synonyms>>.

[[synonyms-expansion]]
==== Simple Expansion

With _simple expansion_,((("synonyms", "expanding or contracting", "simple expansion")))((("simple expansion (synonyms)"))) any of the listed synonyms is expanded into _all_ of
the listed synonyms:

    "jump,hop,leap"

Expansion can be applied either at index time or at query time.  Each has advantages
(⬆)︎ and disadvantages (⬇)︎. When to use which comes down to performance versus
flexibility.

[options="header",cols="h,d,d"]
|===================================================
|                   | Index time             | Query time

| Index size        |
      ⬇︎ Bigger index because all synonyms must be indexed. |
      ⬆︎ Normal.

| Relevance         |
      ⬇︎ All synonyms will have the same IDF (see <<relevance-intro>>), meaning
      that more commonly used words will have the same weight as less commonly
      used words. |
      ⬆︎ The IDF for each synonym will be correct.

| Performance |
      ⬆︎ A query needs to find only the single term specified in the query string. |
      ⬇︎ A query for a single term is rewritten to look up all synonyms, which
      decreases performance.

| Flexibility       |
      ⬇︎ The synonym rules can't be changed for existing documents. For the new rules
      to have effect, existing documents have to be reindexed. |
      ⬆︎ Synonym rules can be updated without reindexing documents.
|===================================================

[[synonyms-contraction]]
==== Simple Contraction

_Simple contraction_ maps a group of ((("synonyms", "expanding or contracting", "simple contraction")))((("simple contraction (synonyms)")))synonyms on the left side to a single
value on the right side:

    "leap,hop => jump"

It must be applied both at index time and at query time, to ensure that query
terms are mapped to the same single value that exists in the index.

This approach has some advantages and some disadvantages compared to the simple expansion approach:

Index size::

⬆︎ The index size is normal, as only a single term is indexed.

Relevance::

⬇︎ The IDF for all terms is the same, so you can't distinguish between more
commonly used words and less commonly used words.

Performance::

⬆︎ A query needs to find only the single term that appears in the index.

Flexibility::
+
--

⬆︎ New synonyms can be added to the left side of the rule and applied at
query time. For instance, imagine that we wanted to add the word `bound` to
the rule specified previously. The following rule would work for queries that
contain `bound` or for newly added documents that contain `bound`:

    "leap,hop,bound => jump"

But we could expand the effect to also take into account _existing_ documents
that contain `bound` by writing the rule as follows:

    "leap,hop,bound => jump,bound"

When you reindex your documents, you could revert to the previous rule to gain
the performance benefit of querying only a single term.

--

[[synonyms-genres]]
==== Genre Expansion

Genre expansion is quite different from simple((("synonyms", "expanding or contracting", "genre expansion")))((("genre expansion (synonyms)"))) contraction or expansion.
Instead of treating all synonyms as equal, genre expansion widens the meaning
of a term to be more generic. Take these rules, for example:

    "cat    => cat,pet",
    "kitten => kitten,cat,pet",
    "dog    => dog,pet"
    "puppy  => puppy,dog,pet"

By applying genre expansion at index time:

* A query for `kitten` would find just documents about kittens.
* A query for `cat` would find documents abouts kittens and cats.
* A query for `pet` would find documents about kittens, cats, puppies, dogs,
  or pets.

Alternatively, by applying genre expansion at query time, a query for `kitten`
would be expanded to return documents that mention kittens, cats, or pets
specifically.

You could also have the best of both worlds by applying expansion at index
time to ensure that the genres are present in the index. Then, at query time,
you can choose to not apply synonyms (so that a query for `kitten`
returns only documents about kittens) or to apply synonyms in order to match
kittens, cats and pets (including the canine variety).

With the preceding example rules above, the IDF for `kitten` will be correct, while the
IDF for `cat` and `pet` will be artificially deflated.  However, this
works in your favor--a genre-expanded query for `kitten OR cat OR pet` will
rank documents with `kitten` highest, followed by documents with `cat`, and
documents with `pet` would be right at the bottom.
