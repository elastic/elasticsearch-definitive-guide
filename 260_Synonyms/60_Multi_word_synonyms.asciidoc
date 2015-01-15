[[multi-word-synonyms]]
=== Multiword Synonyms and Phrase Queries

So far, synonyms appear to be quite straightforward. Unfortunately, this is
where things start to go wrong.((("synonyms", "multiword, and phrase queries")))((("phrase matching", "multiword synonyms and"))) For <<phrase-matching,phrase queries>> to
function correctly, Elasticsearch needs to know the position that each term
occupies in the original text. Multiword synonyms can play havoc with term
positions, especially when the injected synonyms are of differing lengths.

To demonstrate, we'll create a synonym token filter that uses this rule:

    "usa,united states,u s a,united states of america"

[source,json]
-----------------------------------
PUT /my_index
{
  "settings": {
    "analysis": {
      "filter": {
        "my_synonym_filter": {
          "type": "synonym",
          "synonyms": [
            "usa,united states,u s a,united states of america"
          ]
        }
      },
      "analyzer": {
        "my_synonyms": {
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "my_synonym_filter"
          ]
        }
      }
    }
  }
}

GET /my_index/_analyze?analyzer=my_synonyms&text=
The United States is wealthy
-----------------------------------

The tokens emitted by the `analyze` request look like this:

[source,text]
-----------------------------------
Pos 1:  (the)
Pos 2:  (usa,united,u,united)
Pos 3:  (states,s,states)
Pos 4:  (is,a,of)
Pos 5:  (wealthy,america)
-----------------------------------

If we were to index a document analyzed with synonyms as above, and then run a
phrase query without synonyms, we'd have some surprising results.  These
phrases would not match:

* The usa is wealthy
* The united states of america is wealthy
* The U.S.A. is wealthy

However, these phrases would:

* United states is wealthy
* Usa states of wealthy
* The U.S. of wealthy
* U.S. is america

If we were to use synonyms at query time instead, we would see even more-bizarre matches. Look at the output of this `validate-query` request:

[source,json]
-----------------------------------
GET /my_index/_validate/query?explain
{
  "query": {
    "match_phrase": {
      "text": {
        "query": "usa is wealthy",
        "analyzer": "my_synonyms"
      }
    }
  }
}
-----------------------------------

The explanation is as follows:

    "(usa united u united) (is states s states) (wealthy a of) america"

This would match documents containg `u is of america` but wouldn't match any
document that didn't contain the term `america`.

[TIP]
==================================================

Multiword synonyms ((("highlighting searches", "multiword synonyms and")))affect highlighting in a similar way.  A query for `USA`
could end up returning a highlighted snippet such as: ``The _United States
is wealthy_''.

==================================================

==== Use Simple Contraction for Phrase Queries

The way to avoid this mess is to use <<synonyms-contraction,simple contraction>>
to inject a single((("synonyms", "multiword, and phrase queries", "using simple contraction")))((("phrase matching", "multiword synonyms and", "using simple contraction")))((("simple contraction (synonyms)", "using for phrase queries"))) term that represents all synonyms, and to use the same
synonym token filter at query time:

[source,json]
-----------------------------------
PUT /my_index
{
  "settings": {
    "analysis": {
      "filter": {
        "my_synonym_filter": {
          "type": "synonym",
          "synonyms": [
            "united states,u s a,united states of america=>usa"
          ]
        }
      },
      "analyzer": {
        "my_synonyms": {
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "my_synonym_filter"
          ]
        }
      }
    }
  }
}

GET /my_index/_analyze?analyzer=my_synonyms
The United States is wealthy
-----------------------------------

The result of the preceding `analyze` request looks much more sane:

[source,text]
-----------------------------------
Pos 1:  (the)
Pos 2:  (usa)
Pos 3:  (is)
Pos 5:  (wealthy)
-----------------------------------

And repeating the `validate-query` request that we made previously yields a simple,
sane explanation:

    "usa is wealthy"

The downside of this approach is that, by reducing `united states of america`
down to the single term `usa`, you can't use the same field to find just the
word `united` or `states`. You would need to use a separate field with a
different analysis chain for that purpose.

==== Synonyms and the query_string Query

We have tried to avoid discussing the `query_string` query ((("query strings", "synonyms and")))((("synonyms", "multiword, and query string queries")))because we don't
recommend using it.  In <<query-string-query, "More-Complicated Queries">>, we said that, because the
`query_string` query supports a terse mini _search-syntax_, it could
frequently lead to surprising results or even syntax errors.

One of the gotchas of this query involves multiword synonyms. To
support its search-syntax, it has to parse the query string to recognize
special operators like `AND`, `OR`, `+`, `-`, `field:`, and so forth.  (See the full
http://bit.ly/151G5I1[`query_string` syntax]
here.)

As part of this parsing process, it breaks up the query string on whitespace,
and passes each word that it finds to the relevant analyzer separately. This
means that your synonym analyzer will never receive a multiword synonym.
Instead of seeing `United States` as a single string, the analyzer will
receive `United` and `States` separately.

Fortunately, the trustworthy `match` query supports no such syntax, and
multiword synonyms will be passed to the analyzer in their entirety.

