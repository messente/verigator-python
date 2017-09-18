from unittest import TestCase

from messente.verigator import api


class ApiTest(TestCase):
    def setUp(self):
        self.api = api.Api("", "")

    def test_contains_required_libs(self):
        self.assertTrue(self.api.auth)
        self.assertTrue(self.api.services)
        self.assertTrue(self.api.users)
