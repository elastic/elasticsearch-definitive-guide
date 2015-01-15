[[using-synonyms]]
=== Using Synonyms

Synonyms can replace existing tokens or((("synonyms", "using"))) be added to the token stream by using the((("synonym token filter")))
http://bit.ly/1DInEGD[`synonym` token filter]:

[source,json]
-------------------------------------
PUT /my_index
{
  "settings": {
    "analysis": {
      "filter": {
        "my_synonym_filter": {
          "type": "synonym", <1>
          "synonyms": [ <2>
            "british,english",
            "queen,monarch"
          ]
        }
      },
      "analyzer": {
        "my_synonyms": {
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "my_synonym_filter" <3>
          ]
        }
      }
    }
  }
}
-------------------------------------
<1> First, we define a token filter of type `synonym`.
<2> We discuss synonym formats in <<synonym-formats>>.
<3> Then we create a custom analyzer that uses the `my_synonym_filter`.

[TIP]
==================================================

Synonyms can be specified inline with the `synonyms` parameter, or in a
synonyms file that must((("synonyms", "specifying inline or in a separate file"))) be present on every node in the cluster. The path to
the synonyms file should be specified with the `synonyms_path` parameter, and
should be either absolute or relative to the Elasticsearch `config` directory.
See <<updating-stopwords>> for techniques that can be used to refresh the
synonyms list.

==================================================

Testing our analyzer with the `analyze` API shows the following:

[source,json]
-------------------------------------
GET /my_index/_analyze?analyzer=my_synonyms
Elizabeth is the English queen
-------------------------------------

[source,text]
------------------------------------
Pos 1: (elizabeth)
Pos 2: (is)
Pos 3: (the)
Pos 4: (british,english) <1>
Pos 5: (queen,monarch) <1>
------------------------------------
<1> All synonyms occupy the same position as the original term.

A document like this will match queries for any of the following: `English queen`,
`British queen`, `English monarch`, or `British monarch`.
Even a phrase query will work, because the position of
each term has been preserved.

[TIP]
======================================

Using the same `synonym` token filter at both index time and search time is
redundant.((("synonym token filter", "using at index time versus search time")))  If, at index time, we replace `English` with the two terms
`english` and `british`, then at search time we need to search for only one of
those terms.  Alternatively, if we don't use synonyms at index time, then at
search time, we would need to convert a query for `English` into a query for
`english OR british`.

Whether to do synonym expansion at search or index time can be a difficult
choice.  We will explore the options more in <<synonyms-expand-or-contract>>.

======================================
