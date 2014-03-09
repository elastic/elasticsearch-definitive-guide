=== Exact values vs. Full text

Data in Elasticsearch can be broadly divided into two types:
_exact values_ and _full text_.

Exact values are exactly what they sound like.  Examples would be a date or a
user ID, but can also include exact strings like a username or an email
address. The exact value `"Foo"` is not the same as the exact value `"foo"`.
The exact value `2014` is not the same as the exact value `2014-09-15`.

Full text, on the other hand, refers to textual data -- usually written in
some human language -- like the text of a tweet or the body of an email.

****

Full text is often referred to as ``unstructured data'', which is a misnomer
-- natural language is highly structured. The problem is that the rules of
natural languages are complex which makes them difficult for computers to
parse correctly. For instance, consider this sentence:

    May is fun but June bores me.

Does it refer to months or to people?
****

Exact values are easy to query. The decision is binary -- a value either
matches the query, or it doesn't. This kind of query is easy to express with
SQL:

[source,js]
--------------------------------------------------
WHERE name    = "John Smith"
  AND user_id = 2
  AND date    > "2014-09-15"
--------------------------------------------------


Querying full text data is much more subtle. We are not just asking ``Does
this document match the query'', but ``How _well_ does this document match the
query?'' In other words, how _relevant_ is this document to the given query?

We seldom want to match the whole full text field exactly.  Instead, we want
to search *within* text fields. Not only that, but we expect search to
understand our *intent*:

* a search for `"UK"` should also return documents mentioning the `"United
  Kingdom"`

* a search for `"jump"` should also match `"jumped"`, `"jumps"`, `"jumping"`
  and perhaps even `"leap"`

* `"johnny walker"` should match `"Johnnie Walker"` and `"johnnie depp"`
  should match `"Johnny Depp"`

* `"fox news hunting"` should return stories about hunting on Fox News,
  while `"fox hunting news"` should return news stories about fox hunting.

In order to facilitate these types of queries on full text fields,
Elasticsearch first _analyzes_ the text, then uses the results to build
an _inverted index_. We will discuss the inverted index and the
analysis process in the next two sections.







