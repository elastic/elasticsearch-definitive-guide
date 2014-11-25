
=== significant_terms Demo

Because the `significant_terms` aggregation((("significant_terms aggregation", "demonstration of")))((("aggregations", "significant_terms", "demonstration of"))) works by analyzing
statistics, you need to have a certain threshold of data for it to become effective.
That means we won't be able to index a small amount of example data for the demo.

Instead, we have a pre-prepared dataset of around 80,000 documents.  This is
saved as a snapshot (for more information about snapshots and restore, see
<<backing-up-your-cluster>>) in our public demo repository.  You can "restore"
this dataset into your cluster by using these commands:

[source,js]
----
PUT /_snapshot/sigterms <1>
{
    "type": "url",
    "settings": {
        "url": "http://download.elasticsearch.org/definitiveguide/sigterms_demo/"
    }
}

GET /_snapshot/sigterms/_all <2>

POST /_snapshot/sigterms/snapshot/_restore <3>

GET /mlmovies,mlratings/_recovery <4>
----
// SENSE: 300_Aggregations/75_sigterms.json
<1> Register a new read-only URL repository pointing at the demo snapshot
<2> (Optional) Inspect the repository to learn details about available snapshots
<3> Begin the Restore process.  This will download two indices into your cluster: `mlmovies`
and `mlratings`
<4> (Optional) Monitor the Restore process using the Recovery API


NOTE: The dataset is around 50 MB and may take some time to download.

In this demo, we are going to look at movie ratings by users of MovieLens.  At
MovieLens, users make movie recommendations so other users can find new
movies to watch.  For this demo, we are going to recommend movies by using `significant_terms`
based on an input movie.

Let's take a look at some sample data, to get a feel for what we are working with.
There are two indices in this dataset, `mlmovies` and `mlratings`.  Let's look
at `mlmovies` first:

[source,js]
----
GET mlmovies/_search <1>

{
   "took": 4,
   "timed_out": false,
   "_shards": {...},
   "hits": {
      "total": 10681,
      "max_score": 1,
      "hits": [
         {
            "_index": "mlmovies",
            "_type": "mlmovie",
            "_id": "2",
            "_score": 1,
            "_source": {
               "offset": 2,
               "bytes": 34,
               "title": "Jumanji (1995)"
            }
         },
         ....
----
// SENSE: 300_Aggregations/75_sigterms.json
<1> Execute a search without a query, so that we can see a random sampling of docs.

Each document in `mlmovies` represents a single movie.  The two important pieces
of data are the `_id` of the movie and the `title` of the movie.  You can ignore
`offset` and `bytes`; they are artifacts of the process used to extract this
data from the original CSV files. There are 10,681 movies in this dataset.

Now let's look at `mlratings`:


[source,js]
----
GET mlratings/_search

{
   "took": 3,
   "timed_out": false,
   "_shards": {...},
   "hits": {
      "total": 69796,
      "max_score": 1,
      "hits": [
         {
            "_index": "mlratings",
            "_type": "mlrating",
            "_id": "00IC-2jDQFiQkpD6vhbFYA",
            "_score": 1,
            "_source": {
               "offset": 1,
               "bytes": 108,
               "movie": [122,185,231,292,
                  316,329,355,356,362,364,370,377,420,
                  466,480,520,539,586,588,589,594,616
               ],
               "user": 1
            }
         },
         ...
----
// SENSE: 300_Aggregations/75_sigterms.json

Here we can see the recommendations of individual users.  Each document represents
a single user, denoted by the `user` ID field.  The `movie` field holds a list
of movies that this user watched and recommended.

==== Recommending Based on Popularity

The first strategy we could take is trying to recommend movies based on popularity.((("popularity", "movie recommendations based on")))
Given a particular movie, we find all users who recommended that movie.  Then
we aggregate all their recommendations and take the top five most popular.

We can express that easily with a `terms` aggregation ((("terms aggregation", "movie recommendations (example)")))and some filtering.  Let's
look at _Talladega Nights_, a comedy about NASCAR racing starring
Will Ferrell.  Ideally, our recommender should find other comedies in a similar
style (and more than likely also starring Will Ferrell).

First we need to find the _Talladega Nights_ ID:

[source,js]
----
GET mlmovies/_search
{
  "query": {
    "match": {
      "title": "Talladega Nights"
    }
  }
}

    ...
    "hits": [
     {
        "_index": "mlmovies",
        "_type": "mlmovie",
        "_id": "46970", <1>
        "_score": 3.658795,
        "_source": {
           "offset": 9575,
           "bytes": 74,
           "title": "Talladega Nights: The Ballad of Ricky Bobby (2006)"
        }
     },
    ...
----
// SENSE: 300_Aggregations/75_sigterms.json
<1> _Talladega Nights_ is ID `46970`.

Armed with the ID, we can now filter the ratings and ((("filtering", "in aggregations")))apply our `terms` aggregation
to find the most popular movies from people who also like _Talladega Nights_:

[source,js]
----
GET mlratings/_search?search_type=count <1>
{
  "query": {
    "filtered": {
      "filter": {
        "term": {
          "movie": 46970 <2>
        }
      }
    }
  },
  "aggs": {
    "most_popular": {
      "terms": {
        "field": "movie", <3>
        "size": 6
      }
    }
  }
}
----
// SENSE: 300_Aggregations/75_sigterms.json
<1> We execute our query on `mlratings` this time, and specify `search_type=count`
since we are interested only in the aggregation results.
<2> Apply a filter on the ID corresponding to _Talladega Nights_.
<3> Finally, find the most popular movies by using a `terms` bucket.

We perform the search on the `mlratings` index, and apply a filter for the ID of
_Talladega Nights_.  Since aggregations operate on query scope, this will
effectively filter the aggregation results to only the users who recommended
_Talladega Nights_. Finally, we execute ((("terms aggregation", "movie recommendations (example)")))a `terms` aggregation to bucket the most
popular movies.  We are requesting the top six results, since it is likely
that _Talladega Nights_ itself will be returned as a hit (and we don't want
to recommend the same movie).

The results come back like so:

[source,js]
----
{
...
   "aggregations": {
      "most_popular": {
         "buckets": [
            {
               "key": 46970,
               "key_as_string": "46970",
               "doc_count": 271
            },
            {
               "key": 2571,
               "key_as_string": "2571",
               "doc_count": 197
            },
            {
               "key": 318,
               "key_as_string": "318",
               "doc_count": 196
            },
            {
               "key": 296,
               "key_as_string": "296",
               "doc_count": 183
            },
            {
               "key": 2959,
               "key_as_string": "2959",
               "doc_count": 183
            },
            {
               "key": 260,
               "key_as_string": "260",
               "doc_count": 90
            }
         ]
      }
   }
...
----

We need to correlate these back to their original titles, which can be done
with a simple filtered query:

[source,js]
----
GET mlmovies/_search
{
  "query": {
    "filtered": {
      "filter": {
        "ids": {
          "values": [2571,318,296,2959,260]
        }
      }
    }
  }
}
----
// SENSE: 300_Aggregations/75_sigterms.json

And finally, we end up with the following list:

1. Matrix, The
2. Shawshank Redemption
3. Pulp Fiction
4. Fight Club
5. Star Wars Episode IV: A New Hope

OK--well that is certainly a good list!  I like all of those movies.  But that's
the problem: most _everyone_ likes that list.  Those movies are universally
well-liked, which means they are popular on everyone's recommendations.  The
list is basically a recommendation of popular movies, not recommendations related
to _Talladega Nights_.

This is easily verified by running the aggregation again, but without the filter
on _Talladega Nights_.  This will give a top-five most popular movie list:

[source,js]
----
GET mlratings/_search?search_type=count
{
  "aggs": {
    "most_popular": {
      "terms": {
        "field": "movie",
        "size": 5
      }
    }
  }
}
----
// SENSE: 300_Aggregations/75_sigterms.json

This returns a list that is very similar:

1. Shawshank Redemption
2. Silence of the Lambs, The
3. Pulp Fiction
4. Forrest Gump
5. Star Wars Episode IV: A New Hope

Clearly, just checking the most popular movies is not sufficient to build a good,
discriminating recommender.

==== Recommending Based on Statistics

Now that the scene is set, let's try using `significant_terms`.  `significant_terms` will analyze
the group of people who enjoy _Talladega Nights_ (the _foreground_ group) and
determine what movies are most popular. ((("statistics, movie recommendations based on (example)"))) It will then construct a list of
popular films for everyone (the _background_ group) and compare the two.

The statistical anomalies will be the movies that are _over-represented_ in the
foreground compared to the background.  Theoretically, this should be a list
of comedies, since people who enjoy Will Ferrell comedies will recommend them
at a higher rate than the background population of people.

Let's give it a shot:

[source,js]
----
GET mlratings/_search?search_type=count
{
  "query": {
    "filtered": {
      "filter": {
        "term": {
          "movie": 46970
        }
      }
    }
  },
  "aggs": {
    "most_sig": {
      "significant_terms": { <1>
        "field": "movie",
        "size": 6
      }
    }
  }
}
----
// SENSE: 300_Aggregations/75_sigterms.json
<1> The setup is nearly identical -- we just use `significant_terms` instead of
`terms`.

As you can see, the query is nearly the same.  We filter for users who
liked _Talladega Nights_; this forms the foreground group.  By default,
`significant_terms` will use the entire index as the background, so we don't need to do
anything special.

The results come back as a list of buckets similar to `terms`, but with some
extra ((("buckets", "returned by significant_terms aggregation")))metadata:

[source,js]
----
...
   "aggregations": {
      "most_sig": {
         "doc_count": 271, <1>
         "buckets": [
            {
               "key": 46970,
               "key_as_string": "46970",
               "doc_count": 271,
               "score": 256.549815498155,
               "bg_count": 271
            },
            {
               "key": 52245, <2>
               "key_as_string": "52245",
               "doc_count": 59, <3>
               "score": 17.66462367106966,
               "bg_count": 185 <4>
            },
            {
               "key": 8641,
               "key_as_string": "8641",
               "doc_count": 107,
               "score": 13.884387742677438,
               "bg_count": 762
            },
            {
               "key": 58156,
               "key_as_string": "58156",
               "doc_count": 17,
               "score": 9.746428133759462,
               "bg_count": 28
            },
            {
               "key": 52973,
               "key_as_string": "52973",
               "doc_count": 95,
               "score": 9.65770100311672,
               "bg_count": 857
            },
            {
               "key": 35836,
               "key_as_string": "35836",
               "doc_count": 128,
               "score": 9.199001116457955,
               "bg_count": 1610
            }
         ]
 ...
----
<1> The top-level `doc_count` shows the number of docs in the foreground group.
<2> Each bucket lists the key (for example, movie ID) being aggregated.
<3> A `doc_count` for that bucket.
<4> And a background count, which shows the rate at which this value appears in
the entire background.

You can see that the first bucket we get back is _Talladega Nights_.  It is
found in all 271 documents, which is not surprising.  Let's look at the next bucket:
key `52245`.

This ID corresponds to _Blades of Glory_, a comedy about male figure skating
that also stars Will Ferrell.  We can see that it was recommended 59 times by
the people who also liked _Talladega Nights_.  This means that 21% of the foreground
group recommended _Blades of Glory_ (`59 / 271 = 0.2177`).

In contrast, _Blades of Glory_ was recommended only 185 times in the entire dataset,
which equates to a mere 0.26% (`185 / 69796 = 0.00265`).  _Blades of Glory_ is therefore
a statistical anomaly: it is uncommonly common in the group of people who
like _Talladega Nights_.  We just found a good recommendation!

If we look at the entire list, they are all comedies that would fit as good
recommendations (many of which also star Will Ferrell):

1. Blades of Glory
2. Anchorman: The Legend of Ron Burgundy
3. Semi-Pro
4. Knocked Up
5. 40-Year-Old Virgin, The

This is just one example of the power of `significant_terms`. Once you start using
`significant_terms`, you find many situations where you don't want the most popular--you want the most uncommonly common.  This simple aggregation can uncover some
surprisingly sophisticated trends in your data.
