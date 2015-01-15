[[decay-functions]]
=== The Closer, The Better

Many variables could influence the user's choice of vacation
home.((("relevance", "controlling", "using decay functions")))  Maybe she would like to be close to the center of town, but perhaps
would be willing to settle for a place that is a bit farther from the
center if the price is low enough.  Perhaps the reverse is true: she would be
willing to pay more for the best location.

If we were to add a filter that excluded any vacation homes farther than 1
kilometer from the center, or any vacation homes that cost more than £100 a
night, we might exclude results that the user would consider to be a good
compromise.

The `function_score` query gives ((("function_score query", "decay functions")))((("decay functions")))us the ability to trade off one sliding scale
(like location) against another sliding scale (like price), with a group of
functions known as the _decay functions_.

The three decay functions--called `linear`, `exp`, and `gauss`&#x2014;operate on numeric fields, date fields, or lat/lon geo-points.((("linear function")))((("exp (exponential) function")))((("gauss (Gaussian) function")))  All three take
the same parameters:

`origin`::
    The _central point_, or the best possible value for the field.
    Documents that fall at the `origin` will get a full `_score` of `1.0`.

`scale`::
    The rate of decay--how quickly the `_score` should drop the further from
    the `origin` that a document lies (for example, every £10 or every 100 meters).

`decay`::
    The `_score` that a document at `scale` distance from the `origin` should
    receive. Defaults to `0.5`.

`offset`::
    Setting a nonzero `offset` expands the central point to cover a range
    of values instead of just the single point specified by the `origin`. All
    values in the range `-offset <= origin <= +offset` will receive the full
    `_score` of `1.0`.

The only difference between these three functions is the shape of the decay
curve. The difference is most easily illustrated with a graph (see <<img-decay-functions>>).

[[img-decay-functions]]
.Decay function curves
image::images/elas_1705.png["The curves of the decay functions"]

The curves shown in <<img-decay-functions>> all have their `origin`&#x2014;the
central point--set to `40`.  The `offset` is `5`, meaning that all values in
the range `40 - 5 <= value <= 40 + 5` are treated as though they were at the
`origin`&#x2014;they all get the full score of `1.0`.

Outside this range, the score starts to decay.  The rate of decay is
determined by the `scale` (which in this example is set to `5`), and the
`decay` (which is set to the default of `0.5`). The result is that all three
curves return a score of `0.5` at `origin +/- (offset + scale)`, or at points
`30` and `50`.

The difference between `linear`, `exp`, and `gauss` is the shape of the curve at other points in the range:

* The `linear` funtion is just a straight line. Once the line hits zero,
  all values outside the line will return a score of `0.0`.
* The `exp` (exponential) function decays rapidly, then slows down.
* The `gauss` (Gaussian) function is bell-shaped--it decays slowly, then
  rapidly, then slows down again.

Which curve you choose depends entirely on how quickly you want the `_score`
to decay, the further a value is from the `origin`.

To return to our example: our user would prefer to rent a vacation home close
to the center of London (`{ "lat": 51.50, "lon": 0.12}`) and to pay no more
than £100 a night, but our user considers price to be more important than
distance. ((("gauss (Gaussian) function", "in function_score query")))  We could write this query as follows:

[source,json]
----------------------------------
GET /_search
{
  "query": {
    "function_score": {
      "functions": [
        {
          "gauss": {
            "location": { <1>
              "origin": { "lat": 51.5, "lon": 0.12 },
              "offset": "2km",
              "scale":  "3km"
            }
          }
        },
        {
          "gauss": {
            "price": { <2>
              "origin": "50", <3>
              "offset": "50",
              "scale":  "20"
            }
          },
          "weight": 2 <4>
        }
      ]
    }
  }
}
----------------------------------
<1> The `location` field is mapped as a `geo_point`.
<2> The `price` field is numeric.
<3> See <<Understanding-the-price-Clause>> for the reason that `origin` is `50` instead of `100`.
<4> The `price` clause has twice the weight of the `location` clause.

The `location` clause is((("location clause, Gaussian function example"))) easy to understand:

* We have specified an `origin` that corresponds to the center of London.
* Any location within `2km` of the `origin` receives the full score of `1.0`.
* Locations `5km` (`offset + scale`) from the centre receive a score
of `0.5`.

[[Understanding-the-price-Clause]]
=== Understanding the price Clause

The `price` clause is a little trickier.((("price clause (Gaussian function example)")))  The user's preferred price is
anything up to £100, but this example sets the origin to £50.  Prices can't be
negative, but the lower they are, the better.  Really, any price between £0 and
£100 should be considered optimal.

If we were to set the `origin` to £100, then prices below £100 would receive a
lower score. Instead, we set both the `origin` and the `offset` to £50.  That
way, the score decays only for any prices above £100 (`origin + offset`).

[TIP]
==================================================

The `weight` parameter can be used to increase or decrease the contribution of
individual clauses. ((("weight parameter (in function_score query)"))) The `weight`, which defaults to `1.0`, is multiplied by
the score from each clause before the scores are combined with the specified
`score_mode`.

==================================================


