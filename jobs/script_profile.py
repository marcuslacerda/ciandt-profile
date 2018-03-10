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
        '--logging_level', default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Set the logging level of detail.')
    flags = parser.parse_args()
    args = vars(flags)
except ImportError:
    flags = None

logging_level = args['logging_level'] or 'ERROR'
logger = logger_builder.initLogger(logging_level)

config = Config()
people = People(config)
profile = Profile(config)

def load_people():
    """Get all login from people API and save on elasticsearch database."""
    count = 0

    for hit in people.find_all_users():
        count += 1
        logger.info("Loading %s - login %s  " % (count, hit['login']))
        page = people.get_profile_page_by_user(hit['login'])
        project = 'Empty'
        awards_list = []
        if page:
            project = people.scan_project(page)
            awards_list = people.scan_awards(page)

        if hit['admission']:
            admission = datetime.utcfromtimestamp(hit['admission'] / 1000)
            admission_real = datetime.utcfromtimestamp(hit['admissionReal'] / 1000)

        if hit['birthday']:
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
               'awards_count': len(awards_list),
               'awards' : awards_list,
               'area': hit['area'],
               'company': hit['company'],
               'status': hit['status'],
               'coach': hit['coach'],
               'pdm': hit['pdm'],
               'bp': hit['bp'],
               'telephone': hit['telephone']
        }

        logger.debug('Inserting person %s' % hit['login'])

        profile.save(doc)

if __name__ == '__main__':
	load_people()
