[[function-score-query]]
=== function_score Query

The http://bit.ly/1sCKtHW[`function_score` query] is the
ultimate tool for taking control of the scoring process.((("function_score query")))((("relevance", "controlling", "function_score query")))  It allows you to
apply a function to each document that matches the main query in order to
alter or completely replace the original query `_score`.

In fact, you can apply different functions to _subsets_ of the main result set by
using filters, which gives you the best of both worlds: efficient scoring with
cacheable filters.

It supports several predefined functions out of the box:

`weight`::

    Apply a simple boost to each document without the boost being
    normalized: a `weight` of `2` results in `2 * _score`.

`field_value_factor`::

    Use the value of a field in the document to alter the `_score`,  such as
    factoring in a `popularity` count or number of `votes`.

`random_score`::

    Use consistently random scoring to sort results differently for every user,
    while maintaining the same sort order for a single user.

_Decay functions_&#x2014;`linear`, `exp`, `gauss`::

    Incorporate sliding-scale values like `publish_date`, `geo_location`, or
    `price` into the `_score` to prefer recently published documents, documents
    near a latitude/longitude (lat/lon) point, or documents near a specified price point.

`script_score`::

    Use a custom script to take complete control of the scoring logic. If your
    needs extend beyond those of the functions in this list, write a custom
    script to implement the logic that you need.

Without the `function_score` query, we would not be able to combine the score
from a full-text query with a factor like recency. We would have to sort
either by `_score` or by `date`; the effect of one would obliterate the
effect of the other. This query allows you to blend the two together: to still
sort by full-text relevance, but giving extra weight to recently published
documents, or popular documents, or products that are near the user's price
point. As you can imagine, a query that supports all of this can look fairly
complex.  We'll start with a simple use case and work our way up the
complexity ladder.
