[[token-normalization]]
== Normalizing Tokens

Breaking text into tokens is ((("normalization", "of tokens")))((("tokens", "normalizing")))only half the job. To make those
tokens more easily searchable, they need to go through a _normalization_
process to remove insignificant differences between otherwise identical words,
such as uppercase versus lowercase.  Perhaps we also need to remove significant
differences, to make `esta`, `ésta`, and `está` all searchable as the same
word.  Would you search for `déjà vu`, or just for `deja vu`?

This is the job of the token filters, which((("token filters"))) receive a stream of tokens from
the tokenizer.  You can have multiple token filters, each doing its particular
job.  Each receives the new token stream as output by the token filter before
it.

