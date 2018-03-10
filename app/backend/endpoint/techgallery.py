""""TechGallery class."""
from backend import current_path
from httplib2 import Http
import re
import json
import os
import sys
import logging
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = 'https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile'
logger = logging.getLogger('stack')

class TechGallery(object):
    """TechGallery operations."""

    def __init__(self, config):
        """Init object.

        Config object must have a TECHGALLERY_ENDPOINT like this
        https://tech-gallery.appspot.com/_ah/api/rest/v1
        """
        self.config = config
        self.endpoint = config.get('TECHGALLERY_ENDPOINT')

    def get_credentials(self):
        """Get valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        credential_path = os.path.abspath(os.path.join(current_path, '..', 'knowledgemap_service_account.json'))
        return ServiceAccountCredentials.from_json_keyfile_name(credential_path, SCOPES)

    def profile(self, login):
        """Get a profile data by login.

        If profile was not found, then return status_code 404
        """
        # authorize http
        if self.config.get('TECHGALLERY_AUTH'):
            credentials = self.get_credentials()
            h = credentials.authorize(Http())
        else:
            h = Http()

        url = '%s/profile?email=%s@ciandt.com' % (self.endpoint, login)
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=UTF-8'
        }
        response, content = h.request(
                url,
                method='GET',
                headers=headers)

        return json.loads(content), response.status

    def technology(self, id):
        """Get details about technology.

        If profile was not found, then return status_code 404
        """
        # authorize http
        if self.config.get('TECHGALLERY_AUTH'):
            credentials = self.get_credentials()
            h = credentials.authorize(Http())
        else:
            h = Http()

        url = '%s/technology/%s' % (self.endpoint, id)
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=UTF-8'
        }
        response, content = h.request(
                url,
                method='GET',
                headers=headers)

        return json.loads(content), response.status


black_list = {
    'backbone.js': 'backbone.js',
    'calabash': 'cabalash',
    'node.js': 'node.js',
    'asp.net core': 'asp.net_core',
    'asp.net webforms': 'asp.net_webforms',
    'asp.net webapi': 'asp.net_webapi',
    'asp.net mvc': 'asp.net_mvc',
    'quartz.net': 'quartz.net'
}


def convert_name_to_id(tech_name):
    r"""Convert technology name to id.

    This method make a string replace using a bellow rules
    public String convertNameToId(String name) {
        name = Normalizer.normalize(name, Normalizer.Form.NFD);
        name = name.replaceAll("[^\\p{ASCII}]", "");
        return name.toLowerCase()
            .replaceAll(" ", "_")
            .replaceAll("#", "_")
            .replaceAll("\\/", "_")
            .replaceAll("\\.", "");
      }

    """
    if tech_name:
        if tech_name.lower() in black_list:
            tech_key = black_list[tech_name.lower()]
        else:
            tech_key = re.sub('[#/ ]', '_', re.sub(
                '[^\x00-\x7F]', '_', re.sub(
                    '[.]', '', tech_name.lower())))

        return tech_key
