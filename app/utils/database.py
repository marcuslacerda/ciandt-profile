"""Database utils."""
from elasticsearch import Elasticsearch
import json
import os
import logging

logger = logging.getLogger('stack')


def initEs(host, user, password):
    """Init Elasticsearch object.

    If user was defined, then the http_auth connection will be created.
    """
    if user:
        return Elasticsearch([host], http_auth=(user, password))
    else:
        return Elasticsearch([host])


def create_template_if_notexits(es, file, index):
    """If template doesn't exists, create one from json file definition.

    Method reads a template definition from file on path ./resources ('%s-template.json' % index)
    where index is a method's parameter
    """
    if not es.indices.exists_template(name=index):
        logger.info('creating template for index %s' % index)
        resource_path = os.path.join(os.path.split(file)[0], ("%s-template.json" % index ))
        with open(resource_path) as data_file:
            settings = json.load(data_file)

        # create index
        response = es.indices.put_template(name=index, body=settings)
        logger.debug("Template %s created" % response['acknowledged'])
