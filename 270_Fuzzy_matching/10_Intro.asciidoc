[[fuzzy-matching]]
== Typoes and Mispelings

We expect a query on structured data like dates and prices to return only
documents that match exactly. ((("typoes and misspellings", "fuzzy matching")))((("fuzzy matching"))) However, good full-text search shouldn't have the
same restriction. Instead, we can widen the net to include words that _may_
match, but use the relevance score to push the better matches to the top
of the result set.

In fact, full-text search ((("full text search", "fuzzy matching")))that only matches exactly will probably frustrate
your users. Wouldn't you expect a search for ``quick brown fox'' to match a
document containing ``fast brown foxes,'' ``Johnny Walker'' to match
``Johnnie Walker,'' or ``Arnold Shcwarzenneger'' to match ``Arnold
Schwarzenegger''?

If documents exist that _do_ contain exactly what the user has queried,
they should appear at the top of the result set, but weaker matches can be
included further down the list.  If no documents match exactly, at least we
can show the user potential matches; they may even be what the user
originally intended!

We have already looked at diacritic-free matching in <<token-normalization>>,
word stemming in <<stemming>>, and synonyms in <<synonyms>>, but all of those
approaches presuppose that words are spelled correctly, or that there is only
one way to spell each word.

Fuzzy matching allows for query-time matching of misspelled words, while
phonetic token filters at index time can be used for _sounds-like_ matching.

