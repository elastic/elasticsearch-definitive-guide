[[stopwords-relavance]]
=== Stopwords and Relevance

The last topic to cover before moving on from stopwords((("stopwords", "relevance and")))((("relevance", "stopwords and"))) is that of relevance.
Leaving stopwords in your index could make the relevance calculation
less accurate, especially if your documents are very long.

As we have already discussed in <<bm25-saturation>>, the((("BM25", "term frequency saturation"))) reason for this is
that <<tfidf,term-frequency/inverse document frequency>> doesn't impose an
upper limit on the impact of term frequency.((("Term Frequency/Inverse Document Frequency  (TF/IDF) similarity algorithm", "stopwords and")))  Very common words may have a low
weight because of inverse document frequency but, in long documents, the sheer
number of occurrences of stopwords in a single document may lead to their
weight being artificially boosted.

You may want to consider using the <<bm25,Okapi BM25>> similarity on long
fields that include stopwords instead of the default Lucene similarity.

