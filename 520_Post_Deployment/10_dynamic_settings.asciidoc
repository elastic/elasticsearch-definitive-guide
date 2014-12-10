
=== Changing Settings Dynamically

Many settings in Elasticsearch are dynamic and can be modified through the API.
Configuration changes that force a node (or cluster) restart are strenuously avoided.((("post-deployment", "changing settings dynamically")))
And while it's possible to make the changes through the static configs, we
recommend that you use the API instead.

The `cluster-update` API operates((("Cluster Update API"))) in two modes:

Transient:: 
    These changes are in effect until the cluster restarts.  Once
a full cluster restart takes place, these settings are erased.

Persistent::
    These changes are permanently in place unless explicitly changed.
They will survive full cluster restarts and override the static configuration files.

Transient versus persistent settings are supplied in the JSON body:

[source,js]
----
PUT /_cluster/settings
{
    "persistent" : {
        "discovery.zen.minimum_master_nodes" : 2 <1>
    },
    "transient" : {
        "indices.store.throttle.max_bytes_per_sec" : "50mb" <2>
    }
}
----
<1> This persistent setting will survive full cluster restarts.
<2> This transient setting will be removed after the first full cluster 
restart.

A complete list of settings that can be updated dynamically can be found in the
http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/cluster-update-settings.html[online reference docs].

