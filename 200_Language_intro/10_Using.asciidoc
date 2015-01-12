[[using-language-analyzers]]
=== Using Language Analyzers

The built-in language analyzers are available globally and don't need to be
configured before being used.((("language analyzers", "using")))  They can be specified directly in the field
mapping:

[source,js]
--------------------------------------------------
PUT /my_index
{
  "mappings": {
    "blog": {
      "properties": {
        "title": {
          "type":     "string",
          "analyzer": "english" <1>
        }
      }
    }
  }
}
--------------------------------------------------
<1> The `title` field will use the `english` analyzer instead of the default
    `standard` analyzer.

Of course, by passing ((("english analyzer", "information lost with")))text through the `english` analyzer, we lose
information:

[source,js]
--------------------------------------------------
GET /my_index/_analyze?field=title <1>
I'm not happy about the foxes
--------------------------------------------------
<1> Emits token: `i'm`, `happi`, `about`, `fox`

We can't tell if the document mentions one `fox` or many  `foxes`; the word
`not` is a stopword and is removed, so we can't tell whether the document is
happy about foxes or not. By using the `english` analyzer, we have increased
recall as we can match more loosely, but we have reduced our ability to rank
documents accurately.

To get the best of both worlds, we can use <<multi-fields,multifields>> to
index the `title` field twice: once((("multifields", "using to index a field with two different analyzers"))) with the `english` analyzer and once with
the `standard` analyzer:

[source,js]
--------------------------------------------------
PUT /my_index
{
  "mappings": {
    "blog": {
      "properties": {
        "title": { <1>
          "type": "string",
          "fields": {
            "english": { <2>
              "type":     "string",
              "analyzer": "english"
            }
          }
        }
      }
    }
  }
}
--------------------------------------------------
<1> The main `title` field uses the `standard` analyzer.
<2> The `title.english` subfield uses the `english` analyzer.

With this mapping in place, we can index some test documents to demonstrate
how to use both fields at query time:

[source,js]
--------------------------------------------------
PUT /my_index/blog/1
{ "title": "I'm happy for this fox" }

PUT /my_index/blog/2
{ "title": "I'm not happy about my fox problem" }

GET /_search
{
  "query": {
    "multi_match": {
      "type":     "most_fields", <1>
      "query":    "not happy foxes",
      "fields": [ "title", "title.english" ]
    }
  }
}
--------------------------------------------------
<1> Use the <<most-fields,`most_fields`>> query type to match the
    same text in as many fields as possible.

Even ((("most fields queries")))though neither of our documents contain the word `foxes`,  both documents
are returned as results thanks to the word stemming on the `title.english`
field.  The second document is ranked as more relevant, because the word `not`
matches on the `title` field.


