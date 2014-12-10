
=== Revisit This List Before Production

You are likely reading this section before you go into production.  
The details covered in this chapter are good to be generally aware of, but it is 
critical to revisit this entire list right before deploying to production.

Some of the topics will simply stop you cold (such as too few available file
descriptors).  These are easy enough to debug because they are quickly apparent.
Other issues, such as split brains and memory settings, are visible only after
something bad happens.  At that point, the resolution is often messy and tedious.

It is much better to proactively prevent these situations from occurring by configuring
your cluster appropriately _before_ disaster strikes.  So if you are going to
dog-ear (or bookmark) one section from the entire book, this chapter would be
a good candidate.  The week before deploying to production, simply flip through
the list presented here and check off all the recommendations.
