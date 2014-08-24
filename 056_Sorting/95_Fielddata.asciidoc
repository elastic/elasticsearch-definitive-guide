[[fielddata-intro]]
=== Fielddata

Our final topic in this chapter is about an internal aspect of Elasticsearch.
While we don't demonstrate any new techniques here, _fielddata_ is an
important topic which we will refer to repeatedly, and is something that you
should be aware of.

When you sort on a field, Elasticsearch needs access to the value for that
field for every document which matches the query.  The inverted index, which
performs very well when searching, is not the ideal structure for sorting on
field values.

* When searching we need to be able to map a term to a list of documents.

* When sorting, we need to map a document to its terms. In other words, we
  need to ``uninvert'' the inverted index.

In order to make sorting efficient, Elasticsearch loads all of the values for
the field that you want to sort on into memory. This is referred to as
_fielddata_.

IMPORTANT: It doesn't just load the values for the documents that matched a
particular query. It loads the values from *every document in your index*,
regardless of the document `type`.

The reason that it loads all values into memory is that uninverting the index
from disk is slow.  Even though you may only need the values for a few docs
for the current request, you will probably need access to the values for other
docs on the next request, so it makes sense to load all the values into memory
at once, and to keep them there.

Fielddata is used in several places in Elasticsearch:

* sorting on a field
* aggregations on a field
* certain filters, eg geo-location filters
* scripts which refer to fields

Clearly, this can consume a lot of memory, especially for high cardinality
string fields -- string fields that have many unique values -- like the body
of an email. Fortunately, insufficient memory is a problem which can be solved
by horizontal scaling, by adding more nodes to your cluster.

For now, all you need to know is what fielddata is, and to be aware that it
can be memory hungry.  Later we will show you how to see how much memory fielddata
is using, how to limit the amount of memory that is available to it, and
how to preload fielddata to improve the user experience.






