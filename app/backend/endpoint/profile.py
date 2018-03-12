"""People Endpoint."""
from backend import app, logger
from utils import security
from flask import request
from flask_restplus import Namespace, Resource, fields
from repository import Repository
from elasticsearch import NotFoundError
import requests
import json
from techgallery import TechGallery

"""
Referencias:
https://github.com/swagger-api/swagger-ui#custom-header-parameters---for-basic-auth-etc
https://github.com/noirbizarre/flask-restplus/issues/26
https://github.com/frol/flask-restplus-server-example
"""
api = Namespace('profiles', description='Profile operations')
# api.add_resource(PeopleList, '/hello')

people = api.model('People', {
    'login': fields.String(readOnly=True, description='The unique identifier'),
    'name': fields.String(required=True, description='Full name'),
    'admission': fields.Date(required=True, description='Real admission date', attribute='admissionReal'),
    'coach': fields.String(required=False, description='Coach'),
    'pdm': fields.String(required=False, description='Manager responsible for career path'),
    'bp': fields.String(required=False, description='Business partner from HR'),
    'birthday': fields.Date(required=True, description='Birthday'),
    'telephone': fields.String(required=True, description='Public telephone'),
    'ranking': fields.Integer(required=True, description='Position on leaderboard'),
    'area': fields.Nested(api.model('AreaData', {
        'code': fields.Integer(
            description=u'code of area',
            required=False,
        ),
        'name': fields.String(
            description=u'name of area',
            required=True,
        ),
    })),
    'company': fields.Nested(api.model('CompanyData', {
        'code': fields.Integer(
            description=u'code of company',
            required=False,
        ),
        'name': fields.String(
            description=u'name of company',
            required=True,
        ),
    })),
    'project': fields.Nested(api.model('ProjectData', {
        'code': fields.Integer(
            description=u'code of projec',
            required=False,
        ),
        'name': fields.String(
            description=u'name of project',
            required=True,
        ),
    })),
    'role': fields.Nested(api.model('RoleData', {
        'code': fields.Integer(
            description=u'code of role',
            required=False,
        ),
        'name': fields.String(
            description=u'name of role',
            required=True,
        ),
    })),
    'cityBase': fields.Nested(api.model('CityBaseData', {
        'code': fields.Integer(
            description=u'code of city',
            required=False,
        ),
        'name': fields.String(
            description=u'name of city',
            required=True,
        ),
        'acronym': fields.String(
            description=u'acronym for city',
            required=True,
        ),
    })),
    'awards': fields.List(
        fields.Nested(api.model('AwardData', {
            'name': fields.String(
                description=u'Award name',
                required=True,
            ),
            'description': fields.String(
                description=u'Award description',
                required=False,
            ),
            'given_at': fields.DateTime(
                description=u'The date prize was given to him ',
                required=True,
            ),
            'given_by': fields.String(
                description=u'Person who gives this award',
                required=False,
            ),
        }))
    ),
})

query = api.model('Elasticsearch Query DSL', {
    'query': fields.String,
})

stack = api.model('Stack', {
    'key': fields.String(readOnly=True, description='The unique identifier'),
    'owner': fields.String(readOnly=True, description='The owner (customer name)'),
    'last_activity': fields.Date(required=True, description='Last updated date'),
    'name': fields.String(required=True, description='Product name or project')
})

skill = api.model('skill', {
    'technologyName': fields.String(readOnly=True, description='The unique identifier'),
    'skillLevel': fields.Integer(readOnly=True, description='The owner (customer name)'),
    'endorsementsCount': fields.Integer(required=True, description='Total of edorsements')
})

strength = api.model('strength', {
    'login': fields.String(readOnly=True, description='The unique identifier'),
    'name': fields.String(required=True, description='Full name'),
    'telephone': fields.String(required=True, description='Public telephone'),
    'ranking': fields.String(required=True, description='Position on leaderboard'),    
    'role': fields.Nested(api.model('RoleData', {
        'code': fields.Integer(
            description=u'code of role',
            required=False,
        ),
        'name': fields.String(
            description=u'name of role',
            required=True,
        ),
    })),
    'total': fields.Integer(readOnly=True, description='Total of points'),
    'skill': fields.Integer(required=True, description='Points about skill evaluation'),
    'award': fields.Integer(required=True, description='Points about awards'),
    'endorsement': fields.Integer(required=True, description='Points about endorsement'),
})


repository = Repository(app.config)

@api.route('/_search')
class PeopleSearch(Resource):
    """Shows a list of all people, and lets you POST to add new tasks"""
    @api.doc(security='oauth2')
    @security.login_authorized
    @api.expect(query)
    @api.marshal_list_with(people)
    def post(self, user):
        """List all people."""
        # print request.json

        return repository.search_by_query(query=request.json)

@api.route('/stack/<login>')
class PeopleStack(Resource):
    """Shows a list of skills"""
    @api.doc(security='oauth2')
    @security.login_authorized
    @api.response(404, 'People not found')
    @api.marshal_list_with(stack)
    def get(self, user, login):
        """List Person's skills."""

        json_web_token = security.parse_token(request)
        access_token = security.get_oauth_token(json_web_token)

        query = 'team.login:' + login
        stack_api_url = 'http://stack-ciandt.appspot.com/api/stacks/_search?q=' + query

        headers = {'Authorization': access_token}
        r = requests.get(stack_api_url, headers=headers)
        return json.loads(r.text)

@api.route('/skill/<login>')
class PeopleSkill(Resource):
    """Shows a list of skills"""
    @api.doc(security='oauth2')
    @security.login_authorized
    @api.response(404, 'People not found')
    @api.marshal_list_with(skill)
    def get(self, user, login):
        """List Person's skills."""

        config = {
            'TECHGALLERY_ENDPOINT' : 'https://tech-gallery.appspot.com/_ah/api/rest/v1',
            'TECHGALLERY_AUTH': True
        }
        techgallery =  TechGallery(config)

        (profile, status_code) = techgallery.profile(login)

        if status_code != 200:
            logger.warn("%s not has login on Tech Gallery" % people['login'])
            response = jsonify(message='Not Found')
            response.status_code = 404

        skill = []
        if 'technologies' in profile:
            for tech in profile['technologies']:
                skill.append(tech)

        skill.sort(key=lambda x:x['endorsementsCount'], reverse=True)

        return skill

@api.route('/strength/<login>')
class PeopleStrength(Resource):
    """Shows a list of skills"""
    @api.doc(security='oauth2')
    @security.login_authorized
    @api.response(404, 'People not found')
    @api.marshal_with(strength)
    def get(self, user, login):
        """List Person's skills."""
        query = {"query": {"match": {"login": login}}}
        strength = repository.search_by_query(query=query, index='profile', doc_type='strength', sort="login.keyword")
        if strength:
            return strength[0]

@api.route('/ranking')
class PeopleRanking(Resource):
    """Shows a list of skills"""
    @api.doc(security='oauth2')
    @security.login_authorized
    @api.marshal_list_with(strength)
    def post(self, user):
        """List Person's skills."""
        query = request.json

        print query

        return repository.search_by_query(query=query, index='profile', doc_type='strength', sort="total:desc")


@api.route('/')
class PeopleList(Resource):
    """Shows a list of all people, and lets you POST to add new tasks."""
    @api.doc(security='oauth2')
    @security.login_authorized
    @api.marshal_list_with(people)
    def get(self, user):
        """List all people."""
        query = {"query": {"match_all": {}}}
        return repository.search_by_query(query=query)

@api.route('/<login>')
@api.response(404, 'People not found')
@api.param('login', 'The login identifier')
class People(Resource):
    """Show a single people item and lets you delete them"""
    @api.doc('get_person')
    @security.login_authorized
    @api.marshal_with(people)
    def get(self, user, login):
        """Fetch a given resource."""
        return repository.get_by_login(login)

    @api.doc('delete_person')
    @security.login_authorized
    @api.response(204, 'Person deleted')
    def delete(self, user, login):
        """Delete a person given its login identifier."""
        repository.delete_by_login(login)
        return '', 204

    @api.expect(people)
    @security.login_authorized
    @api.marshal_with(people)
    def put(self, user, login):
        """Update a task given its identifier."""
        print request.json
        repository.create_template_if_notexits()
        repository.insert(login, request.json)
        return request.json


@api.errorhandler(NotFoundError)
def default_error_handler(e):
    message = 'NotfoundError. %s' % e.error
    logger.exception(message)
    return {'message': message}, e.status_code
    # if not settings.FLASK_DEBUG:

@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    logger.exception(message)
    return {'message': message}, 500
    # if not settings.FLASK_DEBUG:

if __name__ == '__main__':
    app.run(debug=True)
