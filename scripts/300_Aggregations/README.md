This directory contains two scripts that can be used to generate a taxi example data set. They require Python 3 and for `import.py` you must also have the Elasticsearch Python client installed (`pip3 install elasticsearch`).

Run `./generate.py 100 > documents.json` to generate 100 random taxi rides. You can import them into a local Elasticsearch cluster (5.x or 6.0) by running `./import.py mappings.json documents.json`.
