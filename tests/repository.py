"""Repository class for people index."""
from elasticsearch import Elasticsearch
import logging
import os
import json

logger = logging.getLogger('profile')


class Repository(object):

    def __init__(self, config):
        logger.debug('Connection on %s' % config['ELASTICSEARCH_URL'])
        user = config['ELASTICSEARCH_USER']
        if user:
            self.es = Elasticsearch(
                [config['ELASTICSEARCH_URL']],
                http_auth=(
                    config['ELASTICSEARCH_USER'],
                    config['ELASTICSEARCH_PASS']))
        else:
            self.es = Elasticsearch([config['ELASTICSEARCH_URL']])

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

    def search_by_query(self,  query):
        data = self.es.search(index='people', body=query, size=2500)

        list_data = []
        for item in data['hits']['hits']:
            list_data.append(item['_source'])
        return list_data

    def get_by_login(self, login):
        item = self.es.get(index='people', doc_type='login', id=login)
        return item['_source']

    def delete_by_login(self, login):
        return self.es.delete(index='people', doc_type='login', id=login)

    def insert(self, document):
        res = self.es.index(index='people', doc_type='login', body=document, id=document['login'])
        logger.debug("Created documento ID %s" % res['_id'])

        return res
