"""People Endpoint."""
from backend import app, logger
from utils import security
from flask import request
from flask_restplus import Namespace, Resource, fields
from repository import Repository
from elasticsearch import NotFoundError

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
    'coach': fields.String(required=True, description='Coach'),
    'pdm': fields.String(required=True, description='Manager responsible for career path'),
    'bp': fields.String(required=True, description='Business partner from HR'),
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

query = api.model('Query DSL', {
    'query': fields.String,
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
        return repository.search_by_query(index='people', query=request.json)

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
