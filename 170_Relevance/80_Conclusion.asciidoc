
[[relevance-conclusion]]
=== Relevance Tuning Is the Last 10%

In this chapter, we looked at a how Lucene generates scores based on TF/IDF. 
Understanding the score-generation process((("relevance", "controlling", "tuning relevance"))) is critical so you can
tune, modulate, attenuate, and manipulate the score for your particular
business domain.

In practice, simple combinations of queries will get you good search results. 
But to get _great_ search results, you'll often have to start tinkering with
the previously mentioned tuning methods.

Often, applying a boost on a strategic field or rearranging a query to 
emphasize a particular clause will be sufficient to make your results great.
Sometimes you'll need more-invasive changes.  This is usually the case if your
scoring requirements diverge heavily from Lucene's word-based TF/IDF model (for example, you
want to score based on time or distance).

With that said, relevancy tuning is a rabbit hole that you can easily fall into 
and never emerge.  The concept of _most relevant_ is a nebulous target to hit, and
different people often have different ideas about document ranking.  It is easy 
to get into a cycle of constant fiddling without any apparent progress.

We encourage you to avoid this (very tempting) behavior and instead properly
instrument your search results.  Monitor how often your users click the top
result, the top 10, and the first page; how often they execute a secondary query
without selecting a result first; how often they click a result and immediately
go back to the search results, and so forth.

These are all indicators of how relevant your search results are to the user.
If your query is returning highly relevant results, users will select one of
the top-five results, find what they want, and leave.  Irrelevant results cause
users to click around and try new search queries.

Once you have instrumentation in place, tuning your query is simple.  Make a change,
monitor its effect on your users, and repeat as necessary.  The tools outlined in this
chapter are just that: tools.  You have to use them appropriately to propel
your search results into the _great_ category, and the only way to do that is with
strong measurement of user behavior.
