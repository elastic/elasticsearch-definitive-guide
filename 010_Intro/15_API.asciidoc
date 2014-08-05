=== Talking to Elasticsearch

How you talk to Elasticsearch depends on whether you are using Java or not.

==== Java API

If you are using Java, then Elasticsearch comes with two built-in clients
which you can use in your code:

Node client::
    The node client joins a local cluster as a _non-data node_. In other
    words, it doesn't hold any data itself, but it knows what data lives
    on which node in the cluster, and can forward requests directly
    to the correct node.

Transport client::
    The lighter weight transport client can be used to send requests to
    a remote cluster. It doesn't join the cluster itself, but simply
    forwards requests to a node in the cluster.

Both Java clients talk to the cluster over *port 9300*, using the native
Elasticsearch _transport_ protocol.  The nodes in the cluster also communicate
with each other over port 9300. If this port is not open, then your nodes will
not be able to form a cluster.

[TIP]
====
The Java client must be from the same version of Elasticsearch as the nodes,
otherwise they may not be able to understand each other.
====

More information about the Java clients can be found in the Java API section
of the http://www.elasticsearch.org/guide/[Guide].

==== RESTful API with JSON over HTTP

All other languages can communicate with Elasticsearch over *port 9200* using
a RESTful API, accessible with your favorite web client. In fact, as you have
seen above, you can even talk to Elasticsearch from the command line using the
`curl` command.

**************************************************

Elasticsearch provides official clients for several languages -- Groovy,
Javascript, .NET, PHP, Perl, Python, and Ruby --  and there are numerous
community-provided clients and integrations, all of which can be found in the
http://www.elasticsearch.org/guide/[Guide].

**************************************************

A request to Elasticsearch consists of the same parts as any HTTP request. For
instance, to count the number of documents in the cluster, we could use:

[source,js]
--------------------------------------------------
      <1>     <2>                     <3>    <4>
curl -XGET 'http://localhost:9200/_count?pretty' -d '
{  <5>
    "query": {
        "match_all": {}
    }
}
'
--------------------------------------------------
<1> The appropriate HTTP _method_ or _verb_: `GET`, `POST`, `PUT`, `HEAD` or
    `DELETE`
<2> The protocol, hostname and port of any node in the cluster.
<3> The path of the request.
<4> Any optional query string parameters, eg `?pretty` will _pretty-print_
    the JSON response to make it easier to read.
<5> A JSON encoded request body (if the request needs one).

Elasticsearch returns an HTTP status code like `200 OK` and (except for `HEAD`
requests) a JSON encoded response body. The above `curl` request would respond
with a JSON body like the following:

[source,js]
--------------------------------------------------
{
    "count" : 0,
    "_shards" : {
        "total" : 5,
        "successful" : 5,
        "failed" : 0
    }
}
--------------------------------------------------

We don't see the HTTP headers in the response because we didn't ask `curl` to
display them. To see the headers, use the `curl` command with the `-i`
switch:

[source,js]
--------------------------------------------------
curl -i -XGET 'localhost:9200/'
--------------------------------------------------

For the rest of the book, we will show these `curl` examples using a shorthand
format that leaves out all of the bits that are the same in every request,
like the hostname and port, and the `curl` command itself. Instead of showing
a full request like:

[source,js]
--------------------------------------------------
curl -XGET 'localhost:9200/_count?pretty' -d '
{
    "query": {
        "match_all": {}
    }
}'
--------------------------------------------------

we will show it in this shorthand format:

[source,js]
--------------------------------------------------
GET /_count
{
    "query": {
        "match_all": {}
    }
}
--------------------------------------------------
// SENSE: 010_Intro/15_Count.json

In fact, this is the same format that is used by the Sense console that we
installed with <<marvel,Marvel>>. You can open and run this code example in
Sense by clicking the ``View in Sense'' link above.
