=== Installing Elasticsearch

The easiest way to understand what Elasticsearch can do for you is to
play with it, so let's get started!((("Elasticsearch", "installing")))

The only requirement for installing Elasticsearch is a recent version of Java.
Preferably, you should install the latest version of the((("Java", "installing"))) official Java
from http://www.java.com[_www.java.com_].

You can download the latest version of Elasticsearch from
http://www.elasticsearch.org/download/[_elasticsearch.org/download_].

[source,sh]
--------------------------------------------------
curl -L -O http://download.elasticsearch.org/PATH/TO/VERSION.zip <1>
unzip elasticsearch-$VERSION.zip
cd  elasticsearch-$VERSION
--------------------------------------------------
<1> Fill in the URL for the latest version available on
    http://www.elasticsearch.org/download/[_elasticsearch.org/download_].

[TIP]
====
When installing Elasticsearch in production, you can use the method
described previously, or the Debian or RPM packages provided on the
http://www.elasticsearch.org/downloads[downloads page]. You can also use
the officially supported
https://github.com/elasticsearch/puppet-elasticsearch[Puppet module] or
https://github.com/elasticsearch/cookbook-elasticsearch[Chef cookbook].
====

[[marvel]]
==== Installing Marvel

http://www.elasticsearch.com/products/marvel[Marvel] is a management((("Marvel", "defined"))) and monitoring
tool for Elasticsearch, which is free for development use. It comes with an
interactive console called Sense,((("Sense console (Marvel plugin)"))) which makes it easy to talk to
Elasticsearch directly from your browser.

Many of the code examples in the online version of this book include a View in Sense link. When
clicked, it will open up a working example of the code in the Sense console.
You do not have to install Marvel, but it will make this book much more
interactive by allowing you to  experiment with the code samples on your local
Elasticsearch cluster.

Marvel is available as a plug-in.((("Marvel", "downloading and installing"))) To download and install it, run this command
in the Elasticsearch directory:

[source,sh]
--------------------------------------------------
./bin/plugin -i elasticsearch/marvel/latest
--------------------------------------------------

You probably don't want Marvel to monitor your local cluster, so you can
disable data collection with this command:

[source,sh]
--------------------------------------------------
echo 'marvel.agent.enabled: false' >> ./config/elasticsearch.yml
--------------------------------------------------

[[running-elasticsearch]]
=== Running Elasticsearch

Elasticsearch is now ready to run. ((("Elasticsearch", "running")))You can start it up in the foreground
with this:

[source,sh]
--------------------------------------------------
./bin/elasticsearch
--------------------------------------------------
Add `-d` if you want to run it in the background as a daemon.

Test it out by opening another terminal window and running the following:

[source,sh]
--------------------------------------------------
curl 'http://localhost:9200/?pretty'
--------------------------------------------------


You should see a response like this:

[source,js]
--------------------------------------------------
{
   "status": 200,
   "name": "Shrunken Bones",
   "version": {
      "number": "1.4.0",
      "lucene_version": "4.10"
   },
   "tagline": "You Know, for Search"
}
--------------------------------------------------
// SENSE: 010_Intro/10_Info.json

This means that your Elasticsearch _cluster_ is up and running, and we can
start experimenting with it.

NOTE: A _node_ is a running instance of Elasticsearch.((("nodes", "defined"))) A _cluster_ is ((("clusters", "defined")))a group of
nodes with the same `cluster.name` that are working together to share data
and to provide failover and scale, although a single node can form a cluster
all by itself.

You should change the default `cluster.name` to something appropriate to you,
like your own name, to stop ((("clusters", "changing default name")))your nodes from trying to join another cluster on
the same network with the same name!

You can do this by editing the `elasticsearch.yml` file in the `config/`
directory and then restarting Elasticsearch.  When Elasticsearch is running in
the foreground, you can stop it by pressing Ctrl-C; otherwise, you can shut
it down with the `shutdown` API:

[source,sh]
--------------------------------------------------
curl -XPOST 'http://localhost:9200/_shutdown'
--------------------------------------------------


==== Viewing Marvel and Sense

If you installed the <<marvel,Marvel>> management ((("Marvel", "viewing")))and monitoring tool, you can
view it in a web browser by visiting
http://localhost:9200/_plugin/marvel/.

You can reach the _Sense_ developer((("Sense console (Marvel plugin)", "viewing"))) console either by clicking the ``Marvel
dashboards'' drop-down in Marvel, or by visiting
http://localhost:9200/_plugin/marvel/sense/.
