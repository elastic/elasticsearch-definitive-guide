[role="pagebreak-before"]
=== Improving Performance

Phrase and proximity queries are more ((("proximity matching", "improving performance")))((("phrase matching", "improving performance")))expensive than simple `match` queries.
Whereas a `match` query just has to look up terms in the inverted index, a
`match_phrase` query has to calculate and compare the positions of multiple
possibly repeated terms.

The http://people.apache.org/~mikemccand/lucenebench/[Lucene nightly
benchmarks] show that a simple `term` query is about 10 times as fast as a
phrase query, and about 20 times as fast as a proximity query (a phrase query
with `slop`). And of course, this cost is paid at search time instead of at index time.

[TIP]
==================================================

Usually the extra cost of phrase queries is not as scary as these numbers
suggest. Really, the difference in performance is a testimony to just how fast
a simple `term` query is.  Phrase queries on typical full-text data usually
complete within a few milliseconds, and are perfectly usable in practice, even
on a busy cluster.

In certain pathological cases, phrase queries can be costly, but this is
unusual.  An example of a pathological case is DNA sequencing, where there are
many many identical terms repeated in many positions. Using higher `slop`
values in this case results in a huge growth in the number of position
calculations.

==================================================

So what can we do to limit the performance cost of phrase and proximity
queries? One useful approach is to reduce the total number of documents that
need to be examined by the phrase query.

[[rescore-api]]
==== Rescoring Results

In <<proximity-relevance,the preceding section>>, we discussed using proximity
queries just for relevance purposes, not to include or exclude results from
the result set. ((("relevance scores", "rescoring results for top-N documents with proximity query"))) A query may match millions of results, but chances are that
our users are interested in only the first few pages of results.

A simple `match` query will already have ranked documents that contain all
search terms near the top of the list. Really, we just want to rerank the _top
results_ to give an extra relevance bump to those documents that also match the
phrase query.

The `search` API supports exactly this functionality via _rescoring_.((("rescoring"))) The
rescore phase allows you to apply a more expensive scoring algorithm--like a
`phrase` query--to just the top `K` results from each shard. These top
results are then resorted according to their new scores.

The request looks like this:

[source,js]
--------------------------------------------------
GET /my_index/my_type/_search
{
    "query": {
        "match": {  <1>
            "title": {
                "query":                "quick brown fox",
                "minimum_should_match": "30%"
            }
        }
    },
    "rescore": {
        "window_size": 50, <2>
        "query": {         <3>
            "rescore_query": {
                "match_phrase": {
                    "title": {
                        "query": "quick brown fox",
                        "slop":  50
                    }
                }
            }
        }
    }
}
--------------------------------------------------
// SENSE: 120_Proximity_Matching/30_Performance.json

<1> The `match` query decides which results will be included in the final
    result set and ranks results according to TF/IDF.((("window_size parameter")))
<2> The `window_size` is the number of top results to rescore, per shard.
<3> The only rescoring algorithm currently supported is another query, but
    there are plans to add more algorithms later.





