from utils import util
from flask import Flask, send_file
from werkzeug.contrib.fixers import ProxyFix
import sys
import logging
import os
from datetime import datetime
from dotenv import load_dotenv

current_path = os.path.dirname(__file__)
template_path = os.path.abspath(os.path.join(current_path, 'swagger_templates'))
client_path = os.path.abspath(os.path.join(current_path, '..', 'frontend'))
dotenv_path = os.path.abspath(os.path.join(current_path, '..', '.env'))
load_dotenv(dotenv_path)


APP_NAME = 'profile'

app = Flask(
    APP_NAME,
    template_folder=template_path,
    static_url_path='',
    static_folder=client_path)
app.wsgi_app = ProxyFix(app.wsgi_app)

################
#### config ####
################
mode = util.get_environ(app.config, 'MODE', 'development')
config_json_path = os.path.abspath(os.path.join(current_path, '%s.json' % mode))
app.config.from_json(config_json_path)
app.config['GOOGLE_CLIENT_SECRET'] = util.get_environ(app.config, 'GOOGLE_CLIENT_SECRET')
app.config['GOOGLE_CLIENT_ID'] = util.get_environ(app.config, 'GOOGLE_CLIENT_ID')
app.config['ELASTICSEARCH_URL'] = util.get_environ(app.config, 'ELASTICSEARCH_URL')
app.config['ELASTICSEARCH_USER'] = os.environ.get('ELASTICSEARCH_USER')
app.config['ELASTICSEARCH_PASS'] = os.environ.get('ELASTICSEARCH_PASS')


################
#### swager ####
################
# app.config.SWAGGER_UI_JSONEDITOR = True


########################
#### logging config ####
########################
if (2, 7) <= sys.version_info < (3, 2):
    # On Python 2.7 and Python3 < 3.2, install no-op handler to silence
    # `No handlers could be found for logger "elasticsearch"` message per
    # <https://docs.python.org/2/howto/logging.html#configuring-logging-for-a-library>
    FORMAT = '%(name)s %(levelname)-5s %(message)s'
    logging.basicConfig(format=FORMAT)
    for item in app.config['LOGGER']:
        logging.getLogger(item['NAME']).setLevel(int(item['LEVELNO']))

logger = logging.getLogger('profile')
logger.info('starting app => %s ' % id(app))
logger.info('starting mode => %s ' % mode)

@app.after_request
def after_request(response):
    """Add headers for every response with no-cache control."""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "-1"
    response.headers['Last-Modified'] = datetime.now()

    return response


@app.route('/')
def index():
    """Main endpoint sends response with index.html file."""
    return send_file(os.path.join(client_path, 'index.html'))


# ##############
# #### APIs ####
# ##############
import endpoint
