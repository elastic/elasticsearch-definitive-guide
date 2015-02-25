ifndef::es_build[= placeholder7]


[[administration]]
= Administration, Monitoring, and Deployment

[partintro]
--
The majority of this book is aimed at building applications by using Elasticsearch
as the backend.  This section is a little different.  Here, you will learn
how to manage Elasticsearch itself.  Elasticsearch is a complex piece of
software, with many moving parts.  Many APIs are designed
to help you manage your Elasticsearch deployment.

In this chapter, we cover three main topics:

- Monitoring your cluster's vital statistics, understanding which behaviors are normal and which
should be cause for alarm, and interpreting various stats provided by Elasticsearch
- Deploying your cluster to production, including best practices and important
configuration that should (or should not!) be changed
- Performing post-deployment logistics, such as a rolling restart or backup of
your cluster
--

include::500_Cluster_Admin.asciidoc[]

include::510_Deployment.asciidoc[]

include::520_Post_Deployment.asciidoc[]


