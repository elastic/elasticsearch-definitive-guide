ifndef::es_build[= placeholder1]

[[search-in-depth]]
= Search in Depth

[partintro]
--

In <<getting-started>> we covered the basic tools in just enough detail to
allow you to start searching your data with Elasticsearch. ((("searching", "using Elasticsearch"))) It won't take
long, though, before you find that you want more: more flexibility when matching
user queries, more-accurate ranking of results, more-specific searches to
cover different problem domains.

To move to the next level, it is not enough to just use the `match` query. You
need to understand your data and how you want to be able to search it. The
chapters in this part explain how to index and query your data to allow
you to take advantage of word proximity, partial matching, fuzzy matching, and
language awareness.

Understanding how each query contributes to the relevance `_score` will help
you to tune your queries: to ensure that the documents you consider to be the
best results appear on the first page, and to trim the ``long tail'' of barely
relevant results.

Search is not just about full-text search: a large portion of your data will
be structured values like dates and numbers. We will start by explaining how
to combine structured search((("structured search", "combining with full text search")))((("full text search", "combining with structured search"))) with full-text search in the most efficient way.

--

include::080_Structured_Search.asciidoc[]

include::100_Full_Text_Search.asciidoc[]

include::110_Multi_Field_Search.asciidoc[]

include::120_Proximity_Matching.asciidoc[]

include::130_Partial_Matching.asciidoc[]

include::170_Relevance.asciidoc[]


