[[slop]]
=== Mixing It Up

Requiring exact-phrase matches ((("proximity matching", "slop parameter")))may be too strict a constraint. Perhaps we _do_
want documents that contain ``quick brown fox'' to be considered a match for
the query ``quick fox,'' even though the positions aren't exactly equivalent.

We can introduce a degree ((("slop parameter")))of flexibility into phrase matching by using the
`slop` parameter:

[source,js]
--------------------------------------------------
GET /my_index/my_type/_search
{
    "query": {
        "match_phrase": {
            "title": {
            	"query": "quick fox",
            	"slop":  1
            }
        }
    }
}
--------------------------------------------------
// SENSE: 120_Proximity_Matching/10_Slop.json

The `slop` parameter tells the `match_phrase` query how((("match_phrase query", "slop parameter"))) far apart terms are
allowed to be while still considering the document a match. By _how far
apart_ we mean _how many times do you need to move a term in order to make
the query and document match_?

We'll start with a simple example. To make the query `quick fox` match
a document containing `quick brown fox` we need a `slop` of just `1`:


                Pos 1         Pos 2         Pos 3
    -----------------------------------------------
    Doc:        quick         brown         fox
    -----------------------------------------------
    Query:      quick         fox
    Slop 1:     quick                 ↳     fox

Although all words need to be present in phrase matching, even when using `slop`,
the words don't necessarily need to be in the same sequence in order to
match. With a high enough `slop` value, words can be arranged in any order.

To make the query `fox quick` match our document, we need a `slop` of `3`:

                Pos 1         Pos 2         Pos 3
    -----------------------------------------------
    Doc:        quick         brown         fox
    -----------------------------------------------
    Query:      fox           quick
    Slop 1:     fox|quick  ↵  <1>
    Slop 2:     quick      ↳  fox
    Slop 3:     quick                 ↳     fox

<1> Note that `fox` and `quick` occupy the same position in this step.
    Switching word order from `fox quick` to `quick fox` thus requires two
    steps, or a `slop` of `2`.

