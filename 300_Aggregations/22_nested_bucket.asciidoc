
=== Buckets Inside Buckets

The true power of aggregations becomes apparent once you start playing with
different nesting schemes.((("aggregations", "basic example", "buckets nested in other buckets")))((("buckets", "nested in other buckets")))  In the previous examples, we saw how you could nest
a metric inside a bucket, which is already quite powerful.

But the real exciting analytics come from nesting buckets inside _other buckets_.
This time, we want to find out the distribution of car manufacturers for each
color:


[source,js]
--------------------------------------------------
GET /cars/transactions/_search?search_type=count
{
   "aggs": {
      "colors": {
         "terms": {
            "field": "color"
         },
         "aggs": {
            "avg_price": { <1>
               "avg": {
                  "field": "price"
               }
            },
            "make": { <2>
                "terms": {
                    "field": "make" <3>
                }
            }
         }
      }
   }
}
--------------------------------------------------
// SENSE: 300_Aggregations/20_basic_example.json
<1> Notice that we can leave the previous `avg_price` metric in place.
<2> Another aggregation named `make` is added to the `color` bucket.
<3> This aggregation is a `terms` bucket and will generate unique buckets for
each car make.

A few interesting things happened here.((("metrics", "independent, on levels of an aggregation")))  First, you'll notice that the previous
`avg_price` metric is left entirely intact.  Each _level_ of an aggregation can
have many metrics or buckets.  The `avg_price` metric tells us the average price
for each car color.  This is independent of other buckets and metrics that
are also being built.

This is important for your application, since there are often many related,
but entirely distinct, metrics that you need to collect.  Aggregations allow
you to collect all of them in a single pass over the data.

The other important thing to note is that the aggregation we added, `make`, is
a `terms` bucket (nested inside the `colors` `terms` bucket).  This means we will((("terms bucket", "nested in another terms bucket")))
generate a (`color`, `make`) tuple for every unique combination in your dataset.

Let's take a look at the response (truncated for brevity, since it is now
growing quite long):


[source,js]
--------------------------------------------------
{
...
   "aggregations": {
      "colors": {
         "buckets": [
            {
               "key": "red",
               "doc_count": 4,
               "make": { <1>
                  "buckets": [
                     {
                        "key": "honda", <2>
                        "doc_count": 3
                     },
                     {
                        "key": "bmw",
                        "doc_count": 1
                     }
                  ]
               },
               "avg_price": {
                  "value": 32500 <3>
               }
            },

...
}
--------------------------------------------------
<1> Our new aggregation is nested under each color bucket, as expected.
<2> We now see a breakdown of car makes for each color.
<3> Finally, you can see that our previous `avg_price` metric is still intact.

The response tells us the following:

- There are four red cars.
- The average price of a red car is $32,500.
- Three of the red cars are made by Honda, and one is a BMW.
