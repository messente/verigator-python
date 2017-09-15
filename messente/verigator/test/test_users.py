from unittest import TestCase

from mock import MagicMock

from messente.verigator import routes
from messente.verigator.client import RestClient
from messente.verigator.controllers import Users
from messente.verigator.exceptions import *


class TestUsers(TestCase):
    def setUp(self):
        self.client = RestClient("http://test", "test", "test")
        self.users = Users(self.client)
        self.sample_response = {
            "id_in_service": "test2",
            "ctime": "2017-09-15T08:13:26.965341",
            "id": "38fb335c-025d-45eb-9cf2-d2d4d9f54203"
        }

    def tearDown(self):
        pass

    def test_create(self):
        self.client.post = MagicMock(return_value=self.sample_response)
        res = self.users.create("service_id", "0123", "username")

        self.client.post.assert_called_with(routes.CREATE_USER.format("service_id"),
                                            json={"id_in_service": "username", "phone_number": "0123"})
        self.assertEqual(res.id, self.sample_response['id'])
        self.assertEqual(res.creation_time, self.sample_response['ctime'])
        self.assertEqual(res.username, self.sample_response['id_in_service'])

    def test_get(self):
        self.client.get = MagicMock(return_value=self.sample_response)
        res = self.users.get("sid", "uid")

        self.client.get.assert_called_with(routes.GET_USER.format("sid", "uid"))
        self.assertEqual(res.id, self.sample_response['id'])
        self.assertEqual(res.creation_time, self.sample_response['ctime'])
        self.assertEqual(res.username, self.sample_response['id_in_service'])

    def test_get_all(self):
        self.client.get = MagicMock(return_value={"users": [self.sample_response]})
        res = self.users.get_all("sid")

        self.client.get.assert_called_with(routes.GET_USERS.format("sid"))
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].id, self.sample_response['id'])
        self.assertEqual(res[0].creation_time, self.sample_response['ctime'])
        self.assertEqual(res[0].username, self.sample_response['id_in_service'])

    def test_delete(self):
        self.client.delete = MagicMock(return_value=self.sample_response)
        res = self.users.delete("sid", "uid")

        self.client.delete.assert_called_with(routes.DELETE_USER.format("sid", "uid"))
        self.assertTrue(res)

    def test_create_failed(self):
        self.client.post = MagicMock(side_effect=ResourceAlreadyExistsError(409, "message"))

        try:
            self.users.create("", "", "")
        except ResourceAlreadyExistsError as e:
            self.assertEqual(e.code, 409)
            self.assertEqual(e.message, "message")
        else:
            self.fail("Exception not raised")

    def test_invalid_input(self):
        self.assertRaises(ValueError, Users, None)
        self.assertRaises(ValueError, self.users.create, None, None, None)
        self.assertRaises(ValueError, self.users.get, None, None)
        self.assertRaises(ValueError, self.users.get_all, None)
        self.assertRaises(ValueError, self.users.delete, None, None)
