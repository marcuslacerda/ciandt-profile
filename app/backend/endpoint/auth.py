"""People Endpoint."""
from backend import logger, app
from utils import security
from flask import request
from flask_restplus import Namespace, Resource, fields
from flask import jsonify
import requests
import json
from datetime import datetime

api = Namespace('auth', description='Authentication operations')

user = api.model('User', {
    'login': fields.String(readOnly=True, description='The unique identifier'),
    'name': fields.String(required=True, description='Full name'),
})

payload = api.model('Payload json', {
    'client_id': fields.String(readOnly=True, description='The unique id for user account'),
    'redirect_uri': fields.String(readOnly=True, description='Authorized redirect URI. This is the path in your application that users are redirected to after they have authenticated with Google.'),
    'code': fields.String(readOnly=True, description='Code autorization to be exchange by access token'),
})


@api.route('/google')
class GoogleProvider(Resource):
    """Shows a list of all people, and lets you POST to add new tasks"""
    # Using OAuth 2.0 to Access Google APIs. Login flow
    # https://developers.google.com/identity/protocols/OAuth2
    # https://developers.google.com/identity/protocols/OpenIDConnect#exchangecode
    # Step 1: (Browser) Send an authentication request to Google
    # Step 2: Exchange authorization code for access token.
    # Step 3: Retrieve information about the current user.
    @api.expect(payload)
    def post(self):
        """List all people."""
        access_token_url = 'https://www.googleapis.com/oauth2/v4/token'
        people_api_url = 'https://www.googleapis.com/oauth2/v3/userinfo'
        tokeninfo_url = 'https://www.googleapis.com/oauth2/v3/tokeninfo'

        logger.debug('google request =>')
        logger.debug(request.json)

        payload = dict(client_id=request.json['clientId'],
                       redirect_uri=request.json['redirectUri'],
                       client_secret=app.config['GOOGLE_CLIENT_SECRET'],
                       code=request.json['code'],
                       grant_type='authorization_code')

        logger.debug('Google Payload =>')
        logger.debug(payload)

        # Step 2. Exchange authorization code for access token.
        r = requests.post(access_token_url, data=payload)
        token = json.loads(r.text)
        logger.debug('Access Token =>')
        logger.debug(token)

        # Step 2. Retrieve information about the current user.
        # create user if not exists one
        headers = {'Authorization': 'Bearer {0}'.format(token['access_token'])}
        r = requests.get(people_api_url, headers=headers)
        profile = json.loads(r.text)
        logger.info('Login as => %s' % profile['email'])
        logger.debug(profile)

        if security.is_valid_email(profile['email']):
            # Step 4. Create a new account or return an existing one.
            r = requests.get('%s?access_token=%s' % (tokeninfo_url, token['access_token']))
            token_info = json.loads(r.text)
            logger.debug('Tokeninfo =>')
            logger.debug(token_info)

            # Step 5. Create a new account or return an existing one.
            payload = {
                'sub': profile['sub'],
                'iat': datetime.utcnow(),
                'exp': token_info['exp'],
                'access_token':token['access_token']
            }

            jwt = security.create_token(payload)
            return jsonify(token=jwt)
        else:
            return not_authorized(403, 'Invalid domain. Please sign in with @ciandt.com acccount')

@api.route('/logout')
class LogoutProvider(Resource):
    @security.login_authorized
    def get(user):
        """Revoke access token for user."""
        logger.info('Logout by %s' % user['email'])
        access_token = user['oauth_token']
        security.revoke_token(access_token)

        return "Logout Success", 200

def not_authorized(status, error):
    response = jsonify({'code': status,'message': error})
    response.status_code = status
    return response

class User:
    def __init__(self, id, email=None, password=None, display_name=None,
                 provider=None):
        self.id = id
        if email:
            self.email = email.lower()
        if password:
            self.password = password
        if display_name:
            self.display_name = display_name
        if provider:
            self.provider = provider

    def to_json(self):
        return dict(id=self.id, email=self.email, displayName=self.display_name,
                    google=self.google)
