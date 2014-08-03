[[aggregations]]
= Aggregations

[partintro]
--
Up until this point, this book has been dedicated to search.  With search, 
we have a query and we wish to find a subset of documents which
match the query.  We are looking for the proverbial needle(s) in the
haystack.

With aggregations, we zoom out to get an overview of our data.  Instead of 
looking for individual documents, we want to analyze and summarize our complete 
set of data.

// Popular manufacturers? Unusual clumps of needles in the haystack?
- How many needles are in the haystack?
- What is the average length of the needles?
- What is the median length of needle broken down by manufacturer?
- How many needles were added to the haystack each month?

Aggregations can answer more subtle questions too, such as

- What are your most popular needle manufacturers?
- Are there any unusual or anomalous clumps of needles?

Aggregations allow us to ask sophisticated questions of our data.  And yet, while
the functionality is completely different from search, it leverages the
same data-structures.  This means aggregations execute quickly and are
_near-realtime_, just like search.

This is extremely powerful for reporting and dashboards.  Instead of performing
"rollups" of your data (_e.g. that crusty hadoop job that takes a week to run_), 
you can visualize your data in realtime, allowing you to respond immediately.

// Perhaps mention "not precalculated, out of date, and irrelevant"?
// Perhaps "aggs are calculated in the context of the user's search, so you're not showing them that you have 10 4 star hotels on your site, but that you have 10 4 star hotels that *match their criteria*".
Finally, aggregations operate alongside search requests. This means you can
both search/filter documents _and_ perform analytics at the same time, on the
same data, in a single request.  And because aggregations are calculated in the
context of a user's search, you're not just displaying a count of four-star hotels...
you're displaying a count of four-star hotels that _match their search criteria_.

Aggregations are so powerful that many companies have built large Elasticsearch
clusters solely for analytics.
--
