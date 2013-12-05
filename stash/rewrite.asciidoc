
For the last several sections, we've repeated talked about how these partial matching queries rewrite portions of the query.  But we've only vaguely discussed how these rewritten are scored internally.

Elasticsearch allows the user to configure the exact scoring mechanism for rewritten terms.  This is an **expert** setting...99% of users will never need to adjust the rewrite method.  But it is useful to see the options so that you understand what Elasticsearch is thinking when it generates scores.

When Elasticsearch rewrites terms, it places them in the Should clause of a Boolean.  Normal booleans perform scoring based on the term, its frequency in the dictionary, the frequency in the document and how many of the Should clauses match.

This score calculation is non-negligible, and furthermore, not really important to a rewritten query.  In many, many cases, you can happily skip the precise scoring and give each matching document a single, constant boost.  This is much faster and in most cases does not sacrifice precision at all.

The default rewrite method is called `constant_score_auto` and uses a constant scoring scheme to aid performance.

==== constant_score_auto

This rewrite method automatically chooses an appropriate rewrite method depending on the type of query you are using.  These defaults are optimized to work with each particular query, and generally, you'll never need to change it.

The `constant_score_auto` option chooses from two variants of a constant score.

**constant_score_boolean**
This rewrite builds a Should clause where each matching term is given a constant boost equal to the boost of the query.  Scores are then summed together.

**constant_score_filter**
This rewrite is similar in spirit to _boolean, except it constructs a private Filter and uses filter caching to boost performance.

Both these two methods have a hard limit of 1024 terms.  If your rewritten query generates more than 1024 terms, Elasticsearch will throw an error.

==== top_terms_boost_N

The only rewrite option that you *may* need to use is `top_terms_boost_N`.  If your rewritten query is constantly hitting the 1024 term limit, this rewrite can help.

It functions identically to constant_score_filter: it is filter based and matching documents are given a constant score.  The only difference is that `top_terms_boost_N` ranks the scoring terms and only saves the top N terms.  This allows you to avoid overflowing the 1024 maximum term limit.

N is configurable by simply changing the name of the rewrite method (e.g. `top_terms_boost_100`, `top_terms_boost_500`, etc)

==== scoring_boolean

This method is the naive, performance heavy rewrite method.  It saves precise scores for each term in the Boolean, and is therefore much more expensive to compute.

This rewrite is not recommended.  It also has a 1024 term limit.

==== top_terms_N

This method is the sibling to `top_terms_boost_N`: it performs precise Boolean scoring but only saves the top N results to avoid overflowing the term limit.

Like `scoring_boolean`, this rewrite method is heavy and not recommended.


=== Changing the rewrite method

Changing the rewrite method is as simple as specifying the `rewrite` option in the query.  Rewrite can be applied to any query that uses the rewriting process (query_string, prefix, wildcard, etc).

[source,js]
--------------------------------------------------
{
    "prefix" : {
        "my_field" : "qui",
        "rewrite" : "constant_score_auto"
    }
}
--------------------------------------------------

