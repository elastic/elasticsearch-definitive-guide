[[geohashes]]
== Geohashes

http://en.wikipedia.org/wiki/Geohash[Geohashes] are a way of encoding
`lat/lon` points as strings.((("geohashes")))((("latitude/longitude pairs", "encoding lat/lon points as strings with geohashes")))((("strings", "geohash")))  The original intention was to have a
URL-friendly way of specifying geolocations, but geohashes have turned out to
be a useful way of indexing geo-points and geo-shapes in databases.

Geohashes divide the world into a grid of 32 cells--4 rows and 8 columns--each represented by a letter or number.  The `g` cell covers half of
Greenland, all of Iceland, and most of Great Britian. Each cell can be further
divided into another 32 cells, which can be divided into another 32 cells,
and so on.  The `gc` cell covers Ireland and England, `gcp` covers most of
London and part of Southern England, and `gcpuuz94k` is the entrance to
Buckingham Palace, accurate to about 5 meters.

In other words, the longer the geohash string, the more accurate it is.  If
two geohashes share a prefix&#x2014; and `gcpuuz`&#x2014;then it implies that
they are near each other.  The longer the shared prefix, the closer they
are.

That said, two locations that are right next to each other may have completely
different geohashes. For instance, the
http://en.wikipedia.org/wiki/Millennium_Dome[Millenium Dome] in London has
geohash `u10hbp`, because it falls into the `u` cell, the next top-level cell
to the east of the `g` cell.

Geo-points can index their associated geohashes automatically, but more
important, they can also index all geohash _prefixes_. Indexing the location
of the entrance to Buckingham Palace--latitude `51.501568` and longitude
`-0.141257`&#x2014;would index all of the geohashes listed in the following table,
along with  the approximate dimensions of each geohash cell:

[cols="1m,1m,3d",options="header"]
|=============================================
|Geohash        |Level| Dimensions
|g              |1    | ~ 5,004km x 5,004km
|gc             |2    | ~ 1,251km x 625km
|gcp            |3    | ~ 156km x 156km
|gcpu           |4    | ~ 39km x 19.5km
|gcpuu          |5    | ~ 4.9km x 4.9km
|gcpuuz         |6    | ~ 1.2km x 0.61km
|gcpuuz9        |7    | ~ 152.8m x 152.8m
|gcpuuz94       |8    | ~ 38.2m x 19.1m
|gcpuuz94k      |9    | ~ 4.78m x 4.78m
|gcpuuz94kk     |10   | ~ 1.19m x 0.60m
|gcpuuz94kkp    |11   | ~ 14.9cm x 14.9cm
|gcpuuz94kkp5   |12   | ~ 3.7cm x 1.8cm
|=============================================

The http://bit.ly/1DIqyex[`geohash_cell` filter] can use
these geohash prefixes((("geohash_cell filter")))((("filters", "geohash_cell"))) to find locations near a specified `lat/lon` point.

