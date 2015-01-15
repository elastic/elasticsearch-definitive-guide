[[denormalization-concurrency]]
=== Denormalization and Concurrency

Of course, data denormalization has downsides too.((("relationships", "denormalization and concurrency")))((("concurrency", "denormalization and")))((("denormalization", "and concurrency")))  The first disadvantage is
that  the index will be bigger because the `_source` document for every
blog post is bigger, and there are more indexed fields.  This usually isn't a
huge problem.  The data written to disk is highly compressed, and disk space
is cheap. Elasticsearch can happily cope with the extra data.

The more important issue is that, if the user were to change his name, all
of his blog posts would need to be updated too. Fortunately, users don't
often change names.  Even if they did, it is unlikely that a user would have
written more than a few thousand blog posts, so updating blog posts with
the <<scan-scroll,`scroll`>> and <<bulk,`bulk`>> APIs would take less than a
second.

However, let's consider a more complex scenario in which changes are common, far
reaching, and, most important, concurrent.((("files", "searching for files in a particular directory")))

In this example, we are going to emulate a filesystem with directory trees in
Elasticsearch, much like a filesystem on Linux: the root of the directory is
`/`, and each directory can contain files and subdirectories.

We want to be able to search for files that live in a particular directory,
the equivalent of this:

    grep "some text" /clinton/projects/elasticsearch/*

This requires us to index the path of the directory where the file lives:

[source,json]
--------------------------
PUT /fs/file/1
{
  "name":     "README.txt", <1>
  "path":     "/clinton/projects/elasticsearch", <2>
  "contents": "Starting a new Elasticsearch project is easy..."
}
--------------------------
<1> The filename
<2> The full path to the directory holding the file

[NOTE]
==================================================

Really, we should also index `directory` documents so we can list all
files and subdirectories within a directory, but for brevity's sake, we will
ignore that requirement.

==================================================

We also want to be able to search for files that live anywhere in the
directory tree below a particular directory, the equivalent of this:

    grep -r "some text" /clinton

To support this, we need to index the path hierarchy:

* `/clinton`
* `/clinton/projects`
* `/clinton/projects/elasticsearch`

This hierarchy can be generated ((("path_hierarchy tokenizer")))automatically from the `path` field using the
http://bit.ly/1AjGltZ[`path_hierarchy` tokenizer]:

[source,json]
--------------------------
PUT /fs
{
  "settings": {
    "analysis": {
      "analyzer": {
        "paths": { <1>
          "tokenizer": "path_hierarchy"
        }
      }
    }
  }
}
--------------------------
<1> The custom `paths` analyzer uses the `path_hierarchy` tokenizer with its
    default settings. See http://bit.ly/1AjGltZ[`path_hierarchy` tokenizer].

The mapping for the `file` type would look like this:

[source,json]
--------------------------
PUT /fs/_mapping/file
{
  "properties": {
    "name": { <1>
      "type":  "string",
      "index": "not_analyzed"
    },
    "path": { <2>
      "type":  "string",
      "index": "not_analyzed",
      "fields": {
        "tree": { <2>
          "type":     "string",
          "analyzer": "paths"
        }
      }
    }
  }
}
--------------------------
<1> The `name` field will contain the exact name.
<2> The `path` field will contain the exact directory name, while the `path.tree`
    field will contain the path hierarchy.

Once the index is set up and the files have been indexed, we can perform a
search for files containing `elasticsearch` in just the
`/clinton/projects/elasticsearch` directory like this:

[source,json]
--------------------------
GET /fs/file/_search
{
  "query": {
    "filtered": {
      "query": {
        "match": {
          "contents": "elasticsearch"
        }
      },
      "filter": {
        "term": { <1>
          "path": "/clinton/projects/elasticsearch"
        }
      }
    }
  }
}
--------------------------
<1> Find files in this directory only.

Every file that lives in any subdirectory under `/clinton` will include the
term `/clinton` in the `path.tree` field.  So we can search for all files in
any subdirectory of `/clinton` as follows:

[source,json]
--------------------------
GET /fs/file/_search
{
  "query": {
    "filtered": {
      "query": {
        "match": {
          "contents": "elasticsearch"
        }
      },
      "filter": {
        "term": { <1>
          "path.tree": "/clinton"
        }
      }
    }
  }
}
--------------------------
<1> Find files in this directory or in any of its subdirectories.

==== Renaming Files and Directories

So far, so good.((("optimistic concurrency control")))((("files", "renaming files and directories")))  Renaming a file is easy--a simple `update` or `index`
request is all that is required.  You can even use
<<optimistic-concurrency-control,optimistic concurrency control>> to
ensure that your change doesn't conflict with the changes from another user:

[source,json]
--------------------------
PUT /fs/file/1?version=2 <1>
{
  "name":     "README.asciidoc",
  "path":     "/clinton/projects/elasticsearch",
  "contents": "Starting a new Elasticsearch project is easy..."
}
--------------------------
<1> The `version` number ensures that the change is applied only if the
    document in the index has this same version number.

We can even rename a directory, but this means updating all of the files that
exist anywhere in the path hierarchy beneath that directory.  This may be
quick or slow, depending on how many files need to be updated.  All we would
need to do is to use <<scan-scroll,scan-and-scroll>> to retrieve all the
files, and the <<bulk,`bulk` API>> to update them.  The process isn't
atomic, but all files will quickly move to their new home.

