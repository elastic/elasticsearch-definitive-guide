=== Single Query String

The `bool` query is the mainstay of multiclause queries.((("multifield search", "single query string"))) It works well
for many cases, especially when you are able to map different query strings to
individual fields.

The problem is that, these days, users expect to be able to type all of their
search terms into a single field, and expect that the application will figure out how
to give them the right results.  It is ironic that the multifield search form
is known as _Advanced Search_&#x2014;it may appear advanced to the user, but it is
much simpler to implement.

There is no simple _one-size-fits-all_ approach to multiword, multifield
queries.  To get the best results, you have to _know your data_ and know how
to use the appropriate tools.

[[know-your-data]]
==== Know Your Data

When your only user input is a single query string, you will encounter three scenarios frequently:

Best fields::

When searching for words that represent a concept, such as ``brown fox,'' the
words mean more together than they do individually. Fields like the `title`
and `body`, while related, can be considered to be in competition with each
other. Documents should have as many words as possible in _the same field_,
and the score should come from the _best-matching field_.

Most fields::
+
--
A common technique for fine-tuning relevance is to index the same data into
multiple fields, each with its own analysis chain.

The main field may contain words in their stemmed form, synonyms, and words
stripped of their _diacritics_, or accents. It is used to match as many
documents as possible.

The same text could then be indexed in other fields to provide more-precise
matching.  One field may contain the unstemmed version, another the original
word with accents, and a third might use _shingles_ to provide information
about <<proximity-matching,word proximity>>.

These other fields act as _signals_ to increase the relevance score of each
matching document. The _more fields that match_, the better.
--

Cross fields::
+
--
For some entities, the identifying information is spread across multiple
fields, each of which contains just a part of the whole:

* Person: `first_name` and `last_name`
* Book: `title`, `author`, and `description`
* Address:  `street`, `city`, `country`, and `postcode`

In this case, we want to find as many words as possible in _any_ of the listed
fields. We need to search across multiple fields as if they were one big
field.
--

All of these are multiword, multifield queries, but each requires a
different strategy. We will examine each strategy in turn in the rest of this
chapter.

