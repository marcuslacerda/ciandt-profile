"""Unit tests for User profile API."""
from backend import app, logger
import unittest
import json
from .repository import Repository

class ProfileApiTestCase(unittest.TestCase):
    """Tests for User Profile Api."""

    def setUp(self):
        """Setup API settings for tests."""
        app.config['TESTING'] = True
        self.app = app.test_client()
        repository = Repository({
            'ELASTICSEARCH_URL': 'http://localhost:9200',
            'ELASTICSEARCH_USER': ''
        })
        repository.insert(build_mock_people("mlacerda"))

    def tearDown(self):
        """Destroy settings created for tests."""
        pass

    def test_index_response(self):
        """TEST PROFILE API: get home."""
        rv = self.app.get('/')
        assert 200 == rv.status_code

    def test_api_get_version(self):
        """TEST PROFILE API: get version."""
        rv = self.app.get(
            '/api/public/version',
            content_type='application/json')
        self.assertTrue('0.0.BUILD_NUMBER' in rv.data, 'Invalid version')

    def test_api_get_profile(self):
        """TEST PROFILE API: get user profile."""
        id = 'mlacerda'
        rv = self.app.get(
            '/api/profiles/'+id,
            content_type='application/json')
        # print rv.data
        user = json.loads(rv.data)
        logger.info('response: %s' % user)
        self.assertEquals(user['login'], id)
        self.assertEquals(user['name'], 'MARCUS VINICIUS DE OLIVEIRA LACERDA')
        self.assertEquals(user['role']['name'], 'Developer')


def build_mock_people(login):
    doc = {
        "login": login,
        "name": "MARCUS VINICIUS DE OLIVEIRA LACERDA",
        "area": {
          "code": 20,
          "name": "BU South"
        },
        "company": {
          "code": 1,
          "name": "CIT Software S.A."
        },
        "cityBase": {
          "acronym": "BH",
          "code": 6,
          "name": "Belo Horizonte"
        },
        "project": {
          "code": 9347,
          "name": "Coca Cola"
        },
        "role": {
          "code": 96,
          "name": "Developer"
        }
    }

    return doc
