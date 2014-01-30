==== Term's Execution Mode

The `terms` filter can be used for different purposes.  You could be filtering
a list of tags which changes every time the query is executed.  Or we could
be filtering an enumeration which stays constant for every query.

In the first circumstance, it is more efficient to cache the individual tags
independently of each other and then combine their bitsets to calculate
the final results.  In the second circumstance, it is more efficient
to cache all the enumerations together as a single bitset, since they always
appear as a group.

We can control this behavior with an option called `execution_mode`.
By default the execution mode is `plain`, which caches all the individual terms
together.

As the `terms` filter is evaluating each individual term, it maintains a single
bitset which is modified.  Imagine we have four documents, and are looking for
the terms `abc` and `xyz`:

1. The term `abc` is found in the first document.  The bitset is now [1,0,0,0]
2. The term `xyz` is found in the third document.  The bitset is now [1,0,1,0]

When the filter is done executing, you are left with a single bitset that
represents the union of _all_ the terms.

The other option is called `bool`, and it maintains a unique bitset for each
individual term.  Instead of modifying a single bitset, each term gets its own
bitset.  These bitsets are then cached individually in memory.  Using the same
example as above:

1. The term `abc` is found in the first document.  The bitsets are now
abc:[1,0,0,0] xyz:[0,0,0,0]
2. The term `xyz` is found in the third document.  The bitsets are now
abc:[1,0,0,0] xyz:[0,0,1,0]

These two bitsets are cached individually in memory, and the result of the filter
is the bitwise AND of both bitsets (equaling `[1,0,1,0]`).

So which do you pick?  The default execution mode (`plain`) works very well
in the majority of cases.  If you are unsure, just stick with the default.
The reason to choose `bool` over `plain` is based on how often terms clump
together in your filters.

If the same set of terms always appear together in your `terms` filter, caching
the "total" set via `plain` will be the most efficient.  If, instead, terms are
rarely arranged in the same combination, use `bool`.  Whe the terms are constantly
changing,  the "total" set of terms will rarely be used again (much like we
discussed with the range filter on time).  It makes more sense to cache the
bitsets independently to avoid cache churn.


