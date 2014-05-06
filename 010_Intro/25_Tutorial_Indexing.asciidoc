=== Finding your feet

In order to give you a feel for what is possible in Elasticsearch and how easy
it is to use, let's start by walking through a simple tutorial which covers
basic concepts such as _indexing_, _search_ and _aggregations_.

We'll introduce some new terminology and basic concepts along the way, but it
is OK if you don't understand everything immediately.  We'll cover all the
concepts introduced here in _much_ greater depth throughout the rest of the
book.

So, sit back and enjoy a whirlwind tour of what Elasticsearch is capable of.

==== Let's build an employee directory.

We happen to work for **Megacorp**, and as part of HR's new _"We love our
drones!"_ initiative, we have been tasked with creating an employee directory.
The directory is supposed to foster employer empathy and
real-time synergistic-dynamic-collaboration, so it has a few different
business requirements:

* Data can contain multi-value tags, numbers and full-text.
* Retrieve the full details of any employee.
* Allow structured search, such as finding employees over the age of 30.
* Allow simple full text search and more complex _phrase_ searches.
* Returned highlighted search _snippets_ from the text in the
  matching documents.
* Enable management to build analytic dashboards over the data.

=== Indexing employee documents

The first order of business is storing employee data.  This will take the form
of an ``employee document'', where a single document represents a single
employee.  The act of storing data in Elasticsearch is called _indexing_, but
before we can index a document we need to decide _where_ to store it.

In Elasticsearch, a document belongs to a _type_, and those types live inside
an _index_. You can draw some (rough) parallels to a traditional relational database:

    Relational DB  ⇒ Databases ⇒ Tables ⇒ Rows      ⇒ Columns
    Elasticsearch  ⇒ Indices   ⇒ Types  ⇒ Documents ⇒ Fields

An Elasticsearch cluster can contain multiple _indices_ (databases), which in
turn contain multiple _types_ (tables). These types hold multiple _documents_
(rows), and each document has multiple _fields_ (columns).

.Index vs Index vs Index
**************************************************

You may already have noticed that the word ``index'' is overloaded with
several different meanings in the context of Elasticsearch. A little
clarification is necessary:

Index (noun)::

As explained above, an _index_ is like a _database_ in a traditional
relational database. It is the place to store related documents. The plural of
_index_ is _indices_ or _indexes_.

Index (verb)::

__ ``To index a document'' __ is to store a document in an _index (noun)_ so
that it can be retrieved and queried. It is much like the `INSERT` keyword in
SQL except that, if the document already exists, then the new document would
replace the old.

Inverted index::

Relational databases add an _index_, such as a B-Tree index, to specific
columns in order to improve the speed of data retrieval.  Elasticsearch and
Lucene use a structure called an _inverted index_ for exactly the same
purpose.
+
By default, every field in a document is _indexed_ (has an inverted index)
and thus is searchable. A field without an inverted index is not searchable.
We discuss inverted indexes in more detail in <<inverted-index>>.

**************************************************

So for our employee directory, we are going to do the following:

*  Index a _document_ per employee, which contains all the details of a single
   employee.
*  Each document will be of _type_ `employee`.
* That type will live in the `megacorp` _index_.
* That index will reside within our Elasticsearch cluster.

In practice, this is very easy (even though it looks like a lot of steps).  We
can perform all of those actions in a single command:

[source,js]
--------------------------------------------------
PUT /megacorp/employee/1
{
    "first_name" : "John",
    "last_name" :  "Smith",
    "age" :        25,
    "about" :      "I love to go rock climbing",
    "interests": [ "sports", "music" ]
}
--------------------------------------------------
// SENSE: 010_Intro/25_Index.json

Notice that the path `/megacorp/employee/1` contains three pieces of
information:

[horizontal]
*megacorp*::    the index name
*employee*::    the type name
*1*::           the ID of this particular employee

The request body -- the JSON document -- contains all the information about
this employee.  His name is ``John Smith'', he's 25 and enjoys rock climbing.

Simple!  There was no need to perform any administrative tasks first, like
creating an index or specifying the type of data that each field contains. We
could just index a document directly.  Elasticsearch ships with defaults for
everything, so all the necessary administration tasks were taken care of in
the background, using default values.

Before moving on, let's add a few more employees to the directory:

[source,js]
--------------------------------------------------
PUT /megacorp/employee/2
{
    "first_name" :  "Jane",
    "last_name" :   "Smith",
    "age" :         32,
    "about" :       "I like to collect rock albums",
    "interests":  [ "music" ]
}

PUT /megacorp/employee/3
{
    "first_name" :  "Douglas",
    "last_name" :   "Fir",
    "age" :         35,
    "about":        "I like to build cabinets",
    "interests":  [ "forestry" ]
}
--------------------------------------------------
// SENSE: 010_Intro/25_Index.json



