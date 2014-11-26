
[[aggregations-and-analysis]]
=== Aggregations and Analysis

Some aggregations, such as the `terms` bucket, operate((("analysis", "aggregations and")))((("aggregations", "and analysis"))) on string fields.  And
string fields may be either `analyzed` or `not_analyzed`, which begs the question:
how does analysis affect aggregations?((("strings", "analyzed or not_analyzed string fields")))((("not_analyzed fields")))((("analyzed fields")))

The answer is "a lot," but it is best shown through an example.  First, index
some documents representing various states in the US:

[source,js]
----
POST /agg_analysis/data/_bulk
{ "index": {}}
{ "state" : "New York" }
{ "index": {}}
{ "state" : "New Jersey" }
{ "index": {}}
{ "state" : "New Mexico" }
{ "index": {}}
{ "state" : "New York" }
{ "index": {}}
{ "state" : "New York" }
----

We want to build a list of unique states in our dataset, complete with counts.
Simple--let's use a `terms` bucket:

[source,js]
----
GET /agg_analysis/data/_search?search_type=count
{
    "aggs" : {
        "states" : {
            "terms" : {
                "field" : "state"
            }
        }
    }
}
----

This gives us these results:

[source,js]
----
{
...
   "aggregations": {
      "states": {
         "buckets": [
            {
               "key": "new",
               "doc_count": 5
            },
            {
               "key": "york",
               "doc_count": 3
            },
            {
               "key": "jersey",
               "doc_count": 1
            },
            {
               "key": "mexico",
               "doc_count": 1
            }
         ]
      }
   }
}
----

Oh dear, that's not at all what we want!  Instead of counting states, the aggregation
is counting individual words.  The underlying reason is simple: aggregations
are built from the inverted index, and the inverted index is _post-analysis_.

When we added those documents to Elasticsearch, the string `"New York"` was
analyzed/tokenized into `["new", "york"]`.  These individual tokens were then
used to populate fielddata, and ultimately we see counts for `new` instead of
`New York`.

This is obviously not the behavior that we wanted, but luckily it is easily
corrected.

We need to define a multifield for +state+ and set it to `not_analyzed`.  This
will prevent `New York` from being analyzed, which means it will stay a single
token in the aggregation.  Let's try the whole process over, but this time
specify a _raw_ multifield:

[source,js]
----
DELETE /agg_analysis/
PUT /agg_analysis
{
  "mappings": {
    "data": {
      "properties": {
        "state" : {
          "type": "string",
          "fields": {
            "raw" : {
              "type": "string",
              "index": "not_analyzed"<1>
            }
          }
        }
      }
    }
  }
}

POST /agg_analysis/data/_bulk
{ "index": {}}
{ "state" : "New York" }
{ "index": {}}
{ "state" : "New Jersey" }
{ "index": {}}
{ "state" : "New Mexico" }
{ "index": {}}
{ "state" : "New York" }
{ "index": {}}
{ "state" : "New York" }

GET /agg_analysis/data/_search?search_type=count
{
  "aggs" : {
    "states" : {
        "terms" : {
            "field" : "state.raw" <2>
        }
    }
  }
}
----
<1> This time we explicitly map the +state+ field and include a `not_analyzed` sub-field.
<2> The aggregation is run on +state.raw+ instead of +state+.

Now when we run our aggregation, we get results that make sense:

[source,js]
----
{
...
   "aggregations": {
      "states": {
         "buckets": [
            {
               "key": "New York",
               "doc_count": 3
            },
            {
               "key": "New Jersey",
               "doc_count": 1
            },
            {
               "key": "New Mexico",
               "doc_count": 1
            }
         ]
      }
   }
}
----

In practice, this kind of problem is easy to spot.  Your aggregations
will simply return strange buckets, and you'll remember the analysis issue.
It is a generalization, but there are not many instances where you want to use
an analyzed  field in an aggregation.  When in doubt, add a multifield so
you have the option for both.((("analyzed fields", "aggregations and")))

==== High-Cardinality Memory Implications

There is another reason to avoid aggregating analyzed fields: high-cardinality
fields consume a large amount of memory when loaded into fielddata.((("memory usage", "high-cardinality fields")))((("cardinality", "high-cardinality fields, memory use issues")))  The
analysis process often (although not always) generates a large number of tokens,
many of  which are unique.  This increases the overall cardinality of the field
and contributes to more memory pressure.((("analysis", "high-cardinality fields, memory use issues")))

Some types of analysis are _extremely_ unfriendly with regards to memory.
Consider an n-gram analysis process.((("n-grams", "memory use issues associated with")))  The term +New York+ might be n-grammed into
the following tokens:

- `ne`
- `ew`
- +w{nbsp}+
- +{nbsp}y+
- `yo`
- `or`
- `rk`

You can imagine how the n-gramming process creates a huge number of unique tokens,
especially when analyzing paragraphs of text.  When these are loaded into memory,
you can easily exhaust your heap space.

So, before aggregating across fields, take a second to verify that the fields are
`not_analyzed`.  And if you want to aggregate analyzed fields, ensure that the analysis
process is not creating an obscene number of tokens.

[TIP]
==================================================

At the end of the day, it doesn't matter whether a field is `analyzed` or
`not_analyzed`. The more unique values in a field--the higher the
cardinality of the field--the more memory that is required. This is
especially true for string fields, where every unique string must be held in
memory--longer strings use more memory.

==================================================

