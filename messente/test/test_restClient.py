import unittest
from unittest import TestCase

from requests_mock import mock

from messente.verigator.client import *


@mock()
class TestRestClient(TestCase):
    def setUp(self):
        self.client = RestClient("http://test", "test", "test")

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

        self.client.get("")
        self.assertTrue(request_mocker.called)

    def test_get(self, request_mocker):
        request_mocker.get("http://test/test?foo=bar", complete_qs=True, request_headers={"foo": "bar"},
                           json=self.sample_response)
        json = self.client.get("test", params={"foo": "bar"}, headers={"foo": "bar"})
        self.assertTrue(request_mocker.called)
        self.assertEqual(json, self.sample_response)

    def test_post(self, request_mocker):
        request_mocker.post("http://test/test", json=self.sample_response, request_headers=self.valid_post_headers)

        json = self.client.post("test", json=self.sample_response)

        self.assertTrue(request_mocker.called)
        self.assertEqual(json, self.sample_response)
        self.assertEqual(request_mocker.request_history[0].json(), self.sample_response)

    def test_put(self, request_mocker):
        request_mocker.put("http://test/test", json=self.sample_response, request_headers=self.valid_post_headers)

        json = self.client.put("test", json=self.sample_response)

        self.assertTrue(request_mocker.called)
        self.assertEqual(json, self.sample_response)
        self.assertEqual(request_mocker.request_history[0].json(), self.sample_response)

    def test_delete(self, request_mocker):
        request_mocker.delete("http://test/test", json=self.sample_response, request_headers=self.valid_headers)

        json = self.client.delete("test")
        self.assertTrue(request_mocker.called)
        self.assertEqual(json, self.sample_response)

    def test_raises_internal_server_error(self, request_mocker):
        self._register_addresses(request_mocker, 500)
        self.assertRaises(InternalServerError, self.client.get, "test")
        self.assertRaises(InternalServerError, self.client.post, "test")
        self.assertRaises(InternalServerError, self.client.put, "test")
        self.assertRaises(InternalServerError, self.client.delete, "test")

    def test_raises_bad_request_error(self, request_mocker):
        self._register_addresses(request_mocker, 400)
        self.assertRaises(BadRequestError, self.client.get, "test")
        self.assertRaises(BadRequestError, self.client.post, "test")
        self.assertRaises(BadRequestError, self.client.put, "test")
        self.assertRaises(BadRequestError, self.client.delete, "test")

    def test_raises_not_found_error(self, request_mocker):
        self._register_addresses(request_mocker, 404)
        self.assertRaises(NotFoundError, self.client.get, "test")
        self.assertRaises(NotFoundError, self.client.post, "test")
        self.assertRaises(NotFoundError, self.client.put, "test")
        self.assertRaises(NotFoundError, self.client.delete, "test")

    def test_raises_forbidden_error(self, request_mocker):
        self._register_addresses(request_mocker, 403)
        self.assertRaises(ForbiddenError, self.client.get, "test")
        self.assertRaises(ForbiddenError, self.client.post, "test")
        self.assertRaises(ForbiddenError, self.client.put, "test")
        self.assertRaises(ForbiddenError, self.client.delete, "test")

    def test_raises_unauthorized_error(self, request_mocker):
        self._register_addresses(request_mocker, 401)
        self.assertRaises(UnauthorizedError, self.client.get, "test")
        self.assertRaises(UnauthorizedError, self.client.post, "test")
        self.assertRaises(UnauthorizedError, self.client.put, "test")
        self.assertRaises(UnauthorizedError, self.client.delete, "test")

    @staticmethod
    def _register_addresses(request_mocker, code):
        request_mocker.register_uri('GET', 'http://test/test', json={}, status_code=code)
        request_mocker.register_uri('POST', 'http://test/test', json={}, status_code=code)
        request_mocker.register_uri('PUT', 'http://test/test', json={}, status_code=code)
        request_mocker.register_uri('DELETE', 'http://test/test', json={}, status_code=code)


if __name__ == '__main__':
    unittest.main()
