"""Script load people."""
from config import Config
from datetime import datetime
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


def update_rescission():
    """Get all login from people API and save on elasticsearch database."""
    count = 0

    for docs in profile.find_all()['hits']['hits']:
        hit = docs['_source']
        count += 1
        logger.info("Loading %s - %s  " % (hit['login'], count))

        (status_code,  people_doc) = people.find_user(hit['login'])

        if status_code == 200 and people_doc['status'] != 'A':
            rescission = datetime.utcfromtimestamp(people_doc['rescission'] / 1000)
            doc_status = {
                "doc": {
                      "rescission": rescission,
                      "status": people_doc['status']
                  }
            }

            logger.info('rescission detected for %s'  % hit['login'])

            profile.update(hit['login'], doc_status)
            coach.update(hit['login'], doc_status)

if __name__ == '__main__':
	update_rescission()
