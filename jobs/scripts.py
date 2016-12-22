import logging
import os
from config import Config
from datetime import datetime
from people import People
from profile import Profile

FORMAT = '%(name)s %(levelname)-5s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('profile')
logger.addHandler(logging.NullHandler())
logger.setLevel(logging.DEBUG)
logging.getLogger('elasticsearch').setLevel(logging.ERROR)

config = Config()
people = People(config)
profile = Profile(config)

def load_people():
    count = 0

    for hit in people.find_users():
        count += 1
        logger.info("Loading %s - %s  " % (hit['login'], count))
        project = people.find_project_by_user(hit['login'])

        admission = datetime.utcfromtimestamp(hit['admission'] / 1000)
        birthday = datetime.utcfromtimestamp(hit['birthday'] / 1000)

        doc = {
               'name': hit['name'],
               'login': hit['login'],
               'role': hit['role'],
               'cityBase': hit['cityBase'],
               'admission': admission,
               'birthday': birthday,
               'project': {
                    'code': hit['project']['code'],
                    'name': project
               },
               'area': hit['area'],
               'company': hit['company']
        }

        logger.info('Inserting people %s' % hit['login'])

        profile.save(hit['login'], doc)

def load_coach():
    count = 0
    for hit in people.find_users():
        count += 1
        login = hit['login']
        logger.info("Loading %s - %s  " % (login, count))

        coach = people.find_coach_by_login(login)
        pdm = people.find_pdm_by_login(login)




if __name__ == '__main__':
	load_people()
