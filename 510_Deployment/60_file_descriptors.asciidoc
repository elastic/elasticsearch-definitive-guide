
=== File Descriptors and MMap 

Lucene uses a _very_ large number of files. ((("deployment", "file descriptors and MMap"))) At the same time, Elasticsearch
uses a large number of sockets to communicate between nodes and HTTP clients.
All of this requires available file descriptors.((("file descriptors")))

Sadly, many modern Linux distributions ship with a paltry 1,024 file descriptors
allowed per process.  This is _far_ too low for even a small Elasticsearch
node, let alone one that is handling hundreds of indices.

You should increase your file descriptor count to something very large, such as
64,000.  This process is irritatingly difficult and highly dependent on your
particular OS and distribution.  Consult the documentation for your OS to determine
how best to change the allowed file descriptor count.

Once you think you've changed it, check Elasticsearch to make sure it really does
have enough file descriptors:

[source,js]
----
GET /_nodes/process

{
   "cluster_name": "elasticsearch__zach",
   "nodes": {
      "TGn9iO2_QQKb0kavcLbnDw": {
         "name": "Zach",
         "transport_address": "inet[/192.168.1.131:9300]",
         "host": "zacharys-air",
         "ip": "192.168.1.131",
         "version": "2.0.0-SNAPSHOT",
         "build": "612f461",
         "http_address": "inet[/192.168.1.131:9200]",
         "process": {
            "refresh_interval_in_millis": 1000,
            "id": 19808,
            "max_file_descriptors": 64000, <1>
            "mlockall": true
         }
      }
   }
}
----
<1> The `max_file_descriptors` field shows the number of available descriptors that
the Elasticsearch process can access.

Elasticsearch also uses a mix of NioFS and MMapFS ((("MMapFS")))for the various files.  Ensure
that you configure the maximum map count so that there is ample virtual memory available for 
mmapped files.  This can be set temporarily:

[source,js]
----
sysctl -w vm.max_map_count=262144
----

Or you can set it permanently by modifying `vm.max_map_count` setting in your `/etc/sysctl.conf`.




