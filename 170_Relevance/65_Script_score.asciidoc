[[script-score]]
=== Scoring with Scripts

Finally, if none of the `function_score`&#39;s built-in functions suffice, you can
implement the logic that you need with a script, using the `script_score`
function.((("function_score query", "using script_score function")))((("script_score function")))((("relevance", "controlling", "scoring with scripts")))

For an example, let's say that we want to factor our profit margin into the
relevance calculation.  In our business, the profit margin depends on three
factors:

* The `price` per night of the vacation home.
* The user's membership level--some levels get a percentage `discount`
  above a certain price per night `threshold`.
* The negotiated `margin` as a percentage of the price-per-night, after user
  discounts.

The algorithm that we will use to calculate the profit for each home is as
follows:

[source,groovy]
-------------------------
if (price < threshold) {
  profit = price * margin
} else {
  profit = price * (1 - discount) * margin;
}
-------------------------

We probably don't want to use the absolute profit as a score; it would
overwhelm the other factors like location, popularity and features. Instead,
we can express the profit as a percentage of our `target` profit.  A profit
margin above our target will have a positive score (greater than `1.0`), and a profit margin below our target will have a negative score (less than
`1.0`):

[source,groovy]
-------------------------
if (price < threshold) {
  profit = price * margin
} else {
  profit = price * (1 - discount) * margin
}
return profit / target
-------------------------

The default scripting language in Elasticsearch is
http://groovy.codehaus.org/[Groovy], which for the most part looks a lot like
JavaScript.((("Groovy", "script factoring profit margins into relevance calculations"))) The preceding algorithm as a Groovy script would look like this:

[source,groovy]
-------------------------
price  = doc['price'].value <1>
margin = doc['margin'].value <1>

if (price < threshold) { <2>
  return price * margin / target
}
return price * (1 - discount) * margin / target <2>
-------------------------
<1> The `price` and `margin` variables are extracted from the `price` and
    `margin` fields in the document.
<2> The `threshold`, `discount`, and `target` variables we will pass in as
    `params`.

Finally, we can add our `script_score` function to the list of other functions
that we are already using:

[source,json]
-------------------------
GET /_search
{
  "function_score": {
    "functions": [
      { ...location clause... }, <1>
      { ...price clause... }, <1>
      {
        "script_score": {
          "params": { <2>
            "threshold": 80,
            "discount": 0.1,
            "target": 10
          },
          "script": "price  = doc['price'].value; margin = doc['margin'].value; 
          if (price < threshold) { return price * margin / target };
          return price * (1 - discount) * margin / target;" <3>
        }
      }
    ]
  }
}
-------------------------
<1> The `location` and `price` clauses refer to the example explained in
    <<decay-functions>>.
<2> By passing in these variables as `params`, we can change their values
    every time we run this query without having to recompile the script.
<3> JSON cannot include embedded newline characters.  Newline characters in
    the script should  either be escaped as `\n` or replaced with semicolons.

This query would return the documents that best satisfy the user's
requirements for location and price, while still factoring in our need to make
a profit.

[TIP]
========================================

The `script_score` function provides enormous flexibility.((("scripts", "performance and")))  Within a script,
you have access to the fields of the document, to the current `_score`, and
even to the term frequencies, inverse document frequencies, and field length
norms (see http://bit.ly/1E3Rbbh[Text scoring in scripts]).

That said, scripts can have a performance impact.  If you do find that your
scripts are not quite fast enough, you have three options:

* Try to precalculate as much information as possible and include it in each
  document.
* Groovy is fast, but not quite as fast as Java.((("Java", "scripting in")))  You could reimplement your
  script as a native Java script. (See
  http://bit.ly/1ynBidJ[Native Java Scripts]).
* Use the `rescore` functionality((("rescoring"))) described in <<rescore-api>> to apply
  your script to only the best-scoring documents.

========================================

