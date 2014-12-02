[[geo-shapes]]
== Geo-shapes

Geo-shapes use a completely different approach than geo-points.((("geo-shapes"))) A circle on a
computer screen does not consist of a perfect continuous line. Instead it is
drawn by coloring adjacent pixels as an approximation of a circle. Geo-shapes
work in much the same way.

Complex shapes--such as points, lines, polygons, multipolygons, and polygons with
holes,--are ``painted'' onto a grid of geohash cells, and the shape is
converted into a list of the ((("geohashes", "in geo-shapes")))geohashes of all the cells that it touches.

[NOTE]
====
Actually, two types of grids can be used with geo-shapes:
geohashes, which we have already discussed and which are the default encoding,
and _quad trees_.  ((("quad trees")))Quad trees are similar to geohashes except that there are
only four cells at each level, instead of 32.  The difference comes down to a
choice of encoding.
====

All of the geohashes that compose a shape are indexed as if they were terms.
With this information in the index, it is easy to determine whether one shape
intersects with another, as they will share the same geohash terms.

That is the extent of what you can do with geo-shapes: determine the
relationship between a query shape and a shape in the index.  The `relation`
can be ((("relation parameter (geo-shapes)")))one of the following:

`intersects`::

    The query shape overlaps with the indexed shape (default).

`disjoint`::

    The query shape does _not_ overlap at all with the indexed shape.

`within`::

    The indexed shape is entirely within the query shape.

Geo-shapes cannot be used to caculate distance, cannot be used for
sorting or scoring, and cannot be used in aggregations.

