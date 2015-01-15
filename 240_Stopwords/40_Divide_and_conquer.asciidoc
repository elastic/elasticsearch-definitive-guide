[[common-terms]]
=== Divide and Conquer

The terms in a query string can be divided into more-important (low-frequency)
and less-important (high-frequency) terms.((("stopwords", "low and high frequency terms"))) Documents that match only the less
important terms are probably of very little interest.  Really, we want
documents that match as many of the more important terms as possible.

The `match` query accepts ((("cutoff_frequency parameter")))((("match query", "cutoff_frequency parameter")))a `cutoff_frequency` parameter, which allows it to
divide the terms in the query string into a low-frequency and high-frequency
group.((("term frequency", "cutoff_frequency parameter in match query"))) The low-frequency group (more-important terms) form the bulk of the
query, while the high-frequency group (less-important terms) is used only for
scoring, not for matching. By treating these two groups differently, we can
gain a real boost of speed on previously slow queries.

.Domain-Specific Stopwords
*********************************************

One of the benefits of `cutoff_frequency` is that you get _domain-specific_
stopwords for free.((("domain specific stopwords")))((("stopwords", "domain specific"))) For instance, a website about movies may use the words
_movie_, _color_, _black_, and _white_ so often that they could be
considered almost meaningless.  With the `stop` token filter, these domain-specific terms would have to be added to the stopwords list manually. However,
because the `cutoff_frequency` looks at the actual frequency of terms in the
index,  these words would be classified as _high frequency_ automatically.

*********************************************

Take this query as an example:

[source,json]
---------------------------------
{
  "match": {
    "text": {
      "query": "Quick and the dead",
      "cutoff_frequency": 0.01 <1>
    }
}
---------------------------------
<1> Any term that occurs in more than 1% of documents is considered to be high
    frequency. The `cutoff_frequency` can be specified as a fraction (`0.01`)
    or as an absolute number (`5`).

This query uses the `cutoff_frequency` to first divide the query terms into a
low-frequency group (`quick`, `dead`) and a high-frequency group (`and`,
`the`). Then, the query is rewritten to produce the following `bool` query:

[source,json]
---------------------------------
{
  "bool": {
    "must": { <1>
      "bool": {
        "should": [
          { "term": { "text": "quick" }},
          { "term": { "text": "dead"  }}
        ]
      }
    },
    "should": { <2>
      "bool": {
        "should": [
          { "term": { "text": "and" }},
          { "term": { "text": "the" }}
        ]
      }
    }
  }
}
---------------------------------
<1> At least one low-frequency/high-importance term _must_ match.
<2> High-frequency/low-importance terms are entirely optional.

The `must` clause means that at least one of the low-frequency terms&#x2014;`quick` or `dead`&#x2014;_must_ be present for a document to be considered a
match. All other documents are excluded.  The `should` clause then looks for
the high-frequency terms `and` and `the`,  but only in the documents collected
by the `must` clause. The sole job of the `should` clause is to score a
document like ``Quick _and the_ dead'' higher than ``_The_ quick but
dead''.  This approach greatly reduces the number of documents that need to be
examined and scored.

[TIP]
==================================================

Setting the operator parameter to `and` would make _all_ low-frequency terms
required, and score documents that contain _all_ high-frequency terms higher.
However, matching documents would not be required to contain all high-frequency terms.  If you would prefer all low- and high-frequency terms to be
required, you should use a `bool` query instead.   As we saw in
<<stopwords-and>>, this is already an efficient query.

==================================================

==== Controlling Precision

The `minimum_should_match` parameter can be combined with `cutoff_frequency`
but it applies to only the low-frequency terms.((("stopwords", "low and high frequency terms", "controlling precision")))((("minimum_should_match parameter", "controlling precision")))  This query:

[source,json]
---------------------------------
{
  "match": {
    "text": {
      "query": "Quick and the dead",
      "cutoff_frequency": 0.01,
      "minimum_should_match": "75%"
    }
}
---------------------------------

would be rewritten as follows:

[source,json]
---------------------------------
{
  "bool": {
    "must": {
      "bool": {
        "should": [
          { "term": { "text": "quick" }},
          { "term": { "text": "dead"  }}
        ],
        "minimum_should_match": 1 <1>
      }
    },
    "should": { <2>
      "bool": {
        "should": [
          { "term": { "text": "and" }},
          { "term": { "text": "the" }}
        ]
      }
    }
  }
}
---------------------------------
<1> Because there are only two terms, the original 75% is rounded down
    to `1`, that is: _one out of two low-terms must match_.
<2> The high-frequency terms are still optional and used only for scoring.

==== Only High-Frequency Terms

An `or` query for high-frequency((("stopwords", "low and high frequency terms", "only high frequency terms"))) terms only&#x2014;``To be, or not to be''&#x2014;is
the worst case for performance. It is pointless to score _all_ the
documents that contain only one of these terms in order to return just the top
10 matches. We are really interested only in documents in which the terms all occur
together, so in the case where there are no low-frequency terms, the query is
rewritten to make all high-frequency terms required:

[source,json]
---------------------------------
{
  "bool": {
    "must": [
      { "term": { "text": "to" }},
      { "term": { "text": "be" }},
      { "term": { "text": "or" }},
      { "term": { "text": "not" }},
      { "term": { "text": "to" }},
      { "term": { "text": "be" }}
    ]
  }
}
---------------------------------

==== More Control with Common Terms

While the high/low frequency functionality in the `match` query is useful,
sometimes you want more control((("stopwords", "low and high frequency terms", "more control over common terms"))) over how the high- and low-frequency groups
should be handled.  The `match` query exposes a subset of the
functionality available in the `common` terms query.((("common terms query")))

For instance, we could make all low-frequency terms required, and score only
documents that have 75% of all high-frequency terms with a query like this:

[source,json]
---------------------------------
{
  "common": {
    "text": {
      "query":                  "Quick and the dead",
      "cutoff_frequency":       0.01,
      "low_freq_operator":      "and",
      "minimum_should_match": {
        "high_freq":            "75%"
      }
    }
  }
}
---------------------------------

See the http://bit.ly/1wdS2Qo[`common` terms query] reference page for more options.

