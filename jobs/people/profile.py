"""Profile class."""
import logging
from utils import database

logger = logging.getLogger('profile')
index = 'people'
doc_type = 'profile'

class Profile(object):
    """Profile operations."""

    def __init__(self, config):
        """Init profile object using config param."""
        host = config.get('PROFILE_ELASTICSEARCH_HOST')
        user = config.get('PROFILE_ELASTICSEARCH_USER')
        password = config.get('PROFILE_ELASTICSEARCH_PASS')
        self.es = database.initEs(host, user, password)
        logger.debug('Connecting on %s for %s' % (host, index))

    def find_all(self):
        """Retrieve all documents."""
        query = '{"query": {"match_all": {}}}'
        return self.es.search(index=index, doc_type=doc_type, body=query, size=10000)

    def find_ativos(self):
        """Retrieve all documents."""
        query = '{"query": {"match": {"status": "A"}}}'
        return self.es.search(index=index, doc_type=doc_type, body=query, size=10000)


    def save(self, doc, refresh=False):
        """Save profile document. Create template if it not exists."""
        # database.create_template_if_notexits(self.es, __file__, index)
        logger.debug(doc)
        res = self.es.index(
            index=index,
            doc_type=doc_type,
            body=doc,
            id=doc['login'],
            refresh=refresh)
        logger.debug("Created documento ID %s" % res['_id'])

        return res

    def update(self, id, doc, refresh=False):
        """Update a document based on a script or partial data provided."""
        res = self.es.update(
            index=index,
            doc_type=doc_type,
            body=doc,
            id=id,
            refresh=refresh)
        logger.debug("Document %s updated" % res['_id'])


    def delete(self, id):
        """Remove documento by id."""
        self.es.delete(index=index, doc_type=doc_type, id=id)
