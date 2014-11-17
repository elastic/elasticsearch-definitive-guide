[[index-management]]
== Index Management

We have seen how Elasticsearch makes it easy to start developing a new
application without requiring any advance planning or setup.  However, it
doesn't take long before you start wanting to fine-tune the indexing and
search process to better suit your particular use case. Almost all of these customizations relate to the index, and the types
that it contains.  In this chapter, we introduce the APIs
for managing indices and type mappings, and the most important settings.

include::070_Index_Mgmt/05_Create_Delete.asciidoc[]

include::070_Index_Mgmt/10_Settings.asciidoc[]

include::070_Index_Mgmt/15_Configure_Analyzer.asciidoc[]

include::070_Index_Mgmt/20_Custom_Analyzers.asciidoc[]

include::070_Index_Mgmt/25_Mappings.asciidoc[]

include::070_Index_Mgmt/30_Root_Object.asciidoc[]

include::070_Index_Mgmt/35_Dynamic_Mapping.asciidoc[]

include::070_Index_Mgmt/40_Custom_Dynamic_Mapping.asciidoc[]

include::070_Index_Mgmt/45_Default_Mapping.asciidoc[]

include::070_Index_Mgmt/50_Reindexing.asciidoc[]

include::070_Index_Mgmt/55_Aliases.asciidoc[]
