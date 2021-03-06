from unittest import TestCase

from mock import MagicMock

from messente.verigator import routes, client, controllers, exceptions


class TestUsers(TestCase):
    def setUp(self):
        self.rest_client = client.RestClient("http://test", "test", "test")
        self.users = controllers.Users(self.rest_client)
        self.sample_response = {
            "id_in_service": "test2",
            "ctime": "2017-09-15T08:13:26.965341",
            "id": "38fb335c-025d-45eb-9cf2-d2d4d9f54203"
        }

    def tearDown(self):
        pass

    def test_create(self):
        self.rest_client.post = MagicMock(return_value=self.sample_response)
        res = self.users.create("service_id", "0123", "username")

        self.rest_client.post.assert_called_with(routes.CREATE_USER.format("service_id"),
                                                 json={"id_in_service": "username", "phone_number": "0123"})
        self.assertEqual(res.id, self.sample_response['id'])
        self.assertEqual(res.creation_time, self.sample_response['ctime'])
        self.assertEqual(res.username, self.sample_response['id_in_service'])

    def test_get(self):
        self.rest_client.get = MagicMock(return_value=self.sample_response)
        res = self.users.get("sid", "uid")

        self.rest_client.get.assert_called_with(routes.GET_USER.format("sid", "uid"))
        self.assertEqual(res.id, self.sample_response['id'])
        self.assertEqual(res.creation_time, self.sample_response['ctime'])
        self.assertEqual(res.username, self.sample_response['id_in_service'])

    def test_get_all(self):
        self.rest_client.get = MagicMock(return_value={"users": [self.sample_response]})
        res = self.users.get_all("sid")

        self.rest_client.get.assert_called_with(routes.GET_USERS.format("sid"))
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].id, self.sample_response['id'])
        self.assertEqual(res[0].creation_time, self.sample_response['ctime'])
        self.assertEqual(res[0].username, self.sample_response['id_in_service'])

    def test_delete(self):
        self.rest_client.delete = MagicMock(return_value=self.sample_response)
        res = self.users.delete("sid", "uid")

        self.rest_client.delete.assert_called_with(routes.DELETE_USER.format("sid", "uid"))
        self.assertTrue(res)

    def test_create_failed(self):
        self.rest_client.post = MagicMock(side_effect=exceptions.ResourceAlreadyExistsError(409, "message"))

        try:
            self.users.create("", "", "")
        except exceptions.ResourceAlreadyExistsError as e:
            self.assertEqual(e.code, 409)
            self.assertEqual(e.message, "message")
        else:
            self.fail("Exception not raised")

    def test_invalid_input(self):
        self.assertRaises(ValueError, controllers.Users, None)
        self.assertRaises(ValueError, self.users.create, None, None, None)
        self.assertRaises(ValueError, self.users.get, None, None)
        self.assertRaises(ValueError, self.users.get_all, None)
        self.assertRaises(ValueError, self.users.delete, None, None)
