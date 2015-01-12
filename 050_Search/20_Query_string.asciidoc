[[search-lite]]
=== Search _Lite_

There are two forms of the `search` API: a ``lite'' _query-string_ version
that expects all its((("searching", "query string searches")))((("query strings", "searching with"))) parameters to be passed in the query string, and the full
_request body_ version that expects a JSON request body and uses a
rich search language called the query DSL.

The query-string search is useful for running ad hoc queries from the
command line. For instance, this query finds all documents of type `tweet` that
contain the word `elasticsearch` in the `tweet` field:

[source,js]
--------------------------------------------------
GET /_all/tweet/_search?q=tweet:elasticsearch
--------------------------------------------------
// SENSE: 050_Search/20_Query_string.json

The next query looks for `john` in the `name` field and `mary` in the
`tweet` field. The actual query is just

    +name:john +tweet:mary

but the _percent encoding_ needed for query-string parameters makes it appear
more cryptic than it really is:

[source,js]
--------------------------------------------------
GET /_search?q=%2Bname%3Ajohn+%2Btweet%3Amary
--------------------------------------------------
// SENSE: 050_Search/20_Query_string.json


The `+` prefix indicates conditions that _must_ be satisfied for our query to
match. Similarly a `-` prefix would indicate conditions that _must not_
match.  All conditions without a `+` or `-` are optional--the more that match,
the more relevant the document.

[[all-field-intro]]
==== The _all Field

This simple search returns all documents that contain the word `mary`:

[source,js]
--------------------------------------------------
GET /_search?q=mary
--------------------------------------------------
// SENSE: 050_Search/20_All_field.json


In the previous examples, we searched for words in the `tweet` or
`name` fields. However, the results from this query mention `mary` in
three fields:

* A user whose name is Mary
* Six tweets by Mary
* One tweet directed at @mary

How has Elasticsearch managed to find results in three different fields?

When you index a document, Elasticsearch takes the string values of all of
its fields and concatenates them into one big string, which it indexes as
the special `_all` field.((("_all field", sortas="all field"))) For example, when we index this document:

[source,js]
--------------------------------------------------
{
    "tweet":    "However did I manage before Elasticsearch?",
    "date":     "2014-09-14",
    "name":     "Mary Jones",
    "user_id":  1
}
--------------------------------------------------


it's as if we had added an extra field called `_all` with this value:

[source,js]
--------------------------------------------------
"However did I manage before Elasticsearch? 2014-09-14 Mary Jones 1"
--------------------------------------------------


The query-string search uses the `_all` field unless another
field name has been specified.

TIP: The `_all` field is a useful feature while you are getting started with
a new application. Later, you will find that you have more control over
your search results if you query specific fields instead of the `_all`
field.  When the `_all` field is no longer useful to you, you can
disable it, as explained in <<all-field>>.

[[query-string-query]]
[role="pagebreak-before"]
==== More Complicated Queries

The next query searches for tweets, using the following criteria:

* The `name` field contains `mary` or `john`
* The `date` is greater than `2014-09-10`
* The +_all+ field contains either of the words `aggregations` or `geo`

[source,js]
--------------------------------------------------
+name:(mary john) +date:>2014-09-10 +(aggregations geo)
--------------------------------------------------
// SENSE: 050_Search/20_All_field.json

As a properly encoded query string, this looks like the slightly less
readable result:

[source,js]
--------------------------------------------------
?q=%2Bname%3A(mary+john)+%2Bdate%3A%3E2014-09-10+%2B(aggregations+geo)
--------------------------------------------------

As you can see from the preceding examples, this _lite_ query-string search is
surprisingly powerful.((("query strings", "syntax, reference for"))) Its query syntax, which is explained in detail in the
http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax[Query String Syntax]
reference docs, allows us to express quite complex queries succinctly. This
makes it great for throwaway queries from the command line or during
development.

However, you can also see that its terseness can make it cryptic and
difficult to debug. And it's fragile--a slight syntax error in the query
string, such as a misplaced `-`, `:`, `/`, or `"`, and it will return an error
instead of results.

Finally, the query-string search allows any user to run potentially slow, heavy
queries on any field in your index, possibly exposing private information or
even bringing your cluster to its knees!

[TIP]
==================================================
For these reasons, we don't recommend exposing query-string searches directly to
your users, unless they are power users who can be trusted with your data and
with your cluster.
==================================================

Instead, in production we usually rely on the full-featured _request body_
search API, which does all of this, plus a lot more. Before we get there,
though, we first need to take a look at how our data is indexed in
Elasticsearch.

