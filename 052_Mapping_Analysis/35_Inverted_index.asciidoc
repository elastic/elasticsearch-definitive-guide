[[inverted-index]]
=== Inverted index

Elasticsearch uses a structure called an _inverted index_ which is designed
to allow very fast full text searches. An inverted index consists of a list
of all the unique words that appear in any document, and for each word, a list
of the documents in which it appears.

For example, let's say we have two documents, each with a `content` field
containing:

1. ``The quick brown fox jumped over the lazy dog''
2. ``Quick brown foxes leap over lazy dogs in summer''

To create an inverted index, we first split the `content` field of each
document into separate words (which we call _terms_ or _tokens_), create a
sorted list of all the unique terms, then list in which document each term
appears. The result looks something like this:

    Term      Doc_1  Doc_2
    -------------------------
    Quick   |       |  X
    The     |   X   |
    brown   |   X   |  X
    dog     |   X   |
    dogs    |       |  X
    fox     |   X   |
    foxes   |       |  X
    in      |       |  X
    jumped  |   X   |
    lazy    |   X   |  X
    leap    |       |  X
    over    |   X   |  X
    quick   |   X   |
    summer  |       |  X
    the     |   X   |
    ------------------------

Now, if we want to search for `"quick brown"` we just need to find the
documents in which each term appears:


    Term      Doc_1  Doc_2
    -------------------------
    brown   |   X   |  X
    quick   |   X   |
    ------------------------
    Total   |   2   |  1

Both documents match, but the first document has more matches than the second.
If we apply a naive _similarity algorithm_ which just counts the number of
matching terms, then we can say that the first document is a better match --
is _more relevant_ to our query -- than the second document.

But there are a few problems with our current inverted index:

1. `"Quick"` and `"quick"` appear as separate terms, while the user probably
   thinks of them as the same word.

2. `"fox"` and `"foxes"` are pretty similar, as are `"dog"` and `"dogs"`
   -- they share the same root word.

3. `"jumped"` and `"leap"`, while not from the same root word, are similar
   in meaning -- they are synonyms.

With the above index, a search for `"+Quick +fox"` wouldn't match any
documents. (Remember, a preceding `+` means that the word must be present).
Both the term `"Quick"` and the term `"fox"` have to be in the same document
in order to satisfy the query, but the first doc contains `"quick fox"` and
the second doc contains `"Quick foxes"`.

Our user could reasonably expect both documents to match the query. We can do
better.

If we normalize the terms into a standard format, then we can find documents
that contain terms that are not exactly the same as the user requested, but
are similar enough to still be relevant. For instance:

1. `"Quick"` can be lowercased to become `"quick"`.

2. `"foxes"` can be _stemmed_ -- reduced to its root form -- to
   become `"fox"`. Similarly `"dogs"` could be stemmed to `"dog"`.

3. `"jumped"` and `"leap"` are synonyms and can be indexed as just the
   single term `"jump"`.

Now the index looks like this:

    Term      Doc_1  Doc_2
    -------------------------
    brown   |   X   |  X
    dog     |   X   |  X
    fox     |   X   |  X
    in      |       |  X
    jump    |   X   |  X
    lazy    |   X   |  X
    over    |   X   |  X
    quick   |   X   |  X
    summer  |       |  X
    the     |   X   |  X
    ------------------------

But we're not there yet. Our search for `"+Quick +fox"` would *still* fail,
because we no longer have the exact term `"Quick"` in our index. However, if
we apply the same normalization rules that we used on the `content` field to
our query string, it would become a query for `"+quick +fox"`, which would
match both documents!

IMPORTANT: This is very important. You can only find terms that actually exist in your
index, so: *both the indexed text and the query string must be normalized
into the same form*.

This process of tokenization and normalization is called _analysis_, which we
discuss in the next section.
