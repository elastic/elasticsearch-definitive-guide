[[ngrams-compound-words]]
=== Ngrams for Compound Words

Finally, let's take a look at how n-grams can be used to search languages with
compound words. ((("languages", "using many compound words, indexing of")))((("n-grams", "using with compound words")))((("partial matching", "using n-grams for compound words")))((("German", "compound words in"))) German is famous for combining several small words into one
massive compound word in order to capture precise or complex meanings. For
example:

_Aussprachewörterbuch_::
    Pronunciation dictionary

_Militärgeschichte_::
    Military history

_Weißkopfseeadler_::
    White-headed sea eagle, or bald eagle

_Weltgesundheitsorganisation_::
    World Health Organization

_Rindfleischetikettierungsüberwachungsaufgabenübertragungsgesetz_::
    The law concerning the delegation of duties for the supervision of cattle
    marking and the labeling of beef

Somebody searching for ``Wörterbuch'' (dictionary) would probably expect to
see ``Aussprachewörtebuch'' in the results list. Similarly, a search for
``Adler'' (eagle) should include ``Weißkopfseeadler.''

One approach to indexing languages like this is to break compound words into
their constituent parts using the http://bit.ly/1ygdjjC[compound word token filter].
However, the quality of the results depends on how good your compound-word
dictionary is.

Another approach is just to break all words into n-grams and to search for any
matching fragments--the more fragments that match, the more relevant the
document.

Given that an n-gram is a moving window on a word, an n-gram of any length
will cover all of the word.  We want to choose a length that is long enough
to be meaningful, but not so long that we produce far too many unique terms.
A _trigram_ (length 3) is ((("trigrams")))probably a good starting point:

[source,js]
--------------------------------------------------
PUT /my_index
{
    "settings": {
        "analysis": {
            "filter": {
                "trigrams_filter": {
                    "type":     "ngram",
                    "min_gram": 3,
                    "max_gram": 3
                }
            },
            "analyzer": {
                "trigrams": {
                    "type":      "custom",
                    "tokenizer": "standard",
                    "filter":   [
                        "lowercase",
                        "trigrams_filter"
                    ]
                }
            }
        }
    },
    "mappings": {
        "my_type": {
            "properties": {
                "text": {
                    "type":     "string",
                    "analyzer": "trigrams" <1>
                }
            }
        }
    }
}
--------------------------------------------------
// SENSE: 130_Partial_Matching/40_Compound_words.json

<1> The `text` field uses the `trigrams` analyzer to index its contents as
    n-grams of length 3.

Testing the trigrams analyzer with the `analyze` API

[source,js]
--------------------------------------------------
GET /my_index/_analyze?analyzer=trigrams
Weißkopfseeadler
--------------------------------------------------
// SENSE: 130_Partial_Matching/40_Compound_words.json

returns these terms:

    wei, eiß, ißk, ßko, kop, opf, pfs, fse, see, eea,ead, adl, dle, ler

We can index our example compound words to test this approach:

[source,js]
--------------------------------------------------
POST /my_index/my_type/_bulk
{ "index": { "_id": 1 }}
{ "text": "Aussprachewörterbuch" }
{ "index": { "_id": 2 }}
{ "text": "Militärgeschichte" }
{ "index": { "_id": 3 }}
{ "text": "Weißkopfseeadler" }
{ "index": { "_id": 4 }}
{ "text": "Weltgesundheitsorganisation" }
{ "index": { "_id": 5 }}
{ "text": "Rindfleischetikettierungsüberwachungsaufgabenübertragungsgesetz" }
--------------------------------------------------
// SENSE: 130_Partial_Matching/40_Compound_words.json

A search for ``Adler'' (eagle) becomes a query for the three terms `adl`, `dle`,
and `ler`:

[source,js]
--------------------------------------------------
GET /my_index/my_type/_search
{
    "query": {
        "match": {
            "text": "Adler"
        }
    }
}
--------------------------------------------------
// SENSE: 130_Partial_Matching/40_Compound_words.json

which correctly matches ``Weißkopfsee-__adler__'':

[source,js]
--------------------------------------------------
{
  "hits": [
     {
        "_id": "3",
        "_score": 3.3191128,
        "_source": {
           "text": "Weißkopfseeadler"
        }
     }
  ]
}
--------------------------------------------------
// SENSE: 130_Partial_Matching/40_Compound_words.json

A similar query for ``Gesundheit'' (health) correctly matches
``Welt-__gesundheit__-sorganisation,'' but it also matches
``Militär-__ges__-chichte'' and
``Rindfleischetikettierungsüberwachungsaufgabenübertragungs-__ges__-etz,''
both of which also contain the trigram `ges`.

Judicious use of the `minimum_should_match` parameter can remove these
spurious results by requiring that a minimum number of trigrams must be
present for a document to be considered a match:

[source,js]
--------------------------------------------------
GET /my_index/my_type/_search
{
    "query": {
        "match": {
            "text": {
                "query":                "Gesundheit",
                "minimum_should_match": "80%"
            }
        }
    }
}
--------------------------------------------------
// SENSE: 130_Partial_Matching/40_Compound_words.json

This is a bit of a shotgun approach to full-text search and can result in a
large inverted index, but it is an effective generic way of indexing languages
that use many compound words or that don't use whitespace between words,
such as Thai.

This technique is used to increase _recall_&#x2014;the number of relevant
documents that a search returns.  It is usually used in combination with
other techniques, such as shingles (see <<shingles>>) to improve precision and
the relevance score of each document.
