from backend import app, logger

from flask import jsonify, request
from functools import wraps
from httplib2 import Http
import json
import jwt
from jwt import DecodeError, ExpiredSignature

VALID_EMAIL_DOMAIN = '@ciandt.com'


def login_authorized(fn):
    """Decorator that checks that requests
    contain an id-token in the session or request header.
    userid will be None if the
    authentication failed, and have an id otherwise.

    Usage:
    @app.route("/")
    @auth.login_authorized
    def secured_call(userid=None):
        pass
    """
    @wraps(fn)
    def decorated_function(*args, **kwargs):
        if not 'Authorization' in request.headers:
            response = jsonify(message='Missing authorization header')
            response.status_code = 401
            return response

        # try parser json web token
        try:
            json_web_token = parse_token(request)
            access_token = get_oauth_token(json_web_token)

            logger.debug('access_token: %s' % access_token)

            user = validate_token(access_token)
            if user is None:
                response = jsonify(message='Check user token failed')
                response.status_code = 403
                return response
            return fn(user=user, *args, **kwargs)

        except DecodeError:
            response = jsonify(message='Token is invalid')
            response.status_code = 401
            return response
        except ExpiredSignature:
            response = jsonify(message='Token has expired')
            response.status_code = 403
            return response

    return decorated_function


def revoke_token(access_token):
    h = Http()
    logger.debug('revoking %s' % access_token)
    resp, cont = h.request('https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token,
                           headers={'Host': 'www.googleapis.com',
                                    'Authorization': access_token})

    return resp


def get_oauth_token(json_web_token):
    access_token =  json_web_token['access_token']

    if access_token:
        oauth_token = 'OAuth %s' % access_token
        return oauth_token
    return None


def create_token(payload):
    token = jwt.encode(payload, app.config['SECRET_KEY'])
    return token.decode('unicode_escape')

def parse_token(req):
    token = req.headers.get('Authorization').split()[1]
    return jwt.decode(token, app.config['SECRET_KEY'])


def is_valid_email(email):
    return VALID_EMAIL_DOMAIN in email


def validate_token(access_token):
    '''Verifies that an access-token is valid and
    meant for this app.

    Returns None on fail, and an User on success'''
    h = Http()
    resp, cont = h.request("https://www.googleapis.com/oauth2/v2/userinfo",
                           headers={'Host': 'www.googleapis.com',
                                    'Authorization': access_token})

    if not resp['status'] == '200':
        return None

    try:
        data = json.loads(cont)
    except TypeError:
        # Running this in Python3
        # httplib2 returns byte objects
        data = json.loads(cont.decode())

    data['oauth_token'] = access_token

    return data
