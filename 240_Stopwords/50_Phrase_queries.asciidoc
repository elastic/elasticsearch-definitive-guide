[[stopwords-phrases]]
=== Stopwords and Phrase Queries

About 5% of all queries are ((("stopwords", "phrase queries and")))((("phrase matching", "stopwords and")))phrase queries (see <<phrase-matching>>), but they
often account for the majority of slow queries. Phrase queries can perform
poorly, especially if the phrase includes very common words; a phrase like
``To be, or not to be'' could be considered pathological. The reason for this
has to do with the amount of data that is necessary to support proximity
matching.

In <<pros-cons-stopwords>>, we said that removing stopwords saves only a small
amount of space in the inverted index.((("indices", "typical, data contained in")))  That was only partially true.  A
typical index may contain, among other data, some or all of the following:

Terms dictionary::

    A sorted list of all terms that appear in the documents in the index,
    and a count of the number of documents that contain each term.

Postings list::

    A list of which documents contain each term.

Term frequency::

    How often each term appears in each document.

Positions::

    The position of each term within each document, for phrase and proximity
    queries.

Offsets::

    The start and end character offsets of each term in each document, for
    snippet highlighting. Disabled by default.

Norms::

    A factor used to normalize fields of different lengths, to give shorter
    fields more weight.

Removing stopwords from the index may save a small amount of space in the
_terms dictionary_ and the _postings list_, but _positions_ and _offsets_ are
another matter. Positions and offsets data can easily double, triple, or
quadruple index size.

==== Positions Data

Positions are enabled on `analyzed` string fields by default,((("stopwords", "phrase queries and", "positions data")))((("phrase matching", "stopwords and", "positions data"))) so that phrase
queries will work out of the box. The more often that a term appears, the more
space is needed to store its position data. Very common words, by
definition, appear very commonly, and their positions data can run to megabytes
or gigabytes on large collections.

Running a phrase query on a high-frequency word like `the` might result in
gigabytes of data being read from disk. That data will be stored in the kernel
filesystem cache to speed up later access, which seems like a good thing, but
it might cause other data to be evicted from the cache, which will slow
subsequent queries.

This is clearly a problem that needs solving.

[[index-options]]
==== Index Options

The first question you should ((("stopwords", "phrase queries and", "index options")))((("phrase matching", "stopwords and", "index options")))ask yourself is: _Do you need phrase or
proximity queries?_

Often, the answer is no.  For many use cases, such as logging, you need to
know _whether_ a term appears in a document -- information that is provided
by the postings list--but not _where_ it appears. Or perhaps you need to use
phrase queries on one or two fields, but you can disable positions data on all
of the other analyzed `string` fields.

The `index_options` parameter ((("index_options parameter")))allows you to control what information is stored
in the index for each field.((("fields", "index options")))  Valid values are as follows:

`docs`::

    Only store which documents contain which terms. This is the default for
    `not_analyzed` string fields.

`freqs`::

    Store `docs` information, plus how often each term appears in each
    document. Term frequencies are needed for complete <<relevance-intro,TF/IDF>>
    relevance calculations, but they are not required if you just need to know
    whether a document contains a particular term.

`positions`::

    Store `docs` and `freqs`, plus the position of each term in each document.
    This is the default for `analyzed` string fields, but can be disabled if
    phrase/proximity matching is not needed.

`offsets`::

    Store `docs`, `freqs`, `positions`, and the start and end character offsets
    of each term in the original string.  This information is used by the
    http://bit.ly/1u9PJ16[`postings` highlighter]
    but is disabled by default.

You can set `index_options` on fields added at index creation time, or when
adding new fields by using((("put-mapping API"))) the `put-mapping` API. This setting can't be changed
on existing fields:

[source,json]
---------------------------------
PUT /my_index
{
  "mappings": {
    "my_type": {
      "properties": {
        "title": { <1>
          "type":          "string"
       },
        "content": { <2>
          "type":          "string",
          "index_options": "freqs"
      }
    }
  }
}
---------------------------------
<1> The `title` field uses the default setting of `positions`, so
    it is suitable for phrase/proximity queries.
<2> The `content` field has positions disabled and so cannot be used
    for phrase/proximity queries.

==== Stopwords

Removing stopwords is one way of reducing the size of the positions data quite
dramatically.((("stopwords", "phrase queries and", "removing stopwords")))   An index with stopwords removed can still be used for phrase
queries because the original positions of the remaining terms are maintained,
as we saw in <<maintaining-positions>>. But of course, excluding terms from
the index reduces searchability. We wouldn't be able to differentiate between
the two phrases _Man in the moon_ and _Man on the moon_.

Fortunately, there is a way to have our cake and eat it: the
<<common-grams,`common_grams` token filter>>.






