
==== Omitting Lucene Normalization

Each field that is indexed also includes a special value called `norms`,
which includes three components:

- Document Boost: a per-document boost provided at index-time
- Field Boost: a per-field boost also provided at index-time
- Length Norm: a normalization where shorter fields obtain a higher boost
relative to longer fields.  This prevents long fields from matching higher simply
because they are longer.

By default, `norms` are calculated for any analyzed field, and not calculated
for `not_analyzed` field.  But if you are using one of the normalization schemes
we just talked about (e.g. Keyword + lowercase), you may wish to disable `norms`
to save space because you don't care about score at all.

Disabling norms is as simple as setting `omit_norms: true` in your mapping.

Similarly, you may wish to change the default `index_options` value.  This
configuration controls the type of data that is stored about each field.
The options are:

- docs: Indexes only the doc ID
- freqs: Indexes doc IDs and term frequencies
- positions: Indexes doc IDs, term frequencies and token positions

Analyzed fields default to "positions", while `not_analyzed` default to "freqs".
Again, if you are using Keyword + lowercase to make a case-insensitive `not_analyzed`,
it may make sense to change `index_options` to "freqs".

You only have a single token, so the position information is redundant and
useless - it is just taking up space.