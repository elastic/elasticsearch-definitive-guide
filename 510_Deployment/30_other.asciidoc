
=== Java Virtual Machine

You should always run the most recent version of the Java Virtual Machine (JVM),
unless otherwise stated on the Elasticsearch website.((("deployment", "Java Virtual Machine (JVM)")))((("JVM (Java Virtual Machine)")))((("Java Virtual Machine", see="JVM")))  Elasticsearch, and in
particular Lucene, is a demanding piece of software.  The unit and integration
tests from Lucene often expose bugs in the JVM itself.  These bugs range from
mild annoyances to serious segfaults, so it is best to use the latest version
of the JVM where possible.

Java 7 is strongly preferred over Java 6.  Either Oracle or OpenJDK are acceptable. They are comparable in performance and stability.

If your application is written in Java and you are using the transport client
or node client, make sure the JVM running your application is identical to the
server JVM.  In few locations in Elasticsearch, Java's native serialization
is used (IP addresses, exceptions, and so forth).  Unfortunately, Oracle has been known to
change the serialization format between minor releases, leading to strange errors.
This happens rarely, but it is best practice to keep the JVM versions identical
between client and server.

.Please Do Not Tweak JVM Settings
****
The JVM exposes dozens (hundreds even!) of settings, parameters, and configurations.((("JVM (Java Virtual Machine)", "avoiding custom configuration")))
They allow you to tweak and tune almost every aspect of the JVM.

When a knob is encountered, it is human nature to want to turn it.  We implore
you to squash this desire and _not_ use custom JVM settings.  Elasticsearch is
a complex piece of software, and the current JVM settings have been tuned
over years of real-world usage.

It is easy to start turning knobs, producing opaque effects that are hard to measure,
and eventually detune your cluster into a slow, unstable mess.  When debugging
clusters, the first step is often to remove all custom configurations.  About
half the time, this alone restores stability and performance.
****

=== Transport Client Versus Node Client

If you are using Java, you may wonder when to use the transport client versus the
node client.((("Java", "clients for Elasticsearch")))((("clients")))((("node client", "versus transport client")))((("transport client", "versus node client")))  As discussed at the beginning of the book, the transport client
acts as a communication layer between the cluster and your application.  It knows
the API and can automatically round-robin between nodes, sniff the cluster for you,
and more. But it is _external_ to the cluster, similar to the REST clients.

The node client, on the other hand, is actually a node within the cluster (but
does not hold data, and cannot become master).  Because it is a node, it knows
the entire cluster state (where all the nodes reside, which shards live in which
nodes, and so forth). This means it can execute APIs with one less network hop.

There are uses-cases for both clients:

- The transport client is ideal if you want to decouple your application from the
cluster.  For example, if your application quickly creates and destroys
connections to the cluster, a transport client is much "lighter" than a node client,
since it is not part of a cluster.
+
Similarly, if you need to create thousands of connections, you don't want to
have thousands of node clients join the cluster.  The TC will be a better choice.

- On the flipside, if you need only a few long-lived, persistent connection
objects to the cluster, a node client can be a bit more efficient since it knows
the cluster layout.  But it ties your application into the cluster, so it may
pose problems from a firewall perspective.

=== Configuration Management

If you use configuration management already (Puppet, Chef, Ansible), you can skip this tip.((("deployment", "configuration management")))((("configuration management")))

If you don't use configuration management tools yet, you should!  Managing
a handful of servers by `parallel-ssh` may work now, but it will become a nightmare
as you grow your cluster.  It is almost impossible to edit 30 configuration files
by hand without making a mistake.

Configuration management tools help make your cluster consistent by automating
the process of config changes.  It may take a little time to set up and learn,
but it will pay itself off handsomely over time.


