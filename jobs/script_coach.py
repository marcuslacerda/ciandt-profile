"""Script load coach structure."""
from config import Config
from people import People
from people import Profile
from people import Coach
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
coach = Coach(config)

logging_level = args['logging_level'] or 'ERROR'
logger = logger_builder.initLogger(logging_level)


def load_coach():
    """Load coach structure and save document."""
    count = 0
    people_list = profile.find_all()
    total_hits = people_list['hits']['total']
    logger.info('total %s sheets' % total_hits)

    for item in people_list['hits']['hits']:
        count += 1
        people_item = item['_source']
        login = people_item['login']
        logger.info("Loading %s - %s  " % (login, count))

        coach_item = converter_to_people(people.find_coach_by_login(login))
        people_item['coach'] = coach_item
        pdm_item = converter_to_people(people.find_pdm_by_login(login))
        people_item['pdm'] = pdm_item

        coach.save(people_item)


def converter_to_people(worker):
    if worker:
        """Converter array object to people dictionary."""
        doc = {
            'name': worker[0],
            'login': worker[1],
            'role': worker[4],
            'coach': worker[5],
            'pdm': worker[6],
            'city': worker[7]
        }

        return doc
    else:
        return None

if __name__ == '__main__':
	load_coach()
