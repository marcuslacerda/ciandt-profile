"""Repository class for people index."""
from elasticsearch import Elasticsearch
import logging
import os
import json
from utils import database

logger = logging.getLogger('profile')


class Repository(object):

    def __init__(self, config):
        host = config['ELASTICSEARCH_URL']
        user = config['ELASTICSEARCH_USER']
        password = config['ELASTICSEARCH_PASS']

        self.es = database.initEs(host, user, password)
        logger.debug('Connecting on %s' % (host))


    def create_template_if_notexits(self):
        """If template doesn't exists, create one from json file definition.

        Method reads a template definition from file on path ./resources
        ('%s-template.json' % index) where index is a method's parameter.
        """
        index = 'people'
        if not self.es.indices.exists_template(name=index):
            resource_path = os.path.join(
                os.path.split(__file__)[0],
                ("resources/%s-template.json" % index))
            with open(resource_path) as data_file:
                settings = json.load(data_file)

            # create index
            response = self.es.indices.put_template(name=index, body=settings)
            logger.debug("Template %s created" % response['acknowledged'])

    def search_by_query(self,  query, index='people', doc_type='profile', sort="name.keyword"):
        data = self.es.search(index=index, doc_type=doc_type, body=query, sort=sort)

        list_data = []
        for item in data['hits']['hits']:
            list_data.append(item['_source'])
        return list_data

    def get_by_login(self, login):
        item = self.es.get(index='people', doc_type='profile', id=login)
        return item['_source']

    def delete_by_login(self, login):
        return self.es.delete(index='people', doc_type='profile', id=login)

    def insert(self, login, document, index='people', doc_type='profile'):
        res = self.es.index(index=index, doc_type=doc_type, body=document, id=login)
        logger.debug("Created documento ID %s" % res['_id'])

        return res

    def add(self, document, index='people', doc_type='profile'):
        res = self.es.index(index=index, doc_type=doc_type, body=document)
        logger.debug("Created documento ID %s" % res['_id'])

        return res
