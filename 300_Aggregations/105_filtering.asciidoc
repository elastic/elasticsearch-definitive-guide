
=== Fielddata Filtering

Imagine that you are running a website that allows users to listen to their
favorite songs.((("fielddata", "filtering")))((("aggregations", "fielddata", "filtering")))  To make it easier for them to manage their music library,
users can tag songs with whatever tags make sense to them.  You will end up
with a lot of tracks tagged with `rock`, `hiphop`, and `electronica`, but
also with some tracks tagged with `my_16th_birthday_favorite_anthem`.

Now imagine that you want to show users the most popular three tags for each
song.  It is highly likely that tags like `rock` will show up in the top
three, but `my_16th_birthday_favorite_anthem` is very unlikely to make the
grade.  However, in order to calculate the most popular tags, you have been
forced to load all of these one-off terms into memory.

Thanks to fielddata filtering, we can take control of this situation.  We
_know_ that we're interested in only the most popular terms, so we can simply
avoid loading any terms that fall into the less interesting long tail:

[source,js]
----
PUT /music/_mapping/song
{
  "properties": {
    "tag": {
      "type": "string",
      "fielddata": { <1>
        "filter": {
          "frequency": { <2>
            "min":              0.01, <3>
            "min_segment_size": 500  <4>
          }
        }
      }
    }
  }
}
----
<1> The `fielddata` key allows us to configure how fielddata is handled for this field.
<2> The `frequency` filter allows us to filter fielddata loading based on term frequencies.((("term frequency", "fielddata filtering based on")))
<3> Load only terms that occur in at least 1% of documents in this segment.
<4> Ignore any segments that have fewer than 500 documents.

With this mapping in place, only terms that appear in at least 1% of the
documents _in that segment_ will be loaded into memory. You can also specify a
`max` term frequency, which could be used to exclude terms that are _too_
common, such as <<stopwords,stopwords>>.

Term frequencies, in this case, are calculated per segment.  This is a
limitation of the implementation: fielddata is loaded per segment, and at
that point the only term frequencies that are visible are the frequencies for
that segment.  However, this limitation has interesting properties: it
allows newly popular terms to rise to the top quickly.

Let's say that a new genre of song becomes popular one day.  You would like to
include the tag for this new genre in the most popular list, but if you were
relying on term frequencies calculated across the whole index, you would have
to wait for the new tag to become as popular as `rock` and `electronica`.
Because of the way frequency filtering is implemented, the newly added tag
will quickly show up as a high-frequency tag within new segments, so will
quickly float to the top.

The `min_segment_size` parameter tells Elasticsearch to ignore segments below
a certain size.((("min_segment_size parameter")))  If a segment holds only a few documents, the term frequencies
are too coarse to have any meaning.  Small segments will soon be merged into
bigger segments, which will then be big enough to take into account.

[TIP]
====
Filtering terms by frequency is not the only option. You can also decide to
load only those terms that match a regular expression.  For instance, you
could use a `regex` filter ((("regex filtering")))on tweets to load only hashtags into memory --
terms the start with a `#`.  This assumes that you are using an analyzer that
preserves punctuation, like the `whitespace` analyzer.
====

Fielddata filtering can have a _massive_ impact on memory usage.  The
trade-off is fairly obvious: you are essentially ignoring data.  But for many
applications, the trade-off is reasonable since the data is not being used
anyway.  The memory savings is often more important than including a large and
relatively useless long tail of terms.

