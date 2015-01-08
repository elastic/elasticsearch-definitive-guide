

=== One Final Modification

Just to drive the point home, let's make one final modification to our example
before moving on to new topics.((("aggregations", "basic example", "adding extra metrics")))((("metrics", "adding more to aggregation (example)")))  Let's add two metrics to calculate the min and
max price for each make:


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
            "avg_price": { "avg": { "field": "price" }
            },
            "make" : {
                "terms" : {
                    "field" : "make"
                },
                "aggs" : { <1>
                    "min_price" : { "min": { "field": "price"} }, <2>
                    "max_price" : { "max": { "field": "price"} } <3>
                }
            }
         }
      }
   }
}
--------------------------------------------------
// SENSE: 300_Aggregations/20_basic_example.json

<1> We need to add another `aggs` level for nesting.
<2> Then we include a `min` metric.
<3> And a `max` metric.

Which gives ((("min and max metrics (aggregation example)")))us the following output (again, truncated):

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
               "make": {
                  "buckets": [
                     {
                        "key": "honda",
                        "doc_count": 3,
                        "min_price": {
                           "value": 10000 <1>
                        },
                        "max_price": {
                           "value": 20000 <1>
                        }
                     },
                     {
                        "key": "bmw",
                        "doc_count": 1,
                        "min_price": {
                           "value": 80000
                        },
                        "max_price": {
                           "value": 80000
                        }
                     }
                  ]
               },
               "avg_price": {
                  "value": 32500
               }
            },
...
--------------------------------------------------
<1> The `min` and `max` metrics that we added now appear under each `make`

With those two buckets, we've expanded the information derived from this query
to include the following:

- There are four red cars.
- The average price of a red car is $32,500.
- Three of the red cars are made by Honda, and one is a BMW.
- The cheapest red Honda is $10,000.
- The most expensive red Honda is $20,000.
