[[practical-scoring-function]]
=== Lucene's Practical Scoring Function

For multiterm queries, Lucene takes((("relevance", "controlling", "Lucene&#x27;s practical scoring function", id="ix_relcontPCF", range="startofrange")))((("Boolean Model"))) the <<boolean-model,Boolean model>>,
<<tfidf,TF/IDF>>, and the <<vector-space-model,vector space model>> and
combines ((("Term Frequency/Inverse Document Frequency  (TF/IDF) similarity algorithm")))((("Vector Space Model"))) them in a single efficient package that collects matching
documents and scores them as it goes.

A multiterm query like

[source,json]
------------------------------
GET /my_index/doc/_search
{
  "query": {
    "match": {
      "text": "quick fox"
    }
  }
}
------------------------------

is rewritten internally to look like this:

[source,json]
------------------------------
GET /my_index/doc/_search
{
  "query": {
    "bool": {
      "should": [
        {"term": { "text": "quick" }},
        {"term": { "text": "fox"   }}
      ]
    }
  }
}
------------------------------

The `bool` query implements the Boolean model and, in this example, will
include only documents that contain either the term `quick` or the term `fox` or
both.

As soon as a document matches a query, Lucene calculates its score for that
query, combining the scores of each matching term.  The formula used for
scoring is called the _practical scoring function_.((("practical scoring function"))) It looks intimidating, but
don't be put off--most of the components you already know. It introduces a
few new elements that we discuss next.

................................
score(q,d)  =  <1>
            queryNorm(q)  <2>
          · coord(q,d)    <3>
          · ∑ (           <4>
                tf(t in d)   <5>
              · idf(t)²      <6>
              · t.getBoost() <7>
              · norm(t,d)    <8>
            ) (t in q)    <4>
................................

<1> `score(q,d)` is the relevance score of document `d` for query `q`.
<2> `queryNorm(q)` is the <<query-norm,_query normalization_ factor>> (new).
<3> `coord(q,d)` is the <<coord,_coordination_ factor>> (new).
<4> The sum of the weights for each term `t` in the query `q` for document `d`.
<5> `tf(t in d)` is the <<tf,term frequency>> for term `t` in document `d`.
<6> `idf(t)` is the <<idf,inverse document frequency>> for term `t`.
<7> `t.getBoost()` is the <<query-time-boosting,_boost_>>  that has been
    applied to the query (new).
<8> `norm(t,d)` is the <<field-norm,field-length norm>>, combined with the
    <<index-boost,index-time field-level boost>>, if any. (new).

You should recognize `score`, `tf`, and `idf`. The  `queryNorm`, `coord`,
`t.getBoost`, and `norm` are new.

We will talk more about <<query-time-boosting,query-time boosting>>  later in
this chapter, but first let's get query normalization, coordination, and
index-time field-level boosting out of the way.

[[query-norm]]
==== Query Normalization Factor

The _query normalization factor_ (`queryNorm`) is ((("practical scoring function", "query normalization factor")))((("query normalization factor")))((("normalization", "query normalization factor")))an attempt to _normalize_ a
query so that the results from one query may be compared with the results of
another.

[TIP]
==================================================

Even though the intent of the query norm is to make results from different
queries comparable, it doesn't work very well. The only purpose of
the relevance `_score` is to sort the results of the current query in the
correct order. You should not try to compare the relevance scores from
different queries.

==================================================

This factor is calculated at the beginning of the query. The actual
calculation depends on the queries involved, but a typical implementation is as follows:

..........................
queryNorm = 1 / √sumOfSquaredWeights <1>
..........................
<1> The `sumOfSquaredWeights` is calculated by adding together the IDF of each
    term in the query, squared.

TIP: The same query normalization factor is applied to every document, and you
have no way of changing it. For all intents and purposes, it can be ignored.


[[coord]]
==== Query Coordination

The _coordination factor_ (`coord`) is used to((("coordination factor (coord)")))((("query coordination")))((("practical scoring function", "coordination factor"))) reward documents that contain a
higher percentage of the query terms. The more query terms that appear in
the document, the greater the chances that the document is a good match for
the query.

Imagine that we have a query for `quick brown fox`, and that the
weight for each term is 1.5.  Without the coordination factor, the score would
just be the sum of the weights of the terms in a document. For instance:

* Document with `fox` -> score: 1.5
* Document with `quick fox` -> score: 3.0
* Document with `quick brown fox` -> score: 4.5

The coordination factor multiplies the score by the number of matching terms
in the document, and divides it by the total number of terms in the query.
With the coordination factor, the scores would be as follows:

* Document with `fox` -> score: `1.5 * 1 / 3` = 0.5
* Document with `quick fox` -> score: `3.0 * 2 / 3` = 2.0
* Document with `quick brown fox` -> score: `4.5 * 3 / 3` = 4.5

The coordination factor results in the document that contains all three terms
being much more relevant than the document that contains just two of them.

Remember that the query for `quick brown fox` is rewritten into a `bool` query
like this:

[source,json]
-------------------------------
GET /_search
{
  "query": {
    "bool": {
      "should": [
        { "term": { "text": "quick" }},
        { "term": { "text": "brown" }},
        { "term": { "text": "fox"   }}
      ]
    }
  }
}
-------------------------------

The `bool` query uses query coordination by default for all `should` clauses,
but it does allow you to disable coordination.  Why might you want to do this?
Well, usually the answer is, you don't.  Query coordination is usually a good
thing.  When you use a `bool` query to wrap several high-level queries like
the `match` query, it also makes sense to leave coordination enabled. The more
clauses that match, the higher the degree of overlap between your search
request and the documents that are returned.

However, in some advanced use cases, it might make sense to disable
coordination.  Imagine that you are looking for the synonyms `jump`, `leap`, and
`hop`.  You don't care how many of these synonyms are present, as they all
represent the same concept. In fact, only one of the synonyms is likely to be
present.  This would be a good case for disabling the coordination factor:

[source,json]
-------------------------------
GET /_search
{
  "query": {
    "bool": {
      "disable_coord": true,
      "should": [
        { "term": { "text": "jump" }},
        { "term": { "text": "hop"  }},
        { "term": { "text": "leap" }}
      ]
    }
  }
}
-------------------------------

When you use synonyms (see <<synonyms>>), this is exactly what
happens internally: the rewritten query disables coordination for the
synonyms. ((("synonyms", "query coordination and")))  Most use cases for disabling coordination are handled
automatically; you don't need to worry about it.


[[index-boost]]
==== Index-Time Field-Level Boosting

We will talk about _boosting_ a field--making it ((("indexing", "field-level index time boosts")))((("boosting", "index time field-level boosting")))((("practical scoring function", "index time field-level boosting")))more important than other
fields--at query time in <<query-time-boosting>>.  It is also possible
to apply a boost to a field at index time.  Actually, this boost is applied to
every term in the field, rather than to the field itself.

To store this boost value in the index without using more space
than necessary, this field-level index-time boost is combined with the ((("field-length norm")))field-length norm (see  <<field-norm>>) and stored in the index as a single byte.
This is the value returned by `norm(t,d)` in the preceding formula.

[WARNING]
=========================================

We strongly recommend against using field-level index-time boosts for a few
reasons:

*  Combining the boost with the field-length norm and storing it in a single
    byte means that the field-length norm loses precision. The result is that
    Elasticsearch is unable to distinguish between a field containing three words
    and a field containing five words.

*  To change an index-time boost, you have to reindex all your documents.
    A query-time boost, on the other hand, can be changed with every query.

*  If a field with an index-time boost has multiple values, the boost is
    multiplied by itself for every value, dramatically increasing
    the weight for that field.

<<query-time-boosting,Query-time boosting>> is a much simpler, cleaner, more
flexible option.

=========================================

With query normalization, coordination, and index-time boosting out of the way,
we can now move on to the most useful tool for influencing the relevance
calculation: query-time boosting.((("relevance", "controlling", "Lucene&#x27;s practical scoring function", range="endofrange", startref="ix_relcontPCF")))


