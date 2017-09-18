from unittest import TestCase

from requests_mock import mock

from messente.verigator import exceptions, client


@mock()
class TestRestClient(TestCase):
    def setUp(self):
        self.rest_client = client.RestClient("http://test", "test", "test")

        self.valid_headers = {
            "X-Service-Auth": "test:test"
        }

        self.valid_get_headers = self.valid_headers
        self.valid_post_headers = {
            "X-Service-Auth": "test:test",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        self.sample_response = {
            "foo": "bar"
        }

    def test_auth_header(self, request_mocker):
        request_mocker.get("http://test/", request_headers=self.valid_headers, json={})

        self.rest_client.get("")
        self.assertTrue(request_mocker.called)

    def test_get(self, request_mocker):
        request_mocker.get("http://test/test?foo=bar", complete_qs=True, request_headers={"foo": "bar"},
                           json=self.sample_response)
        json = self.rest_client.get("test", params={"foo": "bar"}, headers={"foo": "bar"})
        self.assertTrue(request_mocker.called)
        self.assertEqual(json, self.sample_response)

    def test_post(self, request_mocker):
        request_mocker.post("http://test/test", json=self.sample_response, request_headers=self.valid_post_headers)

        json = self.rest_client.post("test", json=self.sample_response)

        self.assertTrue(request_mocker.called)
        self.assertEqual(json, self.sample_response)
        self.assertEqual(request_mocker.request_history[0].json(), self.sample_response)

    def test_put(self, request_mocker):
        request_mocker.put("http://test/test", json=self.sample_response, request_headers=self.valid_post_headers)

        json = self.rest_client.put("test", json=self.sample_response)

        self.assertTrue(request_mocker.called)
        self.assertEqual(json, self.sample_response)
        self.assertEqual(request_mocker.request_history[0].json(), self.sample_response)

    def test_delete(self, request_mocker):
        request_mocker.delete("http://test/test", json=self.sample_response, request_headers=self.valid_headers)

        json = self.rest_client.delete("test")
        self.assertTrue(request_mocker.called)
        self.assertEqual(json, self.sample_response)

    def test_raises_internal_server_error(self, request_mocker):
        self._register_addresses(request_mocker, 500)

        self.assertRaises(exceptions.InternalError, self.rest_client.get, "test")
        self.assertRaises(exceptions.InternalError, self.rest_client.post, "test")
        self.assertRaises(exceptions.InternalError, self.rest_client.put, "test")
        self.assertRaises(exceptions.InternalError, self.rest_client.delete, "test")

    def test_raises_bad_request_error(self, request_mocker):
        self._register_addresses(request_mocker, 400)

        self.assertRaises(exceptions.InvalidDataError, self.rest_client.get, "test")
        self.assertRaises(exceptions.InvalidDataError, self.rest_client.post, "test")
        self.assertRaises(exceptions.InvalidDataError, self.rest_client.put, "test")
        self.assertRaises(exceptions.InvalidDataError, self.rest_client.delete, "test")

    def test_raises_not_found_error(self, request_mocker):
        self._register_addresses(request_mocker, 404)

        self.assertRaises(exceptions.NoSuchResourceError, self.rest_client.get, "test")
        self.assertRaises(exceptions.NoSuchResourceError, self.rest_client.post, "test")
        self.assertRaises(exceptions.NoSuchResourceError, self.rest_client.put, "test")
        self.assertRaises(exceptions.NoSuchResourceError, self.rest_client.delete, "test")

    def test_raises_forbidden_error(self, request_mocker):
        self._register_addresses(request_mocker, 403)

        self.assertRaises(exceptions.ResourceForbiddenError, self.rest_client.get, "test")
        self.assertRaises(exceptions.ResourceForbiddenError, self.rest_client.post, "test")
        self.assertRaises(exceptions.ResourceForbiddenError, self.rest_client.put, "test")
        self.assertRaises(exceptions.ResourceForbiddenError, self.rest_client.delete, "test")

    def test_raises_unauthorized_error(self, request_mocker):
        self._register_addresses(request_mocker, 401)

        self.assertRaises(exceptions.WrongCredentialsError, self.rest_client.get, "test")
        self.assertRaises(exceptions.WrongCredentialsError, self.rest_client.post, "test")
        self.assertRaises(exceptions.WrongCredentialsError, self.rest_client.put, "test")
        self.assertRaises(exceptions.WrongCredentialsError, self.rest_client.delete, "test")

    def test_raises_confilct_error(self, request_mocker):
        self._register_addresses(request_mocker, 409)

        self.assertRaises(exceptions.ResourceAlreadyExistsError, self.rest_client.get, "test")
        self.assertRaises(exceptions.ResourceAlreadyExistsError, self.rest_client.post, "test")
        self.assertRaises(exceptions.ResourceAlreadyExistsError, self.rest_client.put, "test")
        self.assertRaises(exceptions.ResourceAlreadyExistsError, self.rest_client.delete, "test")

    def test_raises_any_error(self, request_mocker):
        self._register_addresses(request_mocker, 447)

        self.assertRaises(exceptions.VerigatorError, self.rest_client.get, "test")
        self.assertRaises(exceptions.VerigatorError, self.rest_client.post, "test")
        self.assertRaises(exceptions.VerigatorError, self.rest_client.put, "test")
        self.assertRaises(exceptions.VerigatorError, self.rest_client.delete, "test")

    @staticmethod
    def _register_addresses(request_mocker, code):
        request_mocker.register_uri('GET', 'http://test/test', json={}, status_code=code)
        request_mocker.register_uri('POST', 'http://test/test', json={}, status_code=code)
        request_mocker.register_uri('PUT', 'http://test/test', json={}, status_code=code)
        request_mocker.register_uri('DELETE', 'http://test/test', json={}, status_code=code)
