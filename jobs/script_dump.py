"""Config class."""
import os
import sys
sys.path.insert(1, os.path.abspath(os.curdir))
sys.path.insert(1, os.path.join(os.path.abspath(os.curdir), 'lib'))

from elasticsearch import Elasticsearch

###
# python script_dump.py --logging_level DEBUG --host_source http://104.197.92.45:9202/ --user_source root --pass_source rootpass
###
try:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--logging_level', default='ERROR',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Set the logging level of detail.')
    parser.add_argument(
        '--host_source',
        help='Set hostname for source data. Like localhost:9200',
        required=True)
    parser.add_argument(
        '--user_source',
        help='Set username for source repository.',
        required=True)
    parser.add_argument(
        '--pass_source',
        help='Set password for source repositor.',
        required=True)
    parser.add_argument(
        '--host_target',
        default='localhost:9200',
        help='Set hostname for target data. If notify is defined, will use localhosts:9200',
        required=False)
    parser.add_argument(
        '--user_target',
        help='Set username for source repository.',
        default='user',
        required=False)
    parser.add_argument(
        '--pass_target',
        help='Set password for source repositor.',
        default='changeme',
        required=False)
    flags = parser.parse_args()
    args = vars(flags)
except ImportError:
    flags = None

import logging
from utils import logger_builder
logging_level = args['logging_level'] or 'ERROR'
logger = logger_builder.initLogger(logging_level)

es_source = Elasticsearch(
            [args['host_source']],
            http_auth=(args['user_source'], args['pass_source']),
            send_get_body_as='POST')

es_target = Elasticsearch(
            [args['host_target']],
            http_auth=(args['user_target'], args['pass_target']),
            send_get_body_as='POST')

query = {"query": {"match_all": {}}}

response = es_source.search(index='people', doc_type='profile', body=query, size=5000)

i = 0
for item in response['hits']['hits']:
    document = item['_source']
    login = item['_source']['login']
    i = i +1
    logger.info('%s login %s' % (i, login))
    es_target.index(index='people', doc_type='profile', body=document, id=login)
