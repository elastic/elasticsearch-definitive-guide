[[partial-matching]]
== Partial Matching

A keen observer will notice  that all the queries so far in this book have
operated on whole terms.((("partial matching")))  To match something, the smallest unit had to be a
single term. You can find only terms that exist in the inverted index.

But what happens if you want to match parts of a term but not the whole thing?
_Partial matching_ allows users to specify a portion of the term they are
looking for and find any words that contain that fragment.

The requirement to match on part of a term is less common in the full-text
search-engine world than you might think.  If you have come from an SQL
background, you likely have, at some stage of your career,
implemented a _poor man's full-text search_ using SQL constructs like this:

[source,js]
--------------------------------------------------
    WHERE text LIKE "*quick*"
      AND text LIKE "*brown*"
      AND text LIKE "*fox*" <1>
--------------------------------------------------

<1> `*fox*` would match ``fox'' and ``foxes.''

Of course, with Elasticsearch, we have the analysis process and the inverted
index that remove the need for such brute-force techniques. To handle the
case of matching both ``fox'' and ``foxes,'' we could simply use a stemmer to
index words in their root form.  There is no need to match partial terms.

That said, on some occasions partial matching can be useful.
Common use ((("partial matching", "common use cases")))cases include the following:

* Matching postal codes, product serial numbers, or other `not_analyzed` values
  that start with a particular prefix or match a wildcard pattern
  or even a regular expression

* _search-as-you-type_&#x2014;displaying the most likely results before the
  user has finished typing the search terms

* Matching in languages like German or Dutch, which contain long compound
  words, like _Weltgesundheitsorganisation_ (World Health Organization)

We will start by examining prefix matching on exact-value `not_analyzed`
fields.
