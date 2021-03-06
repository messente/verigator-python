from unittest import TestCase

import requests_mock
from messente.verigator import exceptions, client


@requests_mock.mock()
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

    def test_raises_errors(self, request_mocker):
        self._assertAllRoutesRaises(exceptions.InternalError, request_mocker, 500)
        self._assertAllRoutesRaises(exceptions.InvalidDataError, request_mocker, 400)
        self._assertAllRoutesRaises(exceptions.WrongCredentialsError, request_mocker, 401)
        self._assertAllRoutesRaises(exceptions.ResourceForbiddenError, request_mocker, 403)
        self._assertAllRoutesRaises(exceptions.NoSuchResourceError, request_mocker, 404)
        self._assertAllRoutesRaises(exceptions.ResourceAlreadyExistsError, request_mocker, 409)
        self._assertAllRoutesRaises(exceptions.VerigatorError, request_mocker, 447)

    def test_non_json_response(self, request_mocker):
        request_mocker.register_uri('GET', "http://test/test", text="Some non json response", status_code=200)
        self.assertRaises(exceptions.InvalidResponseError, self.rest_client.get, "test")

    def _assertAllRoutesRaises(self, exception, request_mocker, code):
        self._register_addresses(request_mocker, code)

        self.assertRaises(exception, self.rest_client.get, "test")
        self.assertRaises(exception, self.rest_client.post, "test")
        self.assertRaises(exception, self.rest_client.put, "test")
        self.assertRaises(exception, self.rest_client.delete, "test")

    @staticmethod
    def _register_addresses(request_mocker, code):
        request_mocker.register_uri('GET', 'http://test/test', json={}, status_code=code)
        request_mocker.register_uri('POST', 'http://test/test', json={}, status_code=code)
        request_mocker.register_uri('PUT', 'http://test/test', json={}, status_code=code)
        request_mocker.register_uri('DELETE', 'http://test/test', json={}, status_code=code)
