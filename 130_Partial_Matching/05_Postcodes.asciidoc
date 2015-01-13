=== Postcodes and Structured Data

We will use United Kingdom postcodes (postal codes in the United States) to illustrate how((("partial matching", "postcodes and structured data"))) to use partial matching with
structured data. UK postcodes have a well-defined structure. For instance, the
postcode `W1V 3DG` can((("postcodes (UK), partial matching with"))) be broken down as follows:

* `W1V`: This outer part identifies the postal area and district:

**  `W` indicates the area (one or two letters)
**  `1V` indicates the district (one or two numbers, possibly followed by a letter

* `3DG`: This inner part identifies a street or building:

** `3` indicates the sector (one number)
** `DG` indicates the unit (two letters)


Let's assume that we are indexing postcodes as exact-value `not_analyzed`
fields, so we could create our index as follows:

[source,js]
--------------------------------------------------
PUT /my_index
{
    "mappings": {
        "address": {
            "properties": {
                "postcode": {
                    "type":  "string",
                    "index": "not_analyzed"
                }
            }
        }
    }
}
--------------------------------------------------
// SENSE: 130_Partial_Matching/10_Prefix_query.json

And index some ((("indexing", "postcodes")))postcodes:

[source,js]
--------------------------------------------------
PUT /my_index/address/1
{ "postcode": "W1V 3DG" }

PUT /my_index/address/2
{ "postcode": "W2F 8HW" }

PUT /my_index/address/3
{ "postcode": "W1F 7HW" }

PUT /my_index/address/4
{ "postcode": "WC1N 1LZ" }

PUT /my_index/address/5
{ "postcode": "SW5 0BE" }
--------------------------------------------------
// SENSE: 130_Partial_Matching/10_Prefix_query.json

Now our data is ready to be queried.
