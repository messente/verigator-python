from unittest import TestCase

from mock import MagicMock

from messente.verigator import routes, client, controllers, exceptions


class TestServices(TestCase):
    def setUp(self):
        self.rest_client = client.RestClient("https://test", "test", "test")
        self.services = controllers.Services(self.rest_client)
        self.sample_response = {
            "id": "id",
            "ctime": "2017-09-15T06:44:15.274438",
            "name": "name"
        }

    def tearDown(self):
        pass

    def test_create(self):
        self.rest_client.post = MagicMock(return_value=self.sample_response)
        res = self.services.create("domain", "name")

        self.rest_client.post.assert_called_with(routes.CREATE_SERVICE, json={"fqdn": "domain", "name": "name"})
        self.assertEqual(res.id, self.sample_response['id'])
        self.assertEqual(res.creation_time, self.sample_response['ctime'])
        self.assertEqual(res.name, self.sample_response['name'])

    def test_get(self):
        self.rest_client.get = MagicMock(return_value=self.sample_response)
        res = self.services.get("id")

        self.rest_client.get.assert_called_with(routes.GET_SERVICE.format("id"))
        self.assertEqual(res.id, self.sample_response['id'])
        self.assertEqual(res.creation_time, self.sample_response['ctime'])
        self.assertEqual(res.name, self.sample_response['name'])

    def test_delete(self):
        self.rest_client.delete = MagicMock(return_value=self.sample_response)
        res = self.services.delete("id")

        self.rest_client.delete.assert_called_with(routes.DELETE_SERVICE.format("id"))
        self.assertTrue(res)

    def test_create_failed(self):
        self.rest_client.post = MagicMock(side_effect=exceptions.ResourceAlreadyExistsError(409, "message"))

        try:
            self.services.create("", "")
        except exceptions.ResourceAlreadyExistsError as e:
            self.assertEqual(e.code, 409)
            self.assertEqual(e.message, "message")
        else:
            self.fail("Exception not raised")

    def test_invalid_input(self):
        self.assertRaises(ValueError, controllers.Services, None)
        self.assertRaises(ValueError, self.services.create, None, None, None)
        self.assertRaises(ValueError, self.services.get, None, None)
        self.assertRaises(ValueError, self.services.delete, None, None)
