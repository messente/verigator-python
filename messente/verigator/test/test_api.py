from unittest import TestCase, skip
from messente.verigator.api import Api


class ApiTest(TestCase):

    def setUp(self):
        self.api = Api("", "")

    def test_contains_required_libs(self):
        self.assertTrue(self.api.auth)
        self.assertTrue(self.api.services)
        self.assertTrue(self.api.users)
