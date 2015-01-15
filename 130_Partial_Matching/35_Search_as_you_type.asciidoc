=== Index-Time Search-as-You-Type

The first step to setting up index-time search-as-you-type is to((("search-as-you-type", "index time")))((("partial matching", "index time search-as-you-type"))) define our
analysis chain, which we discussed  in <<configuring-analyzers>>, but we will
go over the steps again here.

==== Preparing the Index

The first step is to configure a ((("partial matching", "index time search-as-you-type", "preparing the index")))custom `edge_ngram` token filter,((("edge_ngram token filter"))) which we
will call the `autocomplete_filter`:

[source,js]
--------------------------------------------------
{
    "filter": {
        "autocomplete_filter": {
            "type":     "edge_ngram",
            "min_gram": 1,
            "max_gram": 20
        }
    }
}
--------------------------------------------------

This configuration says that, for any term that this token filter receives,
it should produce an n-gram anchored to the start of the word of minimum
length 1 and maximum length 20.

Then we need to use this token filter in a custom analyzer,((("analyzers", "autocomplete custom analyzer"))) which we will call
the `autocomplete` analyzer:

[source,js]
--------------------------------------------------
{
    "analyzer": {
        "autocomplete": {
            "type":      "custom",
            "tokenizer": "standard",
            "filter": [
                "lowercase",
                "autocomplete_filter" <1>
            ]
        }
    }
}
--------------------------------------------------
<1> Our custom edge-ngram token filter

This analyzer will tokenize a string into individual terms by using the
`standard` tokenizer, lowercase each term, and then produce edge n-grams of each
term, thanks to our `autocomplete_filter`.

The full request to create the index and instantiate the token filter and
analyzer looks like this:

[source,js]
--------------------------------------------------
PUT /my_index
{
    "settings": {
        "number_of_shards": 1, <1>
        "analysis": {
            "filter": {
                "autocomplete_filter": { <2>
                    "type":     "edge_ngram",
                    "min_gram": 1,
                    "max_gram": 20
                }
            },
            "analyzer": {
                "autocomplete": {
                    "type":      "custom",
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "autocomplete_filter" <3>
                    ]
                }
            }
        }
    }
}
--------------------------------------------------
// SENSE: 130_Partial_Matching/35_Search_as_you_type.json

<1> See <<relevance-is-broken>>.
<2> First we define our custom token filter.
<3> Then we use it in an analyzer.

You can test this new analyzer to make sure it is behaving correctly by using
the `analyze` API:

[source,js]
--------------------------------------------------
GET /my_index/_analyze?analyzer=autocomplete
quick brown
--------------------------------------------------
// SENSE: 130_Partial_Matching/35_Search_as_you_type.json

The results show us that the analyzer is working correctly. It returns these
terms:

* `q`
* `qu`
* `qui`
* `quic`
* `quick`
* `b`
* `br`
* `bro`
* `brow`
* `brown`

To use the analyzer, we need to apply it to a field, which we can do
with((("update-mapping API, applying custom autocomplete analyzer to a field"))) the `update-mapping` API:

[source,js]
--------------------------------------------------
PUT /my_index/_mapping/my_type
{
    "my_type": {
        "properties": {
            "name": {
                "type":     "string",
                "analyzer": "autocomplete"
            }
        }
    }
}
--------------------------------------------------
// SENSE: 130_Partial_Matching/35_Search_as_you_type.json

Now, we can index some test documents:

[source,js]
--------------------------------------------------
POST /my_index/my_type/_bulk
{ "index": { "_id": 1            }}
{ "name": "Brown foxes"    }
{ "index": { "_id": 2            }}
{ "name": "Yellow furballs" }
--------------------------------------------------
// SENSE: 130_Partial_Matching/35_Search_as_you_type.json

==== Querying the Field

If you test out a query for ``brown fo'' by using ((("partial matching", "index time search-as-you-type", "querying the field")))a simple `match` query

[source,js]
--------------------------------------------------
GET /my_index/my_type/_search
{
    "query": {
        "match": {
            "name": "brown fo"
        }
    }
}
--------------------------------------------------
// SENSE: 130_Partial_Matching/35_Search_as_you_type.json

you will see that _both_ documents match, even though the `Yellow furballs`
doc contains neither `brown` nor `fo`:

[source,js]
--------------------------------------------------
{

  "hits": [
     {
        "_id": "1",
        "_score": 1.5753809,
        "_source": {
           "name": "Brown foxes"
        }
     },
     {
        "_id": "2",
        "_score": 0.012520773,
        "_source": {
           "name": "Yellow furballs"
        }
     }
  ]
}
--------------------------------------------------

As always, the `validate-query` API shines some light:

[source,js]
--------------------------------------------------
GET /my_index/my_type/_validate/query?explain
{
    "query": {
        "match": {
            "name": "brown fo"
        }
    }
}
--------------------------------------------------
// SENSE: 130_Partial_Matching/35_Search_as_you_type.json

The `explanation` shows us that the query is looking for edge n-grams of every
word in the query string:

    name:b name:br name:bro name:brow name:brown name:f name:fo

The `name:f` condition is satisfied by the second document because
`furballs` has been indexed as `f`, `fu`, `fur`, and so forth.  In retrospect, this
is not surprising.  The same `autocomplete` analyzer is being applied both at
index time and at search time, which in most situations is the right thing to
do. This is one of the few occasions when it makes sense to break this rule.

We want to ensure that our inverted index contains edge n-grams of every word,
but we want to match only the full words that the user has entered (`brown` and `fo`). ((("analyzers", "changing search analyzer from index analyzer"))) We can do this by using the `autocomplete` analyzer at
index time and the `standard` analyzer at search time.  One way to change the
search analyzer is just to specify it in the query:


[source,js]
--------------------------------------------------
GET /my_index/my_type/_search
{
    "query": {
        "match": {
            "name": {
                "query":    "brown fo",
                "analyzer": "standard" <1>
            }
        }
    }
}
--------------------------------------------------
// SENSE: 130_Partial_Matching/35_Search_as_you_type.json

<1> This overrides the `analyzer` setting on the `name` field.

Alternatively, we can specify ((("search_analyzer parameter")))((("index_analyzer parameter")))the `index_analyzer` and `search_analyzer` in
the mapping for the `name` field itself. Because we want to change only the
`search_analyzer`, we can update the existing mapping without having to
reindex our data:


[source,js]
--------------------------------------------------
PUT /my_index/my_type/_mapping
{
    "my_type": {
        "properties": {
            "name": {
                "type":            "string",
                "index_analyzer":  "autocomplete", <1>
                "search_analyzer": "standard" <2>
            }
        }
    }
}
--------------------------------------------------
// SENSE: 130_Partial_Matching/35_Search_as_you_type.json

<1> Use the `autocomplete` analyzer at index time to produce edge n-grams of
    every term.

<2> Use the `standard` analyzer at search time to search only on the terms
    that the user has entered.


If we were to repeat the `validate-query` request, it would now give us this
explanation:

    name:brown name:fo

Repeating our query correctly returns just the `Brown foxes`
document.

Because most of the work has been done at index time, all this query needs to
do is to look up the two terms `brown` and `fo`, which is much more efficient
than the `match_phrase_prefix` approach of having to find all terms beginning
with `fo`.

.Completion Suggester
*************************************************

Using edge n-grams for search-as-you-type is easy to set up, flexible, and
fast.  However, sometimes it is not fast enough.  Latency matters, especially
when you are trying to provide instant feedback.  Sometimes the fastest way of
searching is not to search at all.

The http://bit.ly/1IChV5j[completion suggester] in
Elasticsearch((("completion suggester"))) takes a completely different approach.  You feed it a list
of all possible completions, and it builds them into a _finite state
transducer_, an((("Finite State Transducer"))) optimized data structure that resembles a big graph.  To
search for suggestions, Elasticsearch starts at the beginning of the graph and
moves character by character along the matching path. Once it has run out of
user input, it looks at all possible endings of the  current path to produce a
list of suggestions.

This data structure lives in memory and makes prefix lookups extremely fast,
much faster than any term-based query could be.  It is an excellent match for
autocompletion of names and brands, whose words are usually organized in a
common order: ``Johnny Rotten'' rather than ``Rotten Johnny.''

When word order is less predictable, edge n-grams can be a better solution
than the completion suggester.  This particular cat may be skinned in myriad
ways.

*************************************************

==== Edge n-grams and Postcodes

The edge n-gram approach can((("postcodes (UK), partial matching with", "using edge n-grams")))((("edge n-grams", "and postcodes"))) also be used for structured data, such as the
postcodes example from <<prefix-query,earlier in this chapter>>.  Of course,
the `postcode` field would need to be `analyzed` instead of `not_analyzed`, but
you could use the `keyword` tokenizer((("keyword tokenizer", "using for values treated as not_analyzed")))((("not_analyzed fields", "using keyword tokenizer with"))) to treat the postcodes as if they were
`not_analyzed`.

[TIP]
==================================================

The `keyword` tokenizer is the no-operation tokenizer, the tokenizer that does
nothing.  Whatever string it receives as input, it emits exactly the same
string as a single token.  It can therefore be used for values that we would
normally treat as `not_analyzed` but that require some other analysis
transformation such as lowercasing.

==================================================

This example uses the `keyword` tokenizer to convert the postcode string into a token stream, so that we can use the edge n-gram token filter:

[source,js]
--------------------------------------------------
{
    "analysis": {
        "filter": {
            "postcode_filter": {
                "type":     "edge_ngram",
                "min_gram": 1,
                "max_gram": 8
            }
        },
        "analyzer": {
            "postcode_index": { <1>
                "tokenizer": "keyword",
                "filter":    [ "postcode_filter" ]
            },
            "postcode_search": { <2>
                "tokenizer": "keyword"
            }
        }
    }
}
--------------------------------------------------
// SENSE: 130_Partial_Matching/35_Postcodes.json

<1> The `postcode_index` analyzer would use the `postcode_filter`
    to turn postcodes into edge n-grams.
<2> The `postcode_search` analyzer would treat search terms as
    if they were `not_indexed`.

