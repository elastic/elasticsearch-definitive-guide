
You'll often find yourself trying to perform exact, structured search on data
that is not "noisy" or "dirty".  For example, your data may have a mix of
capitalization and whitespace.  This usually needs to be removed even for
structured search environments.  It is unlikely that you will expect users to
search for "airplane " (note the trailing space).

There are a number of analyzers that you can apply to your data to help
normalize it, making exact matches work in a predictable manner.  Many of these
analysis chains start with the `keyword` token filter.

This token filter is very simple: it takes your input text and emits it as a
single token.  If you were to use `keyword` as the *only* token filter, it is
identical to setting the field to `not_analyzed`.  Case is not changed, errant
whitespace is not stripped, special characters are not removed.  It simply
outputs your text as a single token.

[[keyword-tokenizer]]
==== Cleaning up data

By itself, `keyword` is not very useful.  But you can combine it with a number of
other token filters to help normalize your data.  Two useful filters to include
with `keyword` are:

- `lowercase` - all characters will be lowercased
- `trim` - Removes any whitespace before and after the text in the token

This combination - `keyword, lowercase, trim` - is a good default token filter
chain for exact match scenarios that still need special characters and
*significant* spacing (such as the spaces between words in a phrase).

This combination is also very a very common way to prepare data for faceting and
sorting.  If you are faceting, you probably want "New York" and "new york" to be
aggregated  together.  Setting the field to `not_analyzed` will make the
aggregations case-sensitive, which may not be the behavior you want.

==== Truncating tokens

In some situations, you may have long fields but only care about the first portion.
For example, you have product serial numbers where the first 10 characters refer
to the product category, while the rest is just unique characters specific to that
particular product.

By combining `keyword` analyzer with the `truncate` filter, you can selectively
index just the portion you are interested in.  This allows you to maintain
searchability without bloating your index with unnecessary terms.  Ultimately,
this saves disk space and processing power (due to a smaller inverted index).

A related filter is the `length` filter.  Truncate is oblivious to connotation -
if the token is too long it gets chopped, even if that is in the middle of a word.

In contrast, the `length` filter is configured to remove tokens that are either
too small or too large.  The filter will inspect each token and either keep it
in the token stream, or remove the entire word.

Which you use is dependent on your data.  If you need to keep a field under a
particular size, use `truncate`.  If you instead care about keeping the terms
under (or over) a certain size, use `length`.

==== Selectively ignoring tokens

Due to the flexible nature of documents in Elasticsearch, it is easy to index
relatively anomalous data.  Perhaps the majority of your values are 20
characters...but sometimes you get a monster that is 10,000 characters long.

These anomalous fields can unescessarily bloat your index on disk.  They also
increase the size of the inverted index and slow down searches.

Depending on your use-case, you can choose to ignore fields that are over a
certain size.  When you create an analyzer, the `ignore_above` setting decides
the cut-off.

[source,js]
--------------------------------------------------
{
    "tweet" : {
        "properties" : {
            "message" : {
                "type" : "string",
                "analyzer" : "not_analyzed",
                "ignore_above" : 200
            }
        }
    }
}
--------------------------------------------------


If a particular field has a value larger than the configured `ignore_above`
setting, it is ignored and not indexed at all.  It is equivalent to setting
`index: no` for that field in that particular document.

This option is most frequently used in combination with `not_analyzed` fields.
Since `not_analyzed` fields require an exact match to find them, it is unlikely
that inordinately large fields will ever be found (since it is unlikely the
user will ever enter 10,000 characters exactly).

It often makes sense to pair `ignore_above` with `not_analyzed` so you can
avoid indexing fields that will never be found simply due to their size.

==== Pruning and limiting the token stream

Imagine you allow users to enter tags for a blog post.  It is entirely possible
that the user will enter the same token twice. If you are using this token for
exact matches (e.g. no scoring), that duplicate token is just a waste of space.

By applying a `unique` token filter after your tokenization step (whitespace, etc),
Elasticsearch will keep only the tokens that are unique.  All duplicate tokens
will be removed.

The `unique` token filter makes sense when the field is some type of enumeration.
With enumerations (such as color, or keywords), you only care about the presence
of a term, not how many times it occurred.  The `unique` token filter will reduce
wasted space.

Using the same blog example, what if your user adds 10,000 tags to a blog
article?  You may wish to limit the number tags that are indexed.  While you
could do this client-side, Elasticsearch can automatically perform this limiting
for you with the `limit` token filter.

If the number of tokens exceeds the configured limit, the additional tokens
will be removed from the token stream.  This is usually more flexible than
doing the limiting client-side, since you can control when tokens are limited
(e.g. after shingling, which tends to create a large number of tokens).

