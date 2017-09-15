from unittest import TestCase

from mock import MagicMock

from messente.verigator import routes
from messente.verigator.client import RestClient
from messente.verigator.controllers import Services
from messente.verigator.exceptions import *


class TestServices(TestCase):
    def setUp(self):
        self.client = RestClient("https://test", "test", "test")
        self.services = Services(self.client)
        self.sample_response = {
            "id": "id",
            "ctime": "2017-09-15T06:44:15.274438",
            "name": "name"
        }

    def tearDown(self):
        pass

    def test_create(self):
        self.client.post = MagicMock(return_value=self.sample_response)
        res = self.services.create("domain", "name")

        self.client.post.assert_called_with(routes.CREATE_SERVICE, json={"fqdn": "domain", "name": "name"})
        self.assertEqual(res.id, self.sample_response['id'])
        self.assertEqual(res.creation_time, self.sample_response['ctime'])
        self.assertEqual(res.name, self.sample_response['name'])

    def test_get(self):
        self.client.get = MagicMock(return_value=self.sample_response)
        res = self.services.get("id")

        self.client.get.assert_called_with(routes.GET_SERVICE.format("id"))
        self.assertEqual(res.id, self.sample_response['id'])
        self.assertEqual(res.creation_time, self.sample_response['ctime'])
        self.assertEqual(res.name, self.sample_response['name'])

    def test_delete(self):
        self.client.delete = MagicMock(return_value=self.sample_response)
        res = self.services.delete("id")

        self.client.delete.assert_called_with(routes.DELETE_SERVICE.format("id"))
        self.assertTrue(res)

    def test_create_failed(self):
        self.client.post = MagicMock(side_effect=ResourceAlreadyExistsError(409, "message"))

        try:
            self.services.create("", "")
        except ResourceAlreadyExistsError as e:
            self.assertEqual(e.code, 409)
            self.assertEqual(e.message, "message")
        else:
            self.fail("Exception not raised")
