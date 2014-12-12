[[synonym-formats]]
=== Formatting Synonyms

In their simplest form, synonyms are((("synonyms", "formatting"))) listed as comma-separated values:

    "jump,leap,hop"

If any of these terms is encountered, it is replaced by all of the listed
synonyms.  For instance:

[role="pagebreak-before"]
[source,text]
--------------------------
Original terms:   Replaced by:
────────────────────────────────
jump            → (jump,leap,hop)
leap            → (jump,leap,hop)
hop             → (jump,leap,hop)
--------------------------

Alternatively, with the `=>` syntax, it is possible to specify a list of terms
to match (on the left side), and a list of one or more replacements (on
the right side):

    "u s a,united states,united states of america => usa"
    "g b,gb,great britain => britain,england,scotland,wales"

[source,text]
--------------------------
Original terms:   Replaced by:
────────────────────────────────
u s a           → (usa)
united states   → (usa)
great britain   → (britain,england,scotland,wales)
--------------------------

If multiple rules for the same synonyms are specified, they are merged
together.  The order of rules is not respected.  Instead, the longest matching
rule wins.  Take the following rules as an example:

    "united states            => usa",
    "united states of america => usa"

If these rules conflicted, Elasticsearch would turn `United States of
America` into the terms `(usa),(of),(america)`.  Instead, the longest
sequence wins, and we end up with just the term `(usa)`.

