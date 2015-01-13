[[significant-terms]]
== Significant Terms

The `significant_terms` (SigTerms) aggregation((("significant_terms aggregation")))((("aggregations", "Significant Terms"))) is rather different from the rest of the
aggregations.  All the aggregations we have seen so far are essentially simple math
operations.  By combining the various building blocks, you can build sophisticated
aggregations and reports about your data.

`significant_terms` has a different agenda. To some, it may even look a bit like
machine learning. ((("terms", "uncommonly common, finding with SigTerms aggregation"))) The `significant_terms` aggregation finds _uncommonly common_ terms
in your data-set.

What do we mean by _uncommonly common_?  These are terms that are statistically
unusual -- data that appears more frequently than the background rate would
suggest.  These statistical anomalies are usually indicative of something
interesting in your data.

For example, imagine you are in charge of detecting and tracking down credit
card fraud.  Customers call and complain about unusual transactions appearing
on their credit card -- their account has been compromised.  These transactions
are just symptoms of a larger problem.  Somewhere in the recent past,
a merchant has either knowingly stolen the customers' credit card information,
or has unknowingly been compromised themselves.

Your job is to find the _common point of compromise_.  If you have 100 customers
complaining of unusual transactions, those customers likely share a single merchant--and it is this merchant that is likely the source of
blame.

Of course, it is a little more nuanced than just finding a merchant that all
customers share.  For example, many of the customers will have large merchants
like Amazon in their recent transaction history.  We can rule out Amazon, however,
since many uncompromised credit cards also have Amazon as a recent merchant.

This is an example of a _commonly common_ merchant.  Everyone, whether compromised
or not, shares the merchant.  This makes it of little interest to us.

On the opposite end of the spectrum, you have tiny merchants such as the corner
drug store.  These are _commonly uncommon_&#x2014;only one or two customers have
transactions from the merchant.  We can rule these out as well.  Since all of
the compromised cards did not interact with the merchant, we can be sure it was
not to blame for the security breach.

What we want are _uncommonly common_ merchants.  These are merchants that every
compromised card shares, but that are not well represented in the background
noise of uncompromised cards.  These merchants are statistical anomalies; they
appear more frequently than they should.  It is highly likely that these
uncommonly common merchants are to blame.

`significant_terms` aggregation does just this.  It analyzes your data and finds
terms that appear with a frequency that is statistically anomalous compared
to the background data.

What you _do_ with this statistical anomaly depends on the data.  With the credit
card data, you might be looking for fraud.  With ecommerce, you might be looking
for an unidentified demographic so you can market to them more efficiently.
If you are analyzing logs, you might find one server that throws a certain type of error
more often than it should.  The applications of `significant_terms` is nearly endless.


