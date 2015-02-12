=== Important Configuration Changes
Elasticsearch ships with _very good_ defaults,((("deployment", "configuration changes, important")))((("configuration changes, important"))) especially when it comes to performance-
related settings and options.  When in doubt, just leave
the settings alone.  We have witnessed countless dozens of clusters ruined
by errant settings because the administrator thought he could turn a knob
and gain 100-fold improvement.

[NOTE]
====
Please read this entire section!  All configurations presented are equally
important, and are not listed in any particular order.  Please read
through all configuration options and apply them to your cluster.
====

Other databases may require tuning, but by and large, Elasticsearch does not.
If you are hitting performance problems, the solution is usually better data
layout or more nodes.  There are very few "magic knobs" in Elasticsearch.
If there were, we'd have turned them already!

With that said, there are some _logistical_ configurations that should be changed
for production.  These changes are necessary either to make your life easier, or because
there is no way to set a good default (because it depends on your cluster layout).


==== Assign Names

Elasticseach by default starts a cluster named `elasticsearch`. ((("configuration changes, important", "assigning names"))) It is wise
to rename your production cluster to something else, simply to prevent accidents
whereby someone's laptop joins the cluster.  A simple change to `elasticsearch_production`
can save a lot of heartache.

This can be changed in your `elasticsearch.yml` file:

[source,yaml]
----
cluster.name: elasticsearch_production
----

Similarly, it is wise to change the names of your nodes. As you've probably
noticed by now, Elasticsearch assigns a random Marvel superhero name
to your nodes at startup.  This is cute in development--but less cute when it is
3a.m. and you are trying to remember which physical machine was Tagak the Leopard Lord.

More important, since these names are generated on startup, each time you
restart your node, it will get a new name. This can make logs confusing,
since the names of all the nodes are constantly changing.

Boring as it might be, we recommend you give each node a name that makes sense
to you--a plain, descriptive name.  This is also configured in your `elasticsearch.yml`:

[source,yaml]
----
node.name: elasticsearch_005_data
----


==== Paths

By default, Elasticsearch will place the plug-ins,((("configuration changes, important", "paths")))((("paths"))) logs, and--most important--your data in the installation directory.  This can lead to
unfortunate accidents, whereby the installation directory is accidentally overwritten
by a new installation of Elasticsearch. If you aren't careful, you can erase all your data.

Don't laugh--we've seen it happen more than a few times.

The best thing to do is relocate your data directory outside the installation
location.  You can optionally move your plug-in and log directories as well.

This can be changed as follows:

[source,yaml]
----
path.data: /path/to/data1,/path/to/data2 <1>

# Path to log files:
path.logs: /path/to/logs

# Path to where plugins are installed:
path.plugins: /path/to/plugins
----
<1> Notice that you can specify more than one directory for data by using comma-separated lists.

Data can be saved to multiple directories, and if each directory
is mounted on a different hard drive, this is a simple and effective way to
set up a software RAID 0.  Elasticsearch will automatically stripe
data between the different directories, boosting performance

==== Minimum Master Nodes

The `minimum_master_nodes` setting is _extremely_ important to the
stability of your cluster.((("configuration changes, important", "minimum_master_nodes setting")))((("minimum_master_nodes setting")))  This setting helps prevent _split brains_, the existence of two masters in a single cluster.

When you have a split brain, your cluster is at danger of losing data.  Because
the master is considered the supreme ruler of the cluster, it decides
when new indices can be created, how shards are moved, and so forth.  If you have _two_
masters, data integrity becomes perilous, since you have two nodes
that think they are in charge.

This setting tells Elasticsearch to not elect a master unless there are enough
master-eligible nodes available.  Only then will an election take place.

This setting should always be configured to a quorum (majority) of your master-eligible nodes.((("quorum")))  A quorum is `(number of master-eligible nodes / 2) + 1`.
Here are some examples:

- If you have ten regular nodes (can hold data, can become master), a quorum is
`6`.
- If you have three dedicated master nodes and a hundred data nodes, the quorum is `2`,
since you need to count only nodes that are master eligible.
- If you have two regular nodes, you are in a conundrum.  A quorum would be
`2`, but this means a loss of one node will make your cluster inoperable.  A
setting of `1` will allow your cluster to function, but doesn't protect against
split brain.  It is best to have a minimum of three nodes in situations like this.

This setting can be configured in your `elasticsearch.yml` file:

[source,yaml]
----
discovery.zen.minimum_master_nodes: 2
----

But because Elasticsearch clusters are dynamic, you could easily add or remove
nodes that will change the quorum.  It would be extremely irritating if you had
to push new configurations to each node and restart your whole cluster just to
change the setting.

For this reason, `minimum_master_nodes` (and other settings) can be configured
via a dynamic API call.  You can change the setting while your cluster is online:

[source,js]
----
PUT /_cluster/settings
{
    "persistent" : {
        "discovery.zen.minimum_master_nodes" : 2
    }
}
----

This will become a persistent setting that takes precedence over whatever is
in the static configuration.  You should modify this setting whenever you add or
remove master-eligible nodes.

==== Recovery Settings

Several settings affect the behavior of shard recovery when
your cluster restarts.((("recovery settings")))((("configuration changes, important", "recovery settings")))  First, we need to understand what happens if nothing is
configured.

Imagine you have ten nodes, and each node holds a single shard--either a primary
or a replica--in a 5 primary / 1 replica index.  You take your
entire cluster offline for maintenance (installing new drives, for example).  When you
restart your cluster, it just so happens that five nodes come online before
the other five.

Maybe the switch to the other five is being flaky, and they didn't
receive the restart command right away.  Whatever the reason, you have five nodes
online.  These five nodes will gossip with each other, elect a master, and form a
cluster.  They notice that data is no longer evenly distributed, since five
nodes are missing from the cluster, and immediately start replicating new
shards between each other.

Finally, your other five nodes turn on and join the cluster.  These nodes see
that _their_ data is being replicated to other nodes, so they delete their local
data (since it is now redundant, and may be outdated).  Then the cluster starts
to rebalance even more, since the cluster size just went from five to ten.

During this whole process, your nodes are thrashing the disk and network, moving
data around--for no good reason. For large clusters with terabytes of data,
this useless shuffling of data can take a _really long time_.  If all the nodes
had simply waited for the cluster to come online, all the data would have been
local and nothing would need to move.

Now that we know the problem, we can configure a few settings to alleviate it.
First, we need to give Elasticsearch a hard limit:

[source,yaml]
----
gateway.recover_after_nodes: 8
----

This will prevent Elasticsearch from starting a recovery until at least eight (data or master) nodes
are present.  The value for this setting is a matter of personal preference: how
many nodes do you want present before you consider your cluster functional?
In this case, we are setting it to `8`, which means the cluster is inoperable
unless there are at least eight nodes.

Then we tell Elasticsearch how many nodes _should_ be in the cluster, and how
long we want to wait for all those nodes:

[source,yaml]
----
gateway.expected_nodes: 10
gateway.recover_after_time: 5m
----

What this means is that Elasticsearch will do the following:

- Wait for eight nodes to be present
- Begin recovering after 5 minutes _or_ after ten nodes have joined the cluster,
whichever comes first.

These three settings allow you to avoid the excessive shard swapping that can
occur on cluster restarts.  It can literally make recovery take seconds instead
of hours.

NOTE: These settings can only be set in the `config/elasticsearch.yml` file or on 
the command line (they are not dynamically updatable) and they are only relevant
during a full cluster restart.

==== Prefer Unicast over Multicast

Elasticsearch is configured to use multicast discovery out of the box.  Multicast((("configuration changes, important", "preferring unicast over multicast")))((("unicast, preferring over multicast")))((("multicast versus unicast")))
works by sending UDP pings across your local network to discover nodes.  Other
Elasticsearch nodes will receive these pings and respond.  A cluster is formed
shortly after.

Multicast is excellent for development, since you don't need to do anything.  Turn
a few nodes on, and they automatically find each other and form a cluster.

This ease of use is the exact reason you should disable it in production.  The
last thing you want is for nodes to accidentally join your production network, simply
because they received an errant multicast ping.  There is nothing wrong with
multicast _per se_.  Multicast simply leads to silly problems, and can be a bit
more fragile (for example, a network engineer fiddles with the network without telling
you--and all of a sudden nodes can't find each other anymore).

In production, it is recommended to use unicast instead of multicast.  This works
by providing Elasticsearch a list of nodes that it should try to contact.  Once
the node contacts a member of the unicast list, it will receive a full cluster
state that lists all nodes in the cluster.  It will then proceed to contact
the master and join.

This means your unicast list does not need to hold all the nodes in your cluster.
It just needs enough nodes that a new node can find someone to talk to.  If you
use dedicated masters, just list your three dedicated masters and call it a day.
This setting is configured in your `elasticsearch.yml`:

[source,yaml]
----
discovery.zen.ping.multicast.enabled: false <1>
discovery.zen.ping.unicast.hosts: ["host1", "host2:port"]
----
<1> Make sure you disable multicast, since it can operate in parallel with unicast.










