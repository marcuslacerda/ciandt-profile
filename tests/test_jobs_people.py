"""People UnitTest."""
import unittest
import os
from people import People
from config import Config


class PeopleTestCase(unittest.TestCase):
    """People Test Cases."""

    def setUp(self):
        """Setup API settings for tests."""
        resource_path = os.path.join(
            os.path.split(__file__)[0], "resources/config.yaml")
        self.people = People(Config(resource_path))

    def test_find_user_by_login(self):
        """People: find user by login."""
        login = 'mlacerda'
        result = self.people.find_user_by_login(login)
        self.assertIsNotNone(result, 'Result must be a valid people')
        self.assertEquals(login, result[1])

    def test_invalid_login_return_none(self):
        """People: invalid login must return none."""
        login = 'blablabla'
        user = self.people.find_user_by_login(login)
        self.assertIsNone(user)

    def test_invlid_login_has_project_empty(self):
        """People: invalid login has project EMPTY."""
        login = 'blablabla'
        page = self.people.get_profile_page_by_user(login)
        self.assertIsNone(page)

    # def test_valid_login_has_project_not_empty(self):
    #     """People: valid login has project not empty."""
    #     login = 'mlacerda'
    #     page = self.people.get_profile_page_by_user(login)
    #     project = self.people.scan_project(page)
    #     self.assertIsNotNone(project)
