[[application-joins]]
=== Application-side Joins

We can (partly) emulate a relational((("relationships", "application-side joins")))((("application-side joins"))) database by implementing joins in our
application. ((("joins", "application-side")))For instance, let's say we are indexing users and their
blog posts.  In the relational world, we would do something like this:

[source,json]
--------------------------------
PUT /my_index/user/1 <1>
{
  "name":     "John Smith",
  "email":    "john@smith.com",
  "dob":      "1970/10/24"
}

PUT /my_index/blogpost/2 <1>
{
  "title":    "Relationships",
  "body":     "It's complicated...",
  "user":     1 <2>
}
--------------------------------
<1> The `index`, `type`, and `id` of each document together function as a primary key.
<2> The `blogpost` links to the user by storing the user's `id`.  The `index`
    and `type` aren't required as they are hardcoded in our application.

Finding blog posts by user with ID `1` is easy:

[source,json]
--------------------------------
GET /my_index/blogpost/_search
{
  "query": {
    "filtered": {
      "filter": {
        "term": { "user": 1 }
      }
    }
  }
}
--------------------------------

To find blogposts by a user called John, we would need to run two queries:
the first would look up all users called John in order to find their IDs,
and the second would pass those IDs in a query similar to the preceding one:

[source,json]
--------------------------------
GET /my_index/user/_search
{
  "query": {
    "match": {
      "name": "John"
    }
  }
}

GET /my_index/blogpost/_search
{
  "query": {
    "filtered": {
      "filter": {
        "terms": { "user": [1] }  <1>
      }
    }
  }
}
--------------------------------
<1> The values in the `terms` filter would be populated with the results from
    the first query.

The main advantage of application-side joins is that the data is normalized.
Changing the user's name has to happen in only one place: the `user` document.
The disadvantage is that you have to run extra queries in order to join documents at search time.

In this example, there was only one user who matched our first query, but in
the real world we could easily have millions of users named John.
Including all of their IDs in the second query would make for a very large
query, and one that has to do millions of term lookups.

This approach is suitable when the first entity (the `user` in this example)
has a small number of documents and, preferably, they seldom change. This
would allow the application to cache the results and avoid running the first
query often.




