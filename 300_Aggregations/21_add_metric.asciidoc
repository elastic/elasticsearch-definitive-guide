
=== Adding a Metric to the Mix

The previous example told us the number of documents in each bucket, which is
useful.  ((("aggregations", "basic example", "adding a metric")))But often, our applications require more-sophisticated metrics about
the documents.((("metrics", "adding to basic aggregation (example)"))) For example, what is the average price of cars in each bucket?

To get this information, we need to tell Elasticsearch which metrics to calculate,
and on which fields. ((("buckets", "nesting metrics in"))) This requires _nesting_ metrics inside the buckets.
Metrics will calculate mathematical statistics based on the values of documents
within a bucket.

Let's go ahead and add ((("average metric")))an `average` metric to our car example:

[source,js]
--------------------------------------------------
GET /cars/transactions/_search?search_type=count
{
   "aggs": {
      "colors": {
         "terms": {
            "field": "color"
         },
         "aggs": { <1>
            "avg_price": { <2>
               "avg": {
                  "field": "price" <3>
               }
            }
         }
      }
   }
}
--------------------------------------------------
// SENSE: 300_Aggregations/20_basic_example.json
<1> We add a new `aggs` level to hold the metric.
<2> We then give the metric a name: `avg_price`.
<3> And finally, we define it as an `avg` metric over the `price` field.

As you can see, we took the previous example and tacked on a new `aggs` level.
This new aggregation level allows us to nest the `avg` metric inside the
`terms` bucket.  Effectively, this means we will generate an average for each
color.

Just like the `colors` example, we need to name our metric (`avg_price`) so we
can retrieve the values later.  Finally, we specify the metric itself (`avg`)
and what field we want the average to be calculated on (`price`):

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
               "avg_price": { <1>
                  "value": 32500
               }
            },
            {
               "key": "blue",
               "doc_count": 2,
               "avg_price": {
                  "value": 20000
               }
            },
            {
               "key": "green",
               "doc_count": 2,
               "avg_price": {
                  "value": 21000
               }
            }
         ]
      }
   }
...
}
--------------------------------------------------
<1> New `avg_price` element in response

Although the response has changed minimally, the data we get out of it has grown
substantially.  Before, we knew there were four red cars.  Now we know that the
average price of red cars is $32,500.  This is something that you can plug directly
into reports or graphs.
