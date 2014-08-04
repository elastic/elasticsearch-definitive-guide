=== Document oriented

Objects in an application are seldom just a simple list of keys and values.
More often than not they are complex data structures which may contain dates,
geo-locations, objects, or arrays of values.

Sooner or later you're going to want to store these objects in a database.
Trying to do this with the rows and columns of a relational database is the
equivalent of trying to squeeze your rich expressive objects into a very big
spreadsheet: you have to flatten the object to fit the table schema -- usually
one field per column -- and then have to reconstruct it every time you
retrieve it.

Elasticsearch is _document oriented_, meaning that it stores entire objects or
_documents_.  Not only does it store them, it also *indexes* the contents of
each document in order to make them searchable. In Elasticsearch, you index,
search, sort and filter documents... not rows of columnar data.  This is a
fundamentally different way of thinking about data and is one of the reasons
Elasticsearch can perform complex full text search.

==== JSON

Elasticsearch uses http://en.wikipedia.org/wiki/Json[_JSON_] (or JavaScript
Object Notation ) as the serialization format for documents. JSON
serialization is supported by most programming languages, and has become the
standard format used by the NoSQL movement. It is simple, concise and easy to
read.

Consider this JSON document which represents a user object:

[source,js]
--------------------------------------------------
{
    "email":      "john@smith.com",
    "first_name": "John",
    "last_name":  "Smith",
    "info": {
        "bio":         "Eco-warrior and defender of the weak",
        "age":         25,
        "interests": [ "dolphins", "whales" ]
    },
    "join_date": "2014/05/01"
}
--------------------------------------------------

Although the original `user` object was complex, the structure and meaning of
the object has been retained in the JSON version. Converting an object to JSON
for indexing in Elasticsearch is much simpler than the equivalent process for
a flat table structure.

.Converting your data to JSON
**************************************************

Almost all languages have modules which will convert arbitrary  data
structures or objects into JSON for you, but the details are specific  to each
language. Look for modules which handle JSON __ ``serialization'' __ or __
``marshalling'' __. http://www.elasticsearch.org/guide[The official
Elasticsearch clients] all handle conversion to and from JSON for you
automatically.

**************************************************
