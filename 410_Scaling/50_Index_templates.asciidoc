[[index-templates]]
=== Index Templates

Elasticsearch doesn't require you to create an index before using it.((("indices", "templates")))((("scaling", "index templates and")))((("templates", "index")))  With
logging, it is often more convenient to rely on index autocreation than to
have to create indices manually.

Logstash uses the timestamp((("Logstash")))((("timestamps, use by Logstash to create index names"))) from an event to derive the index name.  By
default, it indexes into a different index every day, so an event with a
`@timestamp` of `2014-10-01 00:00:01` will be sent to the index
`logstash-2014.10.01`.  If that index doesn't already exist, it will be
created for us.

Usually we want some control over the settings and mappings of the new index.
Perhaps we want to limit the number of shards to `1`, and we want to disable the
`_all` field.  Index templates can be used to control which settings should be
applied to newly created indices:

[source,json]
-------------------------
PUT /_template/my_logs <1>
{
  "template": "logstash-*", <2>
  "order":    1, <3>
  "settings": {
    "number_of_shards": 1 <4>
  },
  "mappings": {
    "_default_": { <5>
      "_all": {
        "enabled": false
      }
    }
  },
  "aliases": {
    "last_3_months": {} <6>
  }
}
-------------------------
<1> Create a template called `my_logs`.
<2> Apply this template to all indices beginning with `logstash-`.
<3> This template should override the default `logstash` template that has
    a lower `order`.
<4> Limit the number of primary shards to `1`.
<5> Disable the `_all` field for all types.
<6> Add this index to the `last_3_months` alias.

This template specifies the default settings that will be applied to any index
whose name begins with `logstash-`, whether it is created manually or
automatically. If we think the index for tomorrow will need more capacity than
today, we can update the index to use a higher number of shards.

The template even adds the newly created index into the `last_3_months` alias, although
removing the old indices from that alias will have to be done manually.
