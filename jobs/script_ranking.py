"""Script load people."""
from config import Config
from datetime import datetime
from people import Profile
from people import Strength
from utils import logger_builder
from techgallery import TechGallery

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
strength = Strength(config)
profile = Profile(config)
techgallery = TechGallery(config)

def load_ranking():
    """Get all login from people API and save on elasticsearch database."""
    count = 0

    for docs in profile.find_ativos()['hits']['hits']:
        person = docs['_source']
        count += 1
        logger.info("Loading %s - %s  " % (person['login'], count))

        # search technologies from login
        (techs, status_code) = techgallery.profile(person['login'])
        if status_code != 200:
            logger.warn("%s not has login on Tech Gallery" % person['login'])
            continue

        endorsement_points = 0
        skill_points = 0
        award_points = 0

        if 'technologies' in techs:
            technologies = techs['technologies']

            # earn 1 point for each endorsement
            endorsement_points = sum(int(tech['endorsementsCount']) for tech in technologies)
            logger.debug('endorse points => ' + str(endorsement_points))

            # earch point for each skill evaluation, using this rule
            # skillLevel : points
            skill_dict = {
                1 : 0.1,
                2 : 0.2,
                3 : 0.5,
                4 : 1,
                5: 10
            }
            skill_rule = lambda skill_level: skill_dict.get(skill_level, 0)
            skill_points = sum([skill_rule(tech['skillLevel']) for tech in techs['technologies']])

            logger.debug('skill_points => %s' % str(skill_points))

        # earn points for each award, like this
        # award_name : points
        awards_dict = {
            "15 Years": 15,
            "10 Years": 10,
            "5 Years": 5,
            "Team Highlight": 5,
            "Area Star": 10,
            "Individual Highlight": 20,
            "Highlight of the Year": 100
            }
        awards_rule = lambda award_name: awards_dict.get(award_name, 0)
        if 'awards' in person:
            award_points = sum([awards_rule(award['name']) for award in person['awards']])
            logger.debug('award_points => %s' % str(award_points))

        doc = {
               'login': person['login'],
               'name': person['name'],
               'login': person['login'],
               'role': person['role'],
               'cityBase': person['cityBase'],
               'telephone': person.get('telephone'),
               'total': endorsement_points + skill_points + award_points,
               'endorsement' : endorsement_points,
               'skill': skill_points,
               'award': award_points
        }

        logger.info(doc)
        strength.save(doc)

    for docs in strength.find_ranking()['hits']['hits']:
        person = docs['_source']
        count += 1
        logger.info("Updating ranking %s Login: %s  Points: %s" % ( count, person['login'], person['total']))

        doc_status = {
            "doc": {
                  "ranking": count
              }
        }

        strength.update(person['login'], doc_status)
        profile.update(person['login'], doc_status)



if __name__ == '__main__':
	load_ranking()
