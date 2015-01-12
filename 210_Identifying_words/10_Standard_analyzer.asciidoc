[[standard-analyzer]]
=== standard Analyzer

The `standard` analyzer is used by default for any full-text `analyzed` string
field. ((("standard analyzer"))) If we were to reimplement the  `standard` analyzer as a
<<custom-analyzers,`custom` analyzer>>, it would be defined as follows:

[role="pagebreak-before"]
[source,js]
--------------------------------------------------
{
    "type":      "custom",
    "tokenizer": "standard",
    "filter":  [ "lowercase", "stop" ]
}
--------------------------------------------------

In <<token-normalization>> and <<stopwords>>, we talk about the
`lowercase`, and `stop` _token filters_, but for the moment, let's focus on
the `standard` _tokenizer_.

