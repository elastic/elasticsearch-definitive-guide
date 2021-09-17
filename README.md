# Elasticsearch: The Definitive Guide

This repository contains the source for the legacy [Elasticsearch: The Definitive Guide](https://www.elastic.co/guide/en/elasticsearch/guide/current/index.html)
documentation and is no longer maintained. For the latest information, see the
<a
href="https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html">current
Elasticsearch documentation</a>.

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

* The [`1.x` branch](https://github.com/elastic/elasticsearch-definitive-guide/tree/1.x) applies to Elasticsearch 1.x
* The [`2.x` and `master` branches](https://github.com/elastic/elasticsearch-definitive-guide/tree/2.x) apply to Elasticsearch 2.x

## Contributing

This repository is no longer maintained. Pull requests and issues will not be
addressed.

To contribute to the current Elasticsearch docs, refer to the [Elasticsearch
repository](https://github.com/elastic/elasticsearch/).

## License

This work is licensed under a Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License.

See http://creativecommons.org/licenses/by-nc-nd/3.0/ for the full text of the License.