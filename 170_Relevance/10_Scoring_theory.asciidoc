[[scoring-theory]]
=== Theory Behind Relevance Scoring

Lucene (and thus Elasticsearch) uses the
http://en.wikipedia.org/wiki/Standard_Boolean_model[_Boolean model_]
to find matching documents,((("relevance scores", "theory behind", id="ix_relscore", range="startofrange")))((("Boolean Model"))) and a formula called the
<<practical-scoring-function,_practical scoring function_>>
to calculate relevance.  This formula borrows concepts from
http://en.wikipedia.org/wiki/Tfidf[_term frequency/inverse document frequency_] and the
http://en.wikipedia.org/wiki/Vector_space_model[_vector space model_]
but adds more-modern features like a coordination factor, field length
normalization, and term or query clause boosting.

[NOTE]
====
Don't be alarmed!  These concepts are not as complicated as the names make
them appear. While this section mentions algorithms, formulae, and mathematical
models, it is intended for consumption by mere humans.  Understanding the
algorithms themselves is not as important as understanding the factors that
influence the outcome.
====

[[boolean-model]]
==== Boolean Model

The _Boolean model_ simply applies the `AND`, `OR`, and `NOT` conditions
expressed in the query to find all the documents that match.((("and operator")))((("not operator")))((("or operator"))) A query for

    full AND text AND search AND (elasticsearch OR lucene)

will include only documents that contain all of the terms `full`, `text`, and
`search`, and either `elasticsearch` or `lucene`.

This process is simple and fast.  It is used to exclude any documents that
cannot possibly match the query.

[[tfidf]]
==== Term Frequency/Inverse Document Frequency (TF/IDF)

Once we have a list of matching documents, they need to be ranked by
relevance.((("Term Frequency/Inverse Document Frequency  (TF/IDF) similarity algorithm"))) Not all documents will contain all the terms, and some terms are
more important than others. The relevance score of the whole document
depends (in part) on the _weight_ of each query term that appears in
that document.

The weight of a term is determined by three factors, which we already
introduced in <<relevance-intro>>. The formulae are included for interest's
sake, but you are not required to remember them.

[[tf]]
===== Term frequency

How often does the term appear in this document?((("Term Frequency/Inverse Document Frequency  (TF/IDF) similarity algorithm", "term frequency"))) The more often, the
_higher_ the weight.  A field containing five mentions of the same term is
more likely to be relevant than a field containing just one mention.
The term frequency is calculated as follows:

..........................
tf(t in d) = √frequency <1>
..........................
<1> The term frequency (`tf`) for term `t` in document `d` is the square root
    of the number of times the term appears in the document.

If you don't care about how often a term appears in a field, and all you care
about is that the term is present, then you can disable term frequencies in
the field mapping:

[source,json]
--------------------------
PUT /my_index
{
  "mappings": {
    "doc": {
      "properties": {
        "text": {
          "type":          "string",
          "index_options": "docs" <1>
        }
      }
    }
  }
}
--------------------------
<1> Setting `index_options` to `docs` will disable term frequencies and term
    positions. A field with this mapping will not count how many times a term
    appears, and will not be usable for phrase or proximity queries.
    Exact-value `not_analyzed` string fields use this setting by default.

[[idf]]
===== Inverse document frequency

How often does the term appear in all documents in the collection?  The more
often, the _lower_ the weight.((("inverse document frequency")))((("Term Frequency/Inverse Document Frequency  (TF/IDF) similarity algorithm", "inverse document frequency"))) Common terms like `and` or `the` contribute
little to relevance, as they appear in most documents, while uncommon terms
like `elastic` or `hippopotamus` help us zoom in on the most interesting
documents. The inverse document frequency is calculated as follows:

..........................
idf(t) = 1 + log ( numDocs / (docFreq + 1)) <1>
..........................
<1> The inverse document frequency (`idf`) of term `t` is the
    logarithm of the number of documents in the index, divided by
    the number of documents that contain the term.


[[field-norm]]
===== Field-length norm

How long is the field?  ((("Term Frequency/Inverse Document Frequency  (TF/IDF) similarity algorithm", "field-length norm")))((("field-length norm")))The shorter the field, the _higher_ the weight. If a
term appears in a short field, such as a `title` field, it is more likely that
the content of that field is _about_ the term than if the same term appears
in a much bigger `body` field. The field length norm is calculated as follows:

..........................
norm(d) = 1 / √numTerms <1>
..........................
<1> The field-length norm (`norm`) is the inverse square root of the number of terms
    in the field.

While the field-length ((("string fields", "field-length norm")))norm is important for full-text search, many other
fields don't need norms. Norms consume approximately 1 byte per `string` field
per document in the index, whether or not a document contains the field.  Exact-value `not_analyzed` string fields have norms disabled by default,
but you can use the field mapping to disable norms on `analyzed` fields as
well:

[source,json]
--------------------------
PUT /my_index
{
  "mappings": {
    "doc": {
      "properties": {
        "text": {
          "type": "string",
          "norms": { "enabled": false } <1>
        }
      }
    }
  }
}
--------------------------
<1> This field will not take the field-length norm into account.  A long field
    and a short field will be scored as if they were the same length.

For use cases such as logging, norms are not useful.  All you care about is
whether a field contains a particular error code or a particular browser
identifier. The length of the field does not affect the outcome.  Disabling
norms can save a significant amount of memory.

===== Putting it together

These three factors--term frequency, inverse document frequency, and field-length norm--are calculated and stored at index time.((("weight", "calculation of")))  Together, they are
used to calculate the _weight_ of a single term in a particular document.

[TIP]
==================================================

When we refer to _documents_ in the preceding formulae, we are actually talking about
a field within a document.  Each field has its own inverted index and thus,
for TF/IDF purposes, the value of the field is the value of the document.

==================================================

When we run a simple `term` query with `explain` set to `true` (see
<<explain>>), you will see that the only factors involved in calculating the
score are the ones explained in the preceding sections:

[role="pagebreak-before"]
[source,json]
----------------------------
PUT /my_index/doc/1
{ "text" : "quick brown fox" }

GET /my_index/doc/_search?explain
{
  "query": {
    "term": {
      "text": "fox"
    }
  }
}
----------------------------

The (abbreviated) `explanation` from the preceding request is as follows:

.......................................................
weight(text:fox in 0) [PerFieldSimilarity]:  0.15342641 <1>
result of:
    fieldWeight in 0                         0.15342641
    product of:
        tf(freq=1.0), with freq of 1:        1.0 <2>
        idf(docFreq=1, maxDocs=1):           0.30685282 <3>
        fieldNorm(doc=0):                    0.5 <4>
.......................................................
<1> The final `score` for term `fox` in field `text` in the document with internal
    Lucene doc ID `0`.
<2> The term `fox` appears once in the `text` field in this document.
<3> The inverse document frequency of `fox` in the `text` field in all
    documents in this index.
<4> The field-length normalization factor for this field.

Of course, queries usually consist of more than one term, so we need a
way of combining the weights of multiple terms.  For this, we turn to the
vector space model.


[[vector-space-model]]
==== Vector Space Model

The _vector space model_ provides a way of ((("Vector Space Model")))comparing a multiterm query
against a document. The output is a single score that represents how well the
document matches the query.  In order to do this, the model represents both the document
and the query as _vectors_.

A vector is really just a one-dimensional array containing numbers, for example:

    [1,2,5,22,3,8]

In the vector space((("Term Frequency/Inverse Document Frequency  (TF/IDF) similarity algorithm", "in Vector Space Model"))) model, each number in the vector is((("weight", "calculation of", "in Vector Space Model"))) the _weight_ of a term,
as calculated with <<tfidf,term frequency/inverse document frequency>>.

[TIP]
==================================================

While TF/IDF is the default way of calculating term weights for the vector
space model, it is not the only way.  Other models like Okapi-BM25 exist and
are available in Elasticsearch.  TF/IDF is the default because it is a
simple, efficient algorithm that produces high-quality search results and
has stood the test of time.

==================================================

Imagine that we have a query for ``happy hippopotamus.''  A common word like
`happy` will have a low weight, while an uncommon term like `hippopotamus`
will have a high weight. Let's assume that `happy` has a weight of 2 and
`hippopotamus` has a weight of 5.  We can plot this simple two-dimensional
vector&#x2014;`[2,5]`&#x2014;as a line on a graph starting at point (0,0) and
ending at point (2,5), as shown in <<img-vector-query>>.

[[img-vector-query]]
.A two-dimensional query vector for ``happy hippopotamus'' represented
image::images/elas_17in01.png["The query vector plotted on a graph"]

Now, imagine we have three documents:

1. I am _happy_ in summer.
2. After Christmas I'm a _hippopotamus_.
3. The _happy hippopotamus_ helped Harry.

We can create a similar vector for each document, consisting of the weight of
each query term&#x2014;`happy` and `hippopotamus`&#x2014;that appears in the
document, and plot these vectors on the same graph, as shown in <<img-vector-docs>>:

* Document 1: `(happy,____________)`&#x2014;`[2,0]`
* Document 2: `( ___ ,hippopotamus)`&#x2014;`[0,5]`
* Document 3: `(happy,hippopotamus)`&#x2014;`[2,5]`

[[img-vector-docs]]
.Query and document vectors for ``happy hippopotamus''
image::images/elas_17in02.png["The query and document vectors plotted on a graph"]

The nice thing about vectors is that they can be compared. By measuring the
angle between the query vector and the document vector, it is possible to
assign a relevance score to each document. The angle between document 1 and
the query is large, so it is of low relevance.  Document 2 is closer to the
query, meaning that it is reasonably relevant, and document 3 is a perfect
match.

[TIP]
==================================================

In practice, only two-dimensional vectors (queries with two terms) can  be
plotted easily on a graph. Fortunately, _linear algebra_&#x2014;the branch of
mathematics that deals with vectors--provides tools to compare the
angle between multidimensional vectors, which means that we can apply the
same principles explained above to queries that consist of many terms.

You can read more about how to compare two vectors by using http://en.wikipedia.org/wiki/Cosine_similarity[_cosine similarity_].

==================================================

Now that we have talked about the theoretical basis of scoring, we can move on
to see how scoring is implemented in Lucene.((("relevance scores", "theory behind", range="endofrange", startref="ix_relscore")))

