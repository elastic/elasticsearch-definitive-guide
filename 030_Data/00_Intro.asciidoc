[[data-in-data-out]]
== Data In, Data Out

Whatever program we write, the intention is the same: to organize data in a
way that serves our purposes.  But data doesn't consist of just random bits
and bytes.  We build relationships between data elements in order to represent
entities, or _things_ that exist in the real world.  A name and an email
address have more meaning if we know that they belong to the same person.

In the real world, though, not all entities of the same type look the same.
One person might have a home telephone number, while another person has only a
cell-phone number, and another might have both.  One person might have three
email addresses, while another has none. A Spanish person will probably have
two last names, while an English person will probably have only one.

One of the reasons that object-oriented programming languages are so popular
is that objects help us represent and manipulate real-world entities with
potentially complex data structures. So far, so good.

The problem comes when we need to store these entities. Traditionally, we have
stored our data in columns and rows in a relational database, the equivalent
of using a spreadsheet.  All the flexibility gained from using objects is lost
because of the inflexibility of our storage medium.

But what if we could store our objects as objects?((("objects", "storing as objects")))  Instead of modeling our
application around the limitations of spreadsheets, we can instead focus on _using_ the data. The flexibility of objects is returned to us.

An _object_ is a language-specific, in-memory data structure.((("objects", "defined"))) To send it across
the network or store it, we need to be able to represent it in some standard
format. http://en.wikipedia.org/wiki/Json[JSON]
is a way of representing objects in human-readable text.((("objects", "represented by JSON")))((("JSON", "representing objects in human-readable text")))((("JavaScript Object Notation", see="JSON")))  It has become the
de facto standard for exchanging data in the NoSQL world. When an object has
been serialized into JSON, it is known as a _JSON document_.((("JSON documents")))

Elasticsearch is a distributed _document_ store.((("document store, Elasticsearch as"))) It can store and retrieve
complex data structures--serialized as JSON documents--in _real time_. In
other words, as soon as a document has been stored in Elasticsearch, it can be
retrieved from any node in the cluster.

Of course, we don't need to only store data; we must also query it, en masse
and at speed. While NoSQL solutions exist that allow us to store
objects as documents, they still require us to think about how we want to
query our data, and which fields require an index in order to make data
retrieval fast.

In Elasticsearch, _all data in every field_ is _indexed by default_.((("indexing", "in Elasticsearch"))) That is,
every field has a dedicated inverted index for fast retrieval. And, unlike
most other databases, it can use all of those inverted indices _in the same
query_, to return results at breathtaking speed.

In this chapter, we present the APIs that we use to create, retrieve,
update, and delete documents. For the moment, we don't care about the data
inside our documents or how to query them. All we care about is how to store our
documents safely in Elasticsearch and how to get them back again.
