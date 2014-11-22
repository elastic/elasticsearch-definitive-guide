[[controlling-relevance]]
== Controlling Relevance

Databases that deal purely in structured data (such as dates, numbers, and
string enums) have it easy: they((("relevance", "controlling"))) just have to check whether a document (or a
row, in a relational database) matches the query.

While Boolean yes/no matches are an essential part of full-text search, they
are not enough by themselves. Instead, we also  need to know how relevant each
document is to the query.  Full-text search engines have to not only find the
matching documents, but also sort them by relevance.

Full-text relevance ((("similarity algorithms")))formulae, or _similarity algorithms_,  combine several
factors to produce a single relevance `_score` for each document.  In this
chapter, we examine the various moving parts and discuss how they can be
controlled.

Of course, relevance is not just about full-text queries; it may need to
take structured data into account as well. Perhaps we are looking for a
vacation home with particular features (air-conditioning, sea view, free
WiFi).  The more features that a property has, the more relevant it is. Or
perhaps we want to factor in sliding scales like recency, price, popularity, or
distance, while still taking the relevance of a full-text query into account.

All of this is possible thanks to the powerful scoring infrastructure
available in Elasticsearch.

We will start by looking at the theoretical side of how Lucene calculates
relevance, and then move on to practical examples of how you can control the
process.
