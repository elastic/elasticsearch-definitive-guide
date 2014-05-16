
=== What about Facets?

If you've used Elasticsearch in the past, you are probably aware of _facets_.
You can think of Aggregations as "facets on steroids".  Everything you can do
with facets, you can do with aggregations.

But there are plenty of operations that are possible in aggregations which are
simply impossible with facets.

Facets have not been officially depreciated yet, but you can expect that to
happen eventually. We recommend migrating your facets over to aggregations when
you get the chance, and starting all new projects with aggregations instead of facets.