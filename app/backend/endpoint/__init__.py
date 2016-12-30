from backend import app, logger
from flask import Blueprint
from flask_restplus import Api

from profile import api as api_profile
from auth import api as api_auth
from user import api as api_user
import public

blueprint = Blueprint('api', __name__, url_prefix='/api')

authorizations = {
    'oauth2': {
        'type': 'oauth2',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(
    blueprint,
    version='1.0',
    title='Profile API',
    description='Access profile data.',
    authorizations=authorizations)

app.register_blueprint(blueprint)
api.add_namespace(api_profile)
logger.info('Profile API was registered.')
api.add_namespace(api_auth)
logger.info('Auth API was registered.')
api.add_namespace(api_user)
logger.info('User API was registered.')
