[[multi-field-search]]
== Multifield Search

Queries are seldom simple one-clause `match` queries. ((("multifield search"))) We frequently need to
search for the same or different query strings in one or more fields, which
means that we need to be able to combine multiple query clauses and their
relevance scores in a way that makes sense.

Perhaps we're looking for a book called _War and Peace_ by an author called
Leo Tolstoy. Perhaps we're searching the Elasticsearch documentation
for ``minimum should match,'' which might be in the title or the body of a
page. Or perhaps we're searching for users with first name John and last
name Smith.

In this chapter, we present the available tools for constructing multiclause
searches and how to figure out which solution you should apply to your
particular use case.
