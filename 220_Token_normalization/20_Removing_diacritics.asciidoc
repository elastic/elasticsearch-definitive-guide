[[asciifolding-token-filter]]
=== You Have an Accent

English uses diacritics (like `´`, `^`, and `¨`) only for imported words--like `rôle`, ++déjà++, and `däis`&#x2014;but usually they are optional. ((("diacritics")))((("tokens", "normalizing", "diacritics"))) Other
languages require diacritics in order to be correct.  Of course, just because
words are spelled correctly in your index doesn't mean that the user will
search for the correct spelling.

It is often useful to strip diacritics from words, allowing `rôle` to match
`role`, and vice versa. With Western languages, this can be done with the
`asciifolding` character filter.((("asciifolding character filter")))  Actually, it does more than just strip
diacritics.  It tries to convert many Unicode characters into a simpler ASCII
representation:

* `ß` => `ss`
* `æ` => `ae`
* `ł` => `l`
* `ɰ` => `m`
* `⁇` => `??`
* `❷` => `2`
* `⁶` => `6`

Like the `lowercase` filter, the `asciifolding` filter doesn't require any
configuration but can be included directly in a `custom` analyzer:

[source,js]
--------------------------------------------------
PUT /my_index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "folding": {
          "tokenizer": "standard",
          "filter":  [ "lowercase", "asciifolding" ]
        }
      }
    }
  }
}

GET /my_index?analyzer=folding
My œsophagus caused a débâcle <1>
--------------------------------------------------
<1> Emits `my`, `oesophagus`, `caused`, `a`, `debacle`

==== Retaining Meaning

Of course, when you strip diacritical marks from a word, you lose meaning.
For instance, consider((("diacritics", "stripping, meaning loss from"))) these three ((("Spanish", "stripping diacritics, meaning loss from")))Spanish words:

`esta`::    
      Feminine form of the adjective _this_, as in _esta silla_ (this chair) or _esta_ (this one).

`ésta`::    
      An archaic form of `esta`.

`está`::    
      The third-person form of the verb _estar_ (to be), as in _está feliz_ (he is happy).

While we would like to conflate the first two forms, they differ in meaning
from the third form, which we would like to keep separate.  Similarly:

`sé`::      
      The first person form of the verb _saber_ (to know) as in _Yo sé_  (I know).

`se`::      
      The third-person reflexive pronoun used with many verbs, such as _se sabe_ (it is known).

Unfortunately, there is no easy way to separate words that should have
their diacritics removed from words that shouldn't.  And it is quite likely
that your users won't know either.

Instead, we index the text twice: once in the original form and once with
diacritics ((("indexing", "text with diacritics removed")))removed:

[source,js]
--------------------------------------------------
PUT /my_index/_mapping/my_type
{
  "properties": {
    "title": { <1>
      "type":           "string",
      "analyzer":       "standard",
      "fields": {
        "folded": { <2>
          "type":       "string",
          "analyzer":   "folding"
        }
      }
    }
  }
}
--------------------------------------------------
<1> The `title` field uses the `standard` analyzer and will contain
    the original word with diacritics in place.
<2> The `title.folded` field uses the `folding` analyzer, which strips
    the diacritical marks.((("folding analyzer")))

You can test the field mappings by using the `analyze` API on the sentence
_Esta está loca_ (This woman is crazy):

[source,js]
--------------------------------------------------
GET /my_index/_analyze?field=title <1>
Esta está loca

GET /my_index/_analyze?field=title.folded <2>
Esta está loca
--------------------------------------------------
<1> Emits `esta`, `está`, `loca`
<2> Emits `esta`, `esta`, `loca`

Let's index some documents to test it out:

[source,js]
--------------------------------------------------
PUT /my_index/my_type/1
{ "title": "Esta loca!" }

PUT /my_index/my_type/2
{ "title": "Está loca!" }
--------------------------------------------------

Now we can search across both fields, using the `multi_match` query in
<<most-fields,`most_fields` mode>> to combine the scores from each field:


[source,js]
--------------------------------------------------
GET /my_index/_search
{
  "query": {
    "multi_match": {
      "type":     "most_fields",
      "query":    "esta loca",
      "fields": [ "title", "title.folded" ]
    }
  }
}
--------------------------------------------------

Running this query through the `validate-query` API helps to explain how the
query is executed:

[source,js]
--------------------------------------------------
GET /my_index/_validate/query?explain
{
  "query": {
    "multi_match": {
      "type":     "most_fields",
      "query":    "está loca",
      "fields": [ "title", "title.folded" ]
    }
  }
}
--------------------------------------------------

The `multi-match` query searches for the original form of the word (`está`) in the `title` field,
and the form without diacritics `esta` in the `title.folded` field:

    (title:está        title:loca       )
    (title.folded:esta title.folded:loca)

It doesn't matter whether the user searches for `esta` or `está`; both
documents will match because the form without diacritics exists in the the
`title.folded` field.  However, only the original form exists in the `title`
field. This extra match will push the document containing the original form of
the word to the top of the results list.

We use the `title.folded` field to  _widen the net_ in order to match more
documents, and use the original `title` field to push the most relevant
document to the top. This same technique can be used wherever an analyzer is
used, to increase matches at the expense of meaning.

[TIP]
=================================================

The `asciifolding` filter does have an option called `preserve_original` that
allows you to index the((("asciifolding character filter", "preserve_original option"))) original token and the folded token in the same
position in the same field.  With this option enabled, you would end up with
something like this:

    Position 1     Position 2
    --------------------------
    (ésta,esta)    loca
    --------------------------

While this appears to be a nice way to save space, it does mean that you have
no way of saying, ``Give me an exact match on the original word.''  Mixing
tokens with and without diacritics can also end up interfering with term-frequency counts, resulting in less-reliable relevance calcuations.

As a rule, it is cleaner to index each field variant into a separate field,
as we have done in this section.

=================================================


