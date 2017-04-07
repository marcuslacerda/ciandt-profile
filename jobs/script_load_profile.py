"""Script load people."""
from config import Config
from datetime import datetime
from people import People
from people import Profile
from utils import logger_builder

try:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--logging_level', default='ERROR',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Set the logging level of detail.')
    flags = parser.parse_args()
    args = vars(flags)
except ImportError:
    flags = None

config = Config()
people = People(config)
profile = Profile(config)

logging_level = args['logging_level'] or 'ERROR'
logger = logger_builder.initLogger(logging_level)


def load_people():
    """Get all login from people API and save on elasticsearch database."""
    count = 0

    for hit in people.find_all_users():
        count += 1
        logger.info("Loading %s - %s  " % (hit['login'], count))
        project = people.find_project_by_user(hit['login'])

        admission = datetime.utcfromtimestamp(hit['admission'] / 1000)
        admission_real = datetime.utcfromtimestamp(hit['admissionReal'] / 1000)
        birthday = datetime.utcfromtimestamp(hit['birthday'] / 1000)

        doc = {
               'name': hit['name'],
               'login': hit['login'],
               'role': hit['role'],
               'cityBase': hit['cityBase'],
               'admission': admission,
               'admissionReal': admission_real,
               'birthday': birthday,
               'project': {
                    'code': hit['project']['code'],
                    'name': project
               },
               'area': hit['area'],
               'company': hit['company'],
               'status': hit['status']
        }

        logger.debug('Inserting people %s' % hit['login'])

        profile.save(doc)

if __name__ == '__main__':
	load_people()
