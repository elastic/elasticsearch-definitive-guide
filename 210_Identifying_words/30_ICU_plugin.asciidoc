[[icu-plugin]]
=== Installing the ICU Plug-in

The https://github.com/elasticsearch/elasticsearch-analysis-icu[ICU analysis
plug-in]  for Elasticsearch uses the _International Components for Unicode_
(ICU) libraries  (see http://site.icu-project.org[site.project.org]) to
provide a rich set of tools for dealing with Unicode.((("International Components for Unicode libraries", see="ICU plugin, installing")))((("words", "identifying", "installing ICU plugin")))((("ICU plugin, installing"))) These include the
`icu_tokenizer`, which is particularly useful for Asian languages,((("Asian languages", "icu_tokenizer for"))) and a number
of token filters that are essential for correct matching and sorting in all
languages other than English.

[NOTE]
==================================================

The ICU plug-in is an essential tool for dealing with languages other than
English, and it is highly recommended that you install and use it.
Unfortunately, because it is based on the external ICU libraries, different
versions of the ICU plug-in may not be compatible with previous versions.  When
upgrading, you may need to reindex your data.

==================================================

To install the plug-in, first shut down your Elasticsearch node  and then run the
following command from the Elasticsearch home directory:

[source,sh]
--------------------------------------------------
./bin/plugin -install elasticsearch/elasticsearch-analysis-icu/$VERSION <1>
--------------------------------------------------

<1> The current `$VERSION` can be found at
    _https://github.com/elasticsearch/elasticsearch-analysis-icu_.

Once installed, restart Elasticsearch, and you should see a line similar to the
following in the startup logs:

    [INFO][plugins] [Mysterio] loaded [marvel, analysis-icu], sites [marvel]

If you are running a cluster with multiple nodes, you will need to install the
plug-in on every node in the cluster.
