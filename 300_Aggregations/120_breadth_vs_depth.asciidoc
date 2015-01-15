
=== Preventing Combinatorial Explosions

The `terms` bucket dynamically builds buckets based on your data; it doesn't
know up front how many buckets will be generated. ((("combinatorial explosions, preventing")))((("aggregations", "preventing combinatorial explosions"))) While this is fine with a
single aggregation, think about what can happen when one aggregation contains
another aggregation, which contains another aggregation, and so forth. The combination of
unique values in each of these aggregations can lead to an explosion in the
number of buckets generated.

Imagine we have a modest dataset that represents movies.  Each document lists
the actors in that movie:

[source,js]
----
{
  "actors" : [
    "Fred Jones",
    "Mary Jane",
    "Elizabeth Worthing"
  ]
}
----

If we want to determine the top 10 actors and their top costars, that's trivial
with an aggregation:

[source,js]
----
{
  "aggs" : {
    "actors" : {
      "terms" : {
         "field" : "actors",
         "size" :  10
      },
      "aggs" : {
        "costars" : {
          "terms" : {
            "field" : "actors",
            "size" :  5
          }
        }
      }
    }
  }
}
----

This will return a list of the top 10 actors, and for each actor, a list of their
top five costars.  This seems like a very modest aggregation; only 50
values will be returned!

However, this seemingly ((("aggregations", "fielddata", "datastructure overview")))innocuous query can easily consume a vast amount of
memory. You can visualize a `terms` aggregation as building a tree in memory.
The `actors` aggregation will build the first level of the tree, with a bucket
for every actor.  Then, nested under each node in the first level, the
`costars` aggregation will build a second level, with a bucket for every costar, as seen in <<depth-first-1>>. That means that a single movie will generate n^2^ buckets!

[[depth-first-1]]
.Build full depth tree
image::images/300_120_depth_first_1.svg["Build full depth tree"]

To use some real numbers, imagine each movie has 10 actors on average. Each movie
will then generate 10^2^ == 100 buckets.  If you have 20,000 movies, that's
roughly 2,000,000 generated buckets.

Now, remember, our aggregation is simply asking for the top 10 actors and their
co-stars, totaling 50 values.  To get the final results, we have to generate
that tree of 2,000,000 buckets, sort it, and finally prune it such that only the
top 10 actors are left. This is illustrated in <<depth-first-2>> and <<depth-first-3>>.

[[depth-first-2]]
.Sort tree
image::images/300_120_depth_first_2.svg["Sort tree"]

[[depth-first-3]]
.Prune tree
image::images/300_120_depth_first_3.svg["Prune tree"]

At this point you should be quite distraught.  Twenty thousand documents is paltry,
and the aggregation is pretty tame.  What if you had 200 million documents, wanted
the top 100 actors and their top 20 costars, as well as the costars' costars?

You can appreciate how quickly combinatorial expansion can grow, making this
strategy untenable.  There is not enough memory in the world to support uncontrolled
combinatorial explosions.

==== Depth-First Versus Breadth-First

Elasticsearch allows you to change the _collection mode_ of an aggregation, for
exactly this situation. ((("collection mode"))) ((("aggregations", "preventing combinatorial explosions", "depth-first versus breadth-first")))The strategy we outlined previously--building the tree fully
and then pruning--is called _depth-first_ and it is the default. ((("depth-first collection strategy"))) Depth-first
works well for the majority of aggregations, but can fall apart in situations
like our actors and costars example.

For these special cases, you should use an alternative collection strategy called
_breadth-first_.  ((("beadth-first collection strategy")))This strategy works a little differently.  It executes the first
layer of aggregations, and _then_ performs a pruning phase before continuing, as illustrated in <<breadth-first-1>> through <<breadth-first-3>>.

In our example, the `actors` aggregation would be executed first.  At this
point, we have a single layer in the tree, but we already know who the top 10
actors are! There is no need to keep the other actors since they won't be in
the top 10 anyway. 

[[breadth-first-1]]
.Build first level
image::images/300_120_breadth_first_1.svg["Build first level"]

[[breadth-first-2]]
.Sort first level
image::images/300_120_breadth_first_2.svg["Sort first level"]

[[breadth-first-3]]
.Prune first level
image::images/300_120_breadth_first_3.svg["Prune first level"]

Since we already know the top ten actors, we can safely prune away the rest of the
long tail. After pruning, the next layer is populated based on _its_ execution mode,
and the process repeats until the aggregation is done, as illustrated in <<breadth-first-4>>. This prevents the
combinatorial explosion of buckets and drastically reduces memory requirements
for classes of queries that are amenable to breadth-first. 

[[breadth-first-4]]
.Populate full depth for remaining nodes
image::images/300_120_breadth_first_4.svg["Step 4: populate full depth for remaining nodes"]

To use breadth-first, simply ((("collect parameter, enabling breadth-first")))enable it via the `collect` parameter:

[source,js]
----
{
  "aggs" : {
    "actors" : {
      "terms" : {
         "field" :        "actors",
         "size" :         10,
         "collect_mode" : "breadth_first" <1>
      },
      "aggs" : {
        "costars" : {
          "terms" : {
            "field" : "actors",
            "size" :  5
          }
        }
      }
    }
  }
}
----
<1> Enable `breadth_first` on a per-aggregation basis.

Breadth-first should be used only when you expect more buckets to be generated
than documents landing in the buckets.  Breadth-first works by caching
document data at the bucket level, and then replaying those documents to child
aggregations after the pruning phase.

The memory requirement of a breadth-first aggregation is linear to the number
of documents in each bucket prior to pruning.  For many aggregations, the
number of documents in each bucket is very large.  Think of a histogram with
monthly intervals: you might have thousands or hundreds of thousands of
documents per bucket.  This makes breadth-first a bad choice, and is why
depth-first is the default.

But for the actor example--which generates a large number of
buckets, but each bucket has relatively few documents--breadth-first is much
more memory efficient, and allows you to build aggregations that would
otherwise fail.


