# The Definitive Guide to Elasticsearch 

This repository contains the sources to the "Definitive Guide to Elasticsearch" which you can [read online](https://www.elastic.co/guide/en/elasticsearch/guide/current/index.html).
 
## Building the Definitive Guide

In order to build this project, we rely on our [docs infrastructure](https://github.com/elastic/docs).

To build the HTML of the complete project, run the following commands:

```
# clone this repo
git clone git@github.com:elastic/elasticsearch-definitive-guide.git
# clone the docs build infrastructure
git clone git@github.com:elastic/docs.git
# Build HTML and open a browser
cd elasticsearch-definitive-guide
../docs/build_docs.pl --doc book.asciidoc --open
```

This assumes that you have all necessary prerequisites installed. For a more complete reference, please refer to the [README in the docs repo](https://github.com/elastic/docs).

The Definitive Guide is written in Asciidoc and the docs repo also contains a [short Asciidoc guide](https://github.com/elastic/docs#asciidoc-guide).

## Supported versions

The Definitive Guide is available for multiple versions of Elasticsearch:

* The [branch `1.x`](https://github.com/elastic/elasticsearch-definitive-guide/tree/1.x) applies to Elasticsearch 1.x
* The [branch `2.x`](https://github.com/elastic/elasticsearch-definitive-guide/tree/2.x) applies to Elasticsearch 2.x
* The [branch `master`](https://github.com/elastic/elasticsearch-definitive-guide/tree/2.x) applies to master branch of Elasticsearch (the current development version)

## Contributing

Before contributing a change please read our [contribution guide](CONTRIBUTING.md).

## License

This work is licensed under a Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License.

See http://creativecommons.org/licenses/by-nc-nd/3.0/ for the full text of the License.