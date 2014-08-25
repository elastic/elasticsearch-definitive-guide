[[document]]
=== What is a document?

Most entities or objects in most applications can be serialized into a JSON
object, with keys and values. A _key_ is the name of a _field_ or _property_,
and a _value_ can be a string, a number, a boolean, another object, an array
of values, or some other specialized type such as a string representing a date
or an object representing a geolocation:

[source,js]
--------------------------------------------------
{
    "name":         "John Smith",
    "age":          42,
    "confirmed":    true,
    "join_date":    "2014-06-01",
    "home": {
        "lat":      51.5,
        "lon":      0.1
    },
    "accounts": [
        {
            "type": "facebook",
            "id":   "johnsmith"
        },
        {
            "type": "twitter",
            "id":   "johnsmith"
        }
    ]
}
--------------------------------------------------


Often, we use the terms _object_ and _document_ interchangeably. However,
there is a distinction.  An object is just a JSON object -- similar to what is
known as a hash, hashmap, dictionary or associative array. Objects may contain
other objects.

In Elasticsearch, the term _document_ has a specific meaning. It refers
to the top-level or _root object_ which is serialized into JSON and
stored in Elasticsearch under a unique ID.

=== Document metadata

A document doesn't consist only of its data. It also has
_metadata_ -- information *about* the document. The three required metadata
elements are:

[horizontal]
`_index`::  Where the document lives.
`_type`::   The class of object that the document represents.
`_id`::     The unique identifier for the document.

==== `_index`

An _index_ is like a ``database'' in a relational database -- it is the place
we store and index related data.

TIP: Actually, in Elasticsearch, our data is stored and indexed in _shards_,
while an index is just a logical namespace which groups together one or more
shards. However, this is an internal detail -- our application shouldn't care
about shards at all.  As far as our application is concerned, our documents
live in an _index_. Elasticsearch takes care of the details.

We will discuss how to create and manage indices ourselves in <<index-management>>,
but for now we will let Elasticsearch create the index for us.  All we have to
do is to choose an index name.  This name must be lower case, cannot begin with an
underscore and cannot contain commas. Let's use `website` as our index name.

==== `_type`

In applications, we use objects to represent ``things'' such as a user, a blog
post, a comment, or an email. Each object belongs to a _class_ which defines
the properties or data associated with an object. Objects in the `user` class
may have a name, a gender, an age and an email address.

In a relational database, we usually store objects of the same class in the
same table because they share the same data structure. For the same reason, in
Elasticsearch we use the same _type_ for documents which represent the same
class of ``thing'', because they share the same data structure.

Every _type_ has its own <<mapping,mapping>> or schema definition, which
defines the data structure for documents of that type, much like the columns
in a database table. Documents of all types can be stored in the same index,
but the _mapping_ for the type tells Elasticsearch how the data in each
document should be indexed.

We will discuss how to specify and manage mappings in <<mapping>>, but for now
we will rely on Elasticsearch to detect our document's data structure
automatically.

A `_type` name can be lower or upper case, but shouldn't begin with an
underscore, or contain commas.  We shall use `blog` for our type name.

==== `_id`

The _id_ is a string that, when combined with the `_index` and `_type`,
uniquely identifies a document in Elasticsearch. When creating a new document,
you can either provide your own `_id` or let Elasticsearch generate one for
you.

==== Other metadata

There are several other metadata elements, which we will discuss in
<<mapping>>. With the elements listed above, we are already able to store a
document in Elasticsearch and to retrieve it by ID -- in other words, to use
Elasticsearch as a document store.
