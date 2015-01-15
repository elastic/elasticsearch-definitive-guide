
=== Clusters Are Living, Breathing Creatures

Once you get a cluster into production, you'll find that it takes on a life of its
own.  ((("clusters", "maintaining")))((("post-deployment", "clusters, rolling restarts and upgrades")))Elasticsearch works hard to make clusters self-sufficient and _just work_.
But a cluster still requires routine care and feeding, such as routine backups 
and upgrades.

Elasticsearch releases new versions with bug fixes and performance enhancements at 
a very fast pace, and it is always a good idea to keep your cluster current.
Similarly, Lucene continues to find new and exciting bugs in the JVM itself, which
means you should always try to keep your JVM up-to-date.

This means it is a good idea to have a standardized, routine way to perform rolling
restarts and upgrades in your cluster.  Upgrading should be a routine process, 
rather than a once-yearly fiasco that requires countless hours of precise planning.

Similarly, it is important to have disaster recovery plans in place.  Take frequent
snapshots of your cluster--and periodically _test_ those snapshots by performing
a real recovery!  It is all too common for organizations to make routine backups but
never test their recovery strategy.  Often you'll find a glaring deficiency
the first time you perform a real recovery (such as users being unaware of which
drive to mount).  It's better to work these bugs out of your process with 
routine testing, rather than at 3 a.m. when there is a crisis.
