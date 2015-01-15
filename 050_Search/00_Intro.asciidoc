[[search]]
== Searching--The Basic Tools

So far, we have learned how to use Elasticsearch as a simple NoSQL-style
distributed document store. We can ((("searching")))throw JSON documents at Elasticsearch and
retrieve each one by ID. But the real power of Elasticsearch lies in its
ability to make sense out of chaos -- to turn Big Data into Big Information.

This is the reason that we use structured JSON documents, rather than
amorphous blobs of data.  Elasticsearch not only _stores_ the document, but
also _indexes_ the content of the document in order to make it searchable.

_Every field in a document is indexed and can be queried_. ((("indexing"))) And it's not just
that. During a single query, Elasticsearch can use _all_ of these indices, to
return results at breath-taking speed.  That's something that you could never
consider doing with a traditional database.

A _search_ can be any of the following:

* A structured query on concrete fields((("fields", "searching on")))((("searching", "types of searches"))) like `gender` or `age`, sorted by
  a field like `join_date`, similar to the type of query that you could construct 
  in SQL

* A full-text query, which finds all documents matching the search keywords,
  and returns them sorted by _relevance_

* A combination of the two

While many searches will just work out of((("full text search"))) the box, to use Elasticsearch to
its full potential, you need to understand three subjects:

 _Mapping_::     
   How the data in each field is interpreted
   
 _Analysis_::    
   How full text is processed to make it searchable
   
 _Query DSL_::   
   The flexible, powerful query language used by Elasticsearch

Each of these is a big subject in its own right, and we explain them in
detail in <<search-in-depth>>. The chapters in this section introduce the
basic concepts of all three--just enough to help you to get an overall
understanding of how search works.

We will start by explaining the `search` API in its simplest form.

.Test Data

****

The documents that we will use for test purposes in this chapter can be found
in this gist: https://gist.github.com/clintongormley/8579281.

You can copy the commands and paste them into your shell in order to follow
along with this chapter.

Alternatively, if you're in the online version of this book, you can link:sense_widget.html?snippets/050_Search/Test_data.json[click here to open in Sense].

****
