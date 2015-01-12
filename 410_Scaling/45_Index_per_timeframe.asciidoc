[[time-based]]
=== Time-Based Data

One of the most common use cases for Elasticsearch is for logging,((("logging", "using Elasticsearch for")))((("time-based data")))((("scaling", "time-based data and"))) so common
in fact that Elasticsearch provides an integrated((("ELK stack"))) logging platform called the
_ELK stack_&#x2014;Elasticsearch, Logstash, and Kibana--to make the process easy.

http://www.elasticsearch.org/overview/logstash[Logstash] collects, parses, and
enriches logs before indexing them into Elasticsearch.((("Logstash")))  Elasticsearch acts as
a centralized logging server, and
http://www.elasticsearch.org/overview/kibana[Kibana] is a((("Kibana"))) graphic frontend
that makes it easy to query and visualize what is happening across your
network in near real-time.

Most traditional use cases for search engines involve a relatively static
collection of documents that grows slowly. Searches look for the most relevant
documents, regardless of when they were created.

Logging--and other time-based data streams such as social-network activity--are very different in nature. ((("social-network activity"))) The number of documents in the index grows
rapidly, often accelerating with time.  Documents are almost never updated,
and searches mostly target the most recent documents.  As documents age, they
lose value.

We need to adapt our index design to function with the flow of time-based
data.

[[index-per-timeframe]]
==== Index per Time Frame

If we were to have one big index for documents of this type, we would soon run
out of space. Logging events just keep on coming, without pause or
interruption. We could delete the old events, with a `delete-by-query`:

[source,json]
-------------------------
DELETE /logs/event/_query
{
  "query": {
    "range": {
      "@timestamp": { <1>
        "lt": "now-90d"
      }
    }
  }
}
-------------------------
<1> Deletes all documents where Logstash's `@timestamp` field is
    older than 90 days.

But this approach is _very inefficient_.  Remember that when you delete a
document, it is only _marked_ as deleted (see <<deletes-and-updates>>). It won't
be physically deleted until the segment containing it is merged away.

Instead, use an _index per time frame_. ((("indices", "index per-timeframe")))You could start out with an index per
year (`logs_2014`) or per month (`logs_2014-10`).  Perhaps, when your
website gets really busy, you need to switch to an index per day
(`logs_2014-10-24`).  Purging old data is easy: just delete old indices.

This approach has the advantage of allowing you to scale as and when you need
to.  You don't have to make any difficult decisions up front.  Every day is a
new opportunity to change your indexing time frames to suit the current demand.
Apply the same logic to how big you make each index.  Perhaps all you need is
one primary shard per week initially.  Later, maybe you need five primary shards
per day.  It doesn't matter--you can adjust to new circumstances at any
time.

Aliases can help make switching indices more transparent.((("aliases, index")))  For indexing,
you can point `logs_current` to the index currently accepting new log events,
and for searching, update `last_3_months` to point to all indices for the
previous three months:

[source,json]
-------------------------
POST /_aliases
{
  "actions": [
    { "add":    { "alias": "logs_current",  "index": "logs_2014-10" }}, <1>
    { "remove": { "alias": "logs_current",  "index": "logs_2014-09" }}, <1>
    { "add":    { "alias": "last_3_months", "index": "logs_2014-10" }}, <2>
    { "remove": { "alias": "last_3_months", "index": "logs_2014-07" }}  <2>
  ]
}
-------------------------
<1> Switch `logs_current` from September to October.
<2> Add October to `last_3_months` and remove July.
