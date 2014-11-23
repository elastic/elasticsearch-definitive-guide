[[lowercase-token-filter]]
=== In That Case

The most frequently used token filter is the `lowercase` filter, which does
exactly what you would expect; it transforms ((("tokens", "normalizing", "lowercase filter")))((("lowercase token filter")))each token into its lowercase
form:

[source,js]
--------------------------------------------------
GET /_analyze?tokenizer=standard&filters=lowercase
The QUICK Brown FOX! <1>
--------------------------------------------------
<1> Emits tokens `the`, `quick`, `brown`, `fox`

It doesn't matter whether users search for `fox` or `FOX`, as long as the same
analysis process is applied at query time and at search time. The `lowercase`
filter will transform a query for `FOX` into a query for `fox`, which is the
same  token that we have stored in our inverted index.

To use token filters as part of the analysis process, we ((("analyzers", "using token filters")))((("token filters", "using with analyzers")))can create a `custom`
analyzer:

[source,js]
--------------------------------------------------
PUT /my_index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_lowercaser": {
          "tokenizer": "standard",
          "filter":  [ "lowercase" ]
        }
      }
    }
  }
}
--------------------------------------------------

And we can test it out with the `analyze` API:

[source,js]
--------------------------------------------------
GET /my_index/_analyze?analyzer=my_lowercaser
The QUICK Brown FOX! <1>
--------------------------------------------------
<1> Emits tokens `the`, `quick`, `brown`, `fox`

