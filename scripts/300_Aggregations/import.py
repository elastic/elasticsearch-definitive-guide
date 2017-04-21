#!/usr/bin/env python3

import elasticsearch
import elasticsearch.helpers
import json
import logging
import sys
import itertools

logger = logging.getLogger("import")

index_name = "taxis"
type_name = "rides"


def create_index(client, mapping_file):
    if client.indices.exists(index=index_name):
        logger.info("Index [%s] already exists. Deleting it." % index_name)
        client.indices.delete(index=index_name)
    logger.info("Creating index [%s]" % index_name)
    client.indices.create(index=index_name, body='{"index.number_of_replicas": 0}')
    with open(mapping_file, "rt") as f:
        mappings = f.read()
    client.indices.put_mapping(index=index_name,
                               doc_type=type_name,
                               body=json.loads(mappings))


def import_data(client, data_file):
    meta_data = '{"_op_type": "index", "_index": "%s", "_type": "%s"}' % (index_name, type_name)
    with open(data_file, "rt") as f:
        elasticsearch.helpers.bulk(client, f, index=index_name, doc_type=type_name)


def main():
    if len(sys.argv) != 3:
        print("usage %s mapping_file_path data_file_path" % sys.argv[0])
        exit(1)

    es = elasticsearch.Elasticsearch()
    mapping_file = sys.argv[1]
    data_file = sys.argv[2]

    create_index(es, mapping_file)
    import_data(es, data_file)


if __name__ == '__main__':
    main()
