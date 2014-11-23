[[configuring-language-analyzers]]
=== Configuring Language Analyzers

While the language analyzers can be used out of the box without any
configuration, most of them ((("english analyzer", "configuring")))((("language analyzers", "configuring")))do allow you to control aspects of their
behavior, specifically:

[[stem-exclusion]]
Stem-word exclusion::
+
Imagine, for instance, that users searching for((("language analyzers", "configuring", "stem word exclusion")))((("stemming words", "stem word exclusion, configuring"))) the ``World Health
Organization'' are instead getting results for ``organ health.'' The reason
for this confusion is that both ``organ'' and ``organization'' are stemmed to
the same root word: `organ`. Often this isn't a problem, but in this
particular collection of documents, this leads to confusing results. We would
like to prevent the words `organization` and `organizations` from being
stemmed.

Custom stopwords::

The default list of stopwords((("stopwords", "configuring for language analyzers"))) used in English are as follows:
+
    a, an, and, are, as, at, be, but, by, for, if, in, into, is, it,
    no, not, of, on, or, such, that, the, their, then, there, these,
    they, this, to, was, will, with
+
The unusual thing about `no` and `not` is that they invert the meaning of the
words that follow them. Perhaps we decide that these two words are important
and that we shouldn't treat them as stopwords.

To customize the behavior of the `english` analyzer, we need to
create a custom analyzer that uses the `english` analyzer as its base but
adds some configuration:

[source,js]
--------------------------------------------------
PUT /my_index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_english": {
          "type": "english",
          "stem_exclusion": [ "organization", "organizations" ], <1>
          "stopwords": [ <2>
            "a", "an", "and", "are", "as", "at", "be", "but", "by", "for",
            "if", "in", "into", "is", "it", "of", "on", "or", "such", "that",
            "the", "their", "then", "there", "these", "they", "this", "to",
            "was", "will", "with"
          ]
        }
      }
    }
  }
}

GET /my_index/_analyze?analyzer=my_english <3>
The World Health Organization does not sell organs.
--------------------------------------------------
<1> Prevents `organization` and `organizations` from being stemmed
<2> Specifies a custom list of stopwords
<3> Emits tokens `world`, `health`, `organization`, `does`, `not`, `sell`, `organ`

We discuss stemming and stopwords in much more detail in <<stemming>> and
<<stopwords>>, respectively.

