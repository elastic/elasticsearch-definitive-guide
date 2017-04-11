## Contributing to the Definitive Guide

### Contributing documentation changes

If you have a change that you would like to contribute, please find or open an
issue about it first. Talk about what you would like to do. It might be that 
somebody is already working on it, or that there are particular issues that 
you should know about before making the change.

Where possible, stick to an 80 character line length in the asciidoc source
files. Do not exceed 120 characters. Use 2 space indents in code examples.

The process for contributing to any of the [Elastic repositories](https://github.com/elastic/) 
is similar. Details can be found below.

### Fork and clone the repository

You will need to fork the main repository and clone it to your local machine.
See the respective [Github help page](https://help.github.com/articles/fork-a-repo)
for help.

### Submitting your changes

Once your changes and tests are ready to submit for review:

1. Test your changes

    [Build the complete book locally](https://github.com/elastic/elasticsearch-definitive-guide#building-the-definitive-guide) 
    and check and correct any errors that you encounter.

2. Sign the Contributor License Agreement

    Please make sure you have signed our [Contributor License Agreement](https://www.elastic.co/contributor-agreement/). 
    We are not asking you to assign copyright to us, but to give us the right 
    to distribute your code without restriction. We ask this of all 
    contributors in order to assure our users of the origin and continuing 
    existence of the code. You only need to sign the CLA once.

3. Rebase your changes

    Update your local repository with the most recent code from the main 
    repository, and rebase your branch on top of the latest `master` branch. 
    We prefer your initial changes to be squashed into a single commit. Later, 
    if we ask you to make changes, add them as separate commits.  This makes 
    them easier to review.  As a final step before merging we will either ask 
    you to squash all commits yourself or we'll do it for you.


4. Submit a pull request

    Push your local changes to your forked copy of the repository and 
    [submit a pull request](https://help.github.com/articles/using-pull-requests). 
    In the pull request, choose a title which sums up the changes that you 
    have made, and in the body provide more details about what your changes do.
    Also mention the number of the issue where discussion has taken place, 
    e.g. "Closes #123".

Then sit back and wait. There will probably be discussion about the pull 
request and, if any changes are needed, we would love to work with you to get 
your pull request merged.

Please adhere to the general guideline that you should never force push
to a publicly shared branch. Once you have opened your pull request, you
should consider your branch publicly shared. Instead of force pushing
you can just add incremental commits; this is generally easier on your
reviewers. If you need to pick up changes from master, you can merge
master into your branch. A reviewer might ask you to rebase a
long-running pull request in which case force pushing is okay for that
request. Note that squashing at the end of the review process should
also not be done, that can be done when the pull request is [integrated
via GitHub](https://github.com/blog/2141-squash-your-commits).