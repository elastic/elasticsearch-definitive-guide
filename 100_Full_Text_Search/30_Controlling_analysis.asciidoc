=== Controlling Analysis

Queries can find only terms that actually ((("full text search", "controlling analysis")))((("analysis", "controlling")))exist in the inverted index, so it
is important to ensure that the same analysis process is applied both to the
document at index time, and to the query string at search time so that the
terms in the query match the terms in the inverted index.

Although we say _document_, analyzers are determined per field.((("analyzers", "determined per-field"))) Each
field can have a different analyzer, either by configuring a specific analyzer
for that field or by falling back on the type, index, or node defaults.  At
index time, a field's value is analyzed by using the configured or default
analyzer for that field.

For instance, let's add a new field to `my_index`:

[source,js]
--------------------------------------------------
PUT /my_index/_mapping/my_type
{
    "my_type": {
        "properties": {
            "english_title": {
                "type":     "string",
                "analyzer": "english"
            }
        }
    }
}
--------------------------------------------------
// SENSE: 100_Full_Text_Search/30_Analysis.json

Now we can compare how values in the `english_title` field and the `title` field are
analyzed at index time by using the `analyze` API to analyze the word `Foxes`:

[source,js]
--------------------------------------------------
GET /my_index/_analyze?field=my_type.title   <1>
Foxes

GET /my_index/_analyze?field=my_type.english_title <2>
Foxes
--------------------------------------------------
// SENSE: 100_Full_Text_Search/30_Analysis.json

<1> Field `title`, which uses the default `standard` analyzer, will return the
    term `foxes`.

<2> Field `english_title`, which uses the `english` analyzer, will return the term
    `fox`.

This means that, were we to run a low-level `term` query for the exact term
`fox`, the `english_title` field would match but the `title` field would
not.

High-level queries like the `match` query understand field mappings and can
apply the correct analyzer for each field being queried.((("match query", "applying appropriate analyzer to each field"))) We can see this
in action with ((("validate query API")))the `validate-query` API:


[source,js]
--------------------------------------------------
GET /my_index/my_type/_validate/query?explain
{
    "query": {
        "bool": {
            "should": [
                { "match": { "title":         "Foxes"}},
                { "match": { "english_title": "Foxes"}}
            ]
        }
    }
}
--------------------------------------------------
// SENSE: 100_Full_Text_Search/30_Analysis.json

which returns this `explanation`:

    (title:foxes english_title:fox)

The `match` query uses the appropriate analyzer for each field to ensure
that it looks for each term in the correct format for that field.

==== Default Analyzers

While we can specify an analyzer at the field level,((("full text search", "controlling analysis", "default analyzers")))((("analyzers", "default"))) how do we determine which
analyzer is used for a field if none is specified at the field level?

Analyzers can be specified at several levels.  Elasticsearch works through
each level until it finds an analyzer that it can use.  At index time, the
order ((("indexing", "applying analyzers")))is as follows:

* The `analyzer` defined in the field mapping, else
* _The analyzer defined in the `_analyzer` field of the document, else_
* The default `analyzer` for the `type`, which defaults to
* The analyzer named `default` in the index settings, which defaults to
* The analyzer named `default` at node level, which defaults to
* The `standard` analyzer

At search time, the ((("searching", "applying analyzers")))sequence is slightly different:

* _The `analyzer` defined in the query itself, else_
* The `analyzer` defined in the field mapping, else
* The default `analyzer` for the `type`, which defaults to
* The analyzer named `default` in the index settings, which defaults to
* The analyzer named `default` at node level, which defaults to
* The `standard` analyzer

[NOTE]
====
The two lines in italics in the preceding lists highlight differences in the index time sequence and the search time sequence.  The `_analyzer` field allows you to specify a default analyzer for each document (for example, `english`, `french`, `spanish`) while the `analyzer` parameter in the query specifies which analyzer to use on the query string. However, this is not the best way to handle multiple languages
in a single index because of the pitfalls highlighted in <<languages>>.
====

Occasionally, it makes sense to use a different analyzer at index and search
time.((("analyzers", "using different analyzers at index and search time"))) For instance, at index time we may want to index synonyms (for example, for every
occurrence of `quick`, we also index `fast`, `rapid`, and `speedy`). But at
search time, we don't need to search for all of these synonyms.  Instead we
can just look up the single word that the user has entered, be it `quick`,
`fast`, `rapid`, or `speedy`.

To enable this distinction, Elasticsearch also supports ((("index_analyzer parameter")))((("search_analyzer parameter")))the `index_analyzer`
and `search_analyzer` parameters, and((("default_search parameter"))) ((("default_index analyzer")))analyzers named `default_index` and
`default_search`.

Taking these extra parameters into account, the _full_ sequence at index time
really looks like this:

* The `index_analyzer` defined in the field mapping, else
* The `analyzer` defined in the field mapping, else
* The analyzer defined in the `_analyzer` field of the document, else
* The default `index_analyzer` for the `type`, which defaults to
* The default `analyzer` for the `type`, which defaults to
* The analyzer named `default_index` in the index settings, which defaults to
* The analyzer named `default` in the index settings, which defaults to
* The analyzer named `default_index` at node level, which defaults to
* The analyzer named `default` at node level, which defaults to
* The `standard` analyzer

And at search time:

* The `analyzer` defined in the query itself, else
* The `search_analyzer` defined in the field mapping, else
* The `analyzer` defined in the field mapping, else
* The default `search_analyzer` for the `type`, which defaults to
* The default `analyzer` for the `type`, which defaults to
* The analyzer named `default_search` in the index settings, which defaults to
* The analyzer named `default` in the index settings, which defaults to
* The analyzer named `default_search` at node level, which defaults to
* The analyzer named `default` at node level, which defaults to
* The `standard` analyzer

==== Configuring Analyzers in Practice

The sheer number of places where you can specify an analyzer is quite
overwhelming.((("full text search", "controlling analysis", "configuring analyzers in practice")))((("analyzers", "configuring in practice")))  In practice, though, it is pretty simple.

===== Use index settings, not config files

The first thing to remember is that, even though you may start out using
Elasticsearch for a single purpose or a single application such as logging,
chances are that you will find more use cases and end up running several
distinct applications on the same cluster.  Each index needs to be independent
and independently configurable. You don't want to set defaults for one use
case, only to have to override them for another use case later.

This rules out configuring analyzers at the node level.  Additionally,
configuring analyzers at the node level requires changing the config file on every
node and restarting every node, which becomes a maintenance nightmare. It's a
much better idea to keep Elasticsearch running and to manage settings only via
the API.

===== Keep it simple

Most of the time, you will know what fields your documents will contain ahead
of time.  The simplest approach is to set the analyzer for each full-text
field when you create your index or add type mappings.  While this approach is
slightly more verbose, it enables you to easily see which analyzer is being applied
to each field.

Typically, most of your string fields will be exact-value `not_analyzed`
fields such as tags or enums, plus a handful of full-text fields that will
use some default analyzer like `standard` or `english` or some other language.
Then you may have one or two fields that need custom analysis: perhaps the
`title` field needs to be indexed in a way that supports _find-as-you-type_.

You can set the `default` analyzer in the index to the analyzer you want to
use for almost all full-text fields, and just configure the specialized
analyzer on the one or two fields that need it.  If, in your model, you need
a different default analyzer per type, then use the type level `analyzer`
setting instead.

[NOTE]
====
A common work flow for time based data like logging is to create a new index
per day on the fly by just indexing into it.  While this work flow prevents
you from creating your index up front, you can still use 
http://bit.ly/1ygczeq[index templates]
to specify the settings and mappings that a new index should have.
====
