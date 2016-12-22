"""Profile API Client."""
import logging
import requests
import json
from datetime import datetime
from requests.auth import HTTPBasicAuth

logger = logging.getLogger('profile')


class Profile(object):
    """Class that handle profile API calls."""

    def __init__(self, config):
        """Init class.

        Expect param config.('PROFILE_ENDPOINT') for profile API. User and pass can be
        provided from enviroment PROFILE_USER and PROFILE_PASS variables
        """
        self.endpoint = config.get('PROFILE_ENDPOINT')

    def save(self, id, payload):
        """Put payload document for profile API."""
        url = '%s/profiles/%s' % (self.endpoint, id)
        json_payload = json.dumps(payload, cls=DateTimeEncoder)
        response = requests.put(url=url, json=json_payload)

        return response.json(), response.status_code


class DateTimeEncoder(json.JSONEncoder):
    """Handle datetime encoder."""

    def default(self, o):
        """Convert datetime using isoformat datetime method."""
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)
