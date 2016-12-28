"""Repository class for people index."""
from elasticsearch import Elasticsearch
import logging

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

    def insert(self, document):
        res = self.es.index(index='people', doc_type='profile', body=document, id=document['login'])
        logger.debug("Created documento ID %s" % res['_id'])

        return res
