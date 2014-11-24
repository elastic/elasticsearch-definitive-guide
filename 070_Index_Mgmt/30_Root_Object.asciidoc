[[root-object]]
=== The Root Object

The uppermost level of a mapping is known ((("mapping (types)", "root object")))((("root object")))as the _root object_. It may
contain the following:

* A _properties_ section, which lists the mapping for each field that a
  document may contain

* Various metadata fields, all of which start with an underscore, such
  as `_type`, `_id`, and `_source`

* Settings, which control how the dynamic detection of new fields
  is handled, such as `analyzer`, `dynamic_date_formats`, and
  `dynamic_templates`

* Other settings, which can be applied both to the root object and to fields
  of type `object`, such as `enabled`, `dynamic`, and `include_in_all`

==== Properties

We have already discussed the three most important settings for document
fields or ((("root object", "properties")))((("properties", "important settings")))properties in <<core-fields>> and <<complex-core-fields>>:

 `type`::
   The datatype that the field contains, such as `string` or `date`

 `index`::      
   Whether a field should be searchable as full text (`analyzed`), searchable as an exact value (`not_analyzed`), or not searchable at all (`no`)

 `analyzer`::    
   Which `analyzer` to use for a full-text field, both at index time and at search time

We will discuss other field types such as `ip`, `geo_point`, and `geo_shape` in
the appropriate sections later in the book.

include::31_Metadata_source.asciidoc[]

include::32_Metadata_all.asciidoc[]

include::33_Metadata_ID.asciidoc[]
