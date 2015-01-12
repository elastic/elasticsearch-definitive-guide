[[one-lang-docs]]
=== One Language per Document

A single predominant language per document ((("languages", "one language per document")))((("indices", "documents in different languages")))requires a relatively simple setup.
Documents from different languages can be stored in separate indices&#x2014;`blogs-en`,
`blogs-fr`, and so forth&#x2014;that use the same type and the same fields for each index,
just with different analyzers:

[source,js]
--------------------------------------------------
PUT /blogs-en
{
  "mappings": {
    "post": {
      "properties": {
        "title": {
          "type": "string", <1>
          "fields": {
            "stemmed": {
              "type":     "string",
              "analyzer": "english" <2>
            }
}}}}}}

PUT /blogs-fr
{
  "mappings": {
    "post": {
      "properties": {
        "title": {
          "type": "string", <1>
          "fields": {
            "stemmed": {
              "type":     "string",
              "analyzer": "french" <2>
            }
}}}}}}
--------------------------------------------------
<1> Both `blogs-en` and `blogs-fr` have a type called `post` that contains
    the field `title`.
<2> The `title.stemmed` subfield uses a language-specific analyzer.


This approach is clean and flexible.  New languages are easy to add--just
create a new index--and because each language is completely separate, we
don't suffer from the term-frequency and stemming problems described in
<<language-pitfalls>>.

The documents of a single language can be queried independently, or queries
can target multiple languages by querying multiple indices.  We can even
specify a preference((("indices_boost parameter", "specifying preference for a specific language"))) for particular languages with the `indices_boost` parameter:

[source,js]
--------------------------------------------------
GET /blogs-*/post/_search <1>
{
    "query": {
        "multi_match": {
            "query":   "deja vu",
            "fields":  [ "title", "title.stemmed" ] <2>
            "type":    "most_fields"
        }
    },
    "indices_boost": { <3>
        "blogs-en": 3,
        "blogs-fr": 2
    }
}
--------------------------------------------------
<1> This search is performed on any index beginning with `blogs-`.
<2> The `title.stemmed` fields are queried using the analyzer
    specified in each index.
<3> Perhaps the user's `accept-language` headers showed a preference for
    English, and then French, so we boost results from each index accordingly.
    Any other languages will have a neutral boost of `1`.

==== Foreign Words

Of course, these documents may contain words or sentences in other languages,
and these words are unlikely to be stemmed correctly.  With
predominant-language documents, this is not usually a major problem.  The user will
often search for the exact words--for instance, of a quotation from another
language--rather than for inflections of a word. Recall can be improved
by using techniques explained in <<token-normalization>>.

Perhaps some words like place names should be queryable in the predominant
language and in the original language, such as _Munich_ and _München_.  These
words are effectively synonyms, which we discuss in <<synonyms>>.

.Don't Use Types for Languages
*************************************************

You may be tempted to use a separate type for each language,((("types", "not using for languages")))((("languages", "not using types for"))) instead of a
separate index. For best results, you should avoid using types for this
purpose.  As explained in <<mapping>>, fields from different types but with
the same field name are indexed into the _same inverted index_.  This means
that the term frequencies from each type (and thus each language) are mixed
together.

To ensure that the term frequencies of one language don't pollute those of
another, either use a separate index for each language, or a separate field,
as explained in the next section.

*************************************************
