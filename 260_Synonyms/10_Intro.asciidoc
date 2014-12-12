[[synonyms]]
== Synonyms

While stemming helps to broaden the scope of search by simplifying inflected
words to their root form, synonyms((("synonyms"))) broaden the scope by relating concepts and
ideas. Perhaps no documents match a query for ``English queen,'' but documents
that contain ``British monarch'' would probably be considered a good match.

A user might search for ``the US'' and expect to find documents that contain
_United States_, _USA_, _U.S.A._, _America_, or _the States_.
However, they wouldn't expect to see results about `the states of matter` or
`state machines`.

This example provides a valuable lesson. It demonstrates how simple it is for
a human to distinguish between separate concepts, and how tricky it can be for
mere machines. The natural tendency is to try to provide synonyms for every
word in the language, to ensure that any document is findable with even the
most remotely related terms.

This is a mistake.  In the same way that we prefer light or minimal stemming
to aggressive stemming, synonyms should be used only where necessary. Users
understand why their results are limited to the words in their search query.
They are less understanding when their results seems almost random.

Synonyms can be used to conflate words that have pretty much the same meaning,
such as `jump`, `leap`, and `hop`, or `pamphlet`, `leaflet`, and `brochure`.
Alternatively, they can be used to make a word more generic.  For instance,
`bird` could be used as a more general synonym for `owl` or `pigeon`, and `adult`
could be used for `man` or `woman`.

Synonyms appear to be a simple concept but they are quite tricky to get right.
In this chapter, we explain the mechanics of using synonyms and discuss
the limitations and gotchas.

[TIP]
====
Synonyms are used to broaden the scope of what is considered a
matching document.  Just as with <<stemming,stemming>> or
<<partial-matching,partial matching>>, synonym fields should not be used
alone but should be combined with a query on a main field that contains
the original text in unadulterated form.  See <<most-fields>> for an
explanation of how to maintain relevance when using synonyms.
====


