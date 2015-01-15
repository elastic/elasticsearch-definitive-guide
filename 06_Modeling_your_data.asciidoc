ifndef::es_build[= placeholder6]

[[modeling-your-data]]

= Modeling Your Data

[partintro]
--

Elasticsearch is a different kind of beast, especially if you come from the
world of SQL.((("modeling your data")))  It comes with many benefits: performance, scale, near real-time
search, and analytics across massive amounts of data. And it is easy to get
going! Just download and start using it.

But it is not magic.  To get the most out of Elasticsearch, you need to
understand how it works and how to make it work for your needs.

Handling relationships between entities is not as obvious as it is with a
dedicated relational store.  The golden rule of a relational database--normalize your data--does not apply to Elasticsearch. In <<relations>>,
<<nested-objects>>, and <<parent-child>> we discuss the pros and cons of
the available approaches.

Then in <<scale>> we talk about the features that Elasticsearch offers
that enable you to scale out quickly and flexibly.  Scale is not  one-size-fits-all.  You need to think about how data flows through your system, and
design your model accordingly. Time-based data like log events or social
network streams require a very different approach than more static collections
of documents.

And finally, we talk about the one thing in Elasticsearch that doesn't scale.

--

include::400_Relationships.asciidoc[]

include::402_Nested.asciidoc[]

include::404_Parent_Child.asciidoc[]

include::410_Scaling.asciidoc[]


