[[concurrency-solutions]]
=== Solving Concurrency Issues

The problem comes when we want to allow more than one person to rename files
or directories _at the same time_. ((("concurrency", "solving concurrency issues")))((("relationships", "solving concurrency issues"))) Imagine that you rename the `/clinton`
directory, which contains hundreds of thousands of files.  Meanwhile, another
user renames the single file `/clinton/projects/elasticsearch/README.txt`.
That user's change, although it started after yours, will probably finish more
quickly.

One of two things will happen:

*   You have decided to use `version` numbers, in which case your mass rename
    will fail with a version conflict when it hits the renamed
    `README.asciidoc` file.

*   You didn't use versioning, and your changes will overwrite the changes from
    the other user.

The problem is that Elasticsearch does not support
http://en.wikipedia.org/wiki/ACID_transactions[ACID transactions].((("ACID transactions")))  Changes to
individual documents are ACIDic, but not changes involving multiple documents.

If your main data store is a relational database, and Elasticsearch is simply
being used as a search engine((("relational databases", "Elasticsearch used with"))) or as a way to improve performance, make
your changes in the database first and replicate those changes to
Elasticsearch after they have succeeded. This way, you benefit from the ACID
transactions available in the database, and all changes to Elasticsearch happen
in the right order. Concurrency is dealt with in the relational database.

If you are not using a relational store, these concurrency issues need to
be dealt with at the Elasticsearch level.  The following are three practical
solutions using Elasticsearch, all of which involve some form of locking:

* Global Locking
* Document Locking
* Tree Locking

[TIP]
==================================================

The solutions described in this section could also be implemented by applying the same
principles while using an external system instead of Elasticsearch.

==================================================

[[global-lock]]
==== Global Locking

We can avoid concurrency issues completely by allowing only one process to
make changes at any time.((("locking", "global lock")))((("global lock")))  Most changes will involve only a few files and will
complete very quickly.  A rename of a top-level directory may block all other
changes for longer, but these are likely to be much less frequent.

Because document-level changes in Elasticsearch are ACIDic, we can use the
existence or absence of a document as a global lock.  To request a
lock, we try to `create` the global-lock document:

[source,json]
--------------------------
PUT /fs/lock/global/_create
{}
--------------------------

If this `create` request fails with a conflict exception,
another process has already been granted the global lock and we will have to
try again later.  If it succeeds, we are now the proud owners of the
global lock and we can continue with our changes.  Once we are finished, we
must release the lock by deleting the global lock document:

[source,json]
--------------------------
DELETE /fs/lock/global
--------------------------

Depending on how frequent changes are, and how long they take, a global lock
could restrict the performance of a system significantly.  We can increase
parallelism by making our locking more fine-grained.

[[document-locking]]
==== Document Locking

Instead of locking the whole filesystem, we could lock individual documents
by using the same technique as previously described.((("locking", "document locking")))((("document locking")))  A process could use a
<<scan-scroll,scan-and-scroll>> request to retrieve the IDs of all documents
that would be affected by the change, and would need to create a lock file for
each of them:

[source,json]
--------------------------
PUT /fs/lock/_bulk
{ "create": { "_id": 1}} <1>
{ "process_id": 123    } <2>
{ "create": { "_id": 2}}
{ "process_id": 123    }
...
--------------------------
<1> The ID of the `lock` document would be the same as the ID of  the file
    that should be locked.
<2> The `process_id` is a unique ID that represents the process that
    wants to perform the changes.

If some files are already locked, parts of the `bulk` request will fail and we
will have to try again.

Of course, if we try to lock _all_ of the files again, the `create` statements
that we used previously will fail for any file that is already locked by us!
Instead of a simple `create` statement, we need an `update` request with an
`upsert` parameter and this `script`:

[source,groovy]
--------------------------
if ( ctx._source.process_id != process_id ) { <1>
  assert false;  <2>
}
ctx.op = 'noop'; <3>
--------------------------
<1> `process_id` is a parameter that we pass into the script.
<2> `assert false` will throw an exception, causing the update to fail.
<3> Changing the `op` from `update` to `noop` prevents the update request
    from making any changes, but still returns success.

The full `update` request looks like this:

[source,json]
--------------------------
POST /fs/lock/1/_update
{
  "upsert": { "process_id": 123 },
  "script": "if ( ctx._source.process_id != process_id ) 
  { assert false }; ctx.op = 'noop';"
  "params": {
    "process_id": 123
  }
}
--------------------------

If the document doesn't already exist, the `upsert` document will be inserted--much the same as the `create` request we used previously.  However, if the
document _does_ exist, the script will look at the `process_id` stored in the
document.  If it is the same as ours, it aborts the update (`noop`) and
returns success.  If it is different, the `assert false` throws an exception
and we know that the lock has failed.

Once all locks have been successfully created, the rename operation can begin.
Afterward, we must release((("delete-by-query request"))) all of the locks, which we can do with a
`delete-by-query` request:

[source,json]
--------------------------
POST /fs/_refresh <1>

DELETE /fs/lock/_query
{
  "query": {
    "term": {
      "process_id": 123
    }
  }
}
--------------------------
<1> The `refresh` call ensures that all `lock` documents are visible to
    the `delete-by-query` request.

Document-level locking enables fine-grained access control, but creating lock
files for millions of documents can be expensive.  In certain scenarios, such
as this example with directory trees, it is possible to achieve fine-grained
locking with much less work.

[[tree-locking]]
==== Tree Locking

Rather than locking every involved document, as in the previous option, we
could lock just part of the directory tree.((("locking", "tree locking")))  We will need exclusive access
to the file or directory that we want to rename, which can be achieved with an
_exclusive lock_ document:

[source,json]
--------------------------
{ "lock_type": "exclusive" }
--------------------------

And we need shared locks on any parent directories, with a _shared lock_
document:

[source,json]
--------------------------
{
  "lock_type":  "shared",
  "lock_count": 1 <1>
}
--------------------------
<1> The `lock_count` records the number of processes that hold a shared lock.

A process that wants to rename `/clinton/projects/elasticsearch/README.txt`
needs an _exclusive_ lock on that file, and a _shared_ lock on `/clinton`,
`/clinton/projects`, and `/clinton/projects/elasticsearch`.

A simple `create` request will suffice for the exclusive lock, but the shared
lock needs a scripted update to implement some extra logic:

[source,groovy]
--------------------------
if (ctx._source.lock_type == 'exclusive') {
  assert false; <1>
}
ctx._source.lock_count++ <2>
--------------------------
<1> If the `lock_type` is `exclusive`, the `assert` statement will throw
    an exception, causing the update request to fail.
<2> Otherwise, we increment the `lock_count`.

This script handles the case where the `lock` document already exists, but we
will also need an `upsert` document to handle the case where it doesn't exist
yet. The full update request is as follows:

[source,json]
--------------------------
POST /fs/lock/%2Fclinton/_update <1>
{
  "upsert": { <2>
    "lock_type":  "shared",
    "lock_count": 1
  },
  "script": "if (ctx._source.lock_type == 'exclusive') 
  { assert false }; ctx._source.lock_count++"
}
--------------------------
<1> The ID of the document is `/clinton`, which is URL-encoded to `%2fclinton`.
<2> The `upsert` document will be inserted if the document does not already
    exist.

Once we succeed in gaining a shared lock on all of the parent directories, we
try to `create` an exclusive lock on the file itself:

[source,json]
--------------------------
PUT /fs/lock/%2Fclinton%2fprojects%2felasticsearch%2fREADME.txt/_create
{ "lock_type": "exclusive" }
--------------------------

Now, if somebody else wants to rename the `/clinton` directory, they would
have to gain an exclusive lock on that path:

[source,json]
--------------------------
PUT /fs/lock/%2Fclinton/_create
{ "lock_type": "exclusive" }
--------------------------

This request would fail because a `lock` document with the same ID already
exists. The other user would have to wait until our operation is done and we
have released our locks. The exclusive lock can just be deleted:

[source,json]
--------------------------
DELETE /fs/lock/%2Fclinton%2fprojects%2felasticsearch%2fREADME.txt
--------------------------

The shared locks need another script that decrements the `lock_count` and, if
the count drops to zero, deletes the `lock` document:

[source,groovy]
--------------------------
if (--ctx._source.lock_count == 0) {
  ctx.op = 'delete' <1>
}
--------------------------
<1> Once the `lock_count` reaches `0`, the `ctx.op` is changed from `update`
    to `delete`.

This update request would need to be run for each parent directory in reverse
order, from longest to shortest:

[source,json]
--------------------------
POST /fs/lock/%2Fclinton%2fprojects%2felasticsearch/_update
{
  "script": "if (--ctx._source.lock_count == 0) { ctx.op = 'delete' } "
}
--------------------------

Tree locking gives us fine-grained concurrency control with the minimum of
effort. Of course, it is not applicable to every situation--the data model
must have some sort of access path like the directory tree for it to work.

[NOTE]
=====================================

None of the three options--global, document, or tree locking--deals with
the thorniest problem associated with locking: what happens if the process
holding the lock dies?

The unexpected death of a process leaves us with two problems:

* How do we know that we can release the locks held by the dead process?
* How do we clean up the change that the dead process did not manage to complete?

These topics are beyond the scope of this book, but you will need to give them
some thought  if you decide to use locking.

=====================================

While denormalization is a good choice for many projects, the need for locking
schemes can make for complicated implementations. Instead, Elasticsearch
provides two models that help us deal with related entities:
_nested objects_ and _parent-child relationships_.
