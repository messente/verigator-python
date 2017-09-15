import unittest
from unittest import TestCase

from requests_mock import mock
from messente.verigator.exceptions import *
from messente.verigator.client import RestClient


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

        self.assertRaises(InternalError, self.client.get, "test")
        self.assertRaises(InternalError, self.client.post, "test")
        self.assertRaises(InternalError, self.client.put, "test")
        self.assertRaises(InternalError, self.client.delete, "test")

    def test_raises_bad_request_error(self, request_mocker):
        self._register_addresses(request_mocker, 400)

        self.assertRaises(InvalidDataError, self.client.get, "test")
        self.assertRaises(InvalidDataError, self.client.post, "test")
        self.assertRaises(InvalidDataError, self.client.put, "test")
        self.assertRaises(InvalidDataError, self.client.delete, "test")

    def test_raises_not_found_error(self, request_mocker):
        self._register_addresses(request_mocker, 404)

        self.assertRaises(NoSuchResourceError, self.client.get, "test")
        self.assertRaises(NoSuchResourceError, self.client.post, "test")
        self.assertRaises(NoSuchResourceError, self.client.put, "test")
        self.assertRaises(NoSuchResourceError, self.client.delete, "test")

    def test_raises_forbidden_error(self, request_mocker):
        self._register_addresses(request_mocker, 403)

        self.assertRaises(ResourceForbiddenError, self.client.get, "test")
        self.assertRaises(ResourceForbiddenError, self.client.post, "test")
        self.assertRaises(ResourceForbiddenError, self.client.put, "test")
        self.assertRaises(ResourceForbiddenError, self.client.delete, "test")

    def test_raises_unauthorized_error(self, request_mocker):
        self._register_addresses(request_mocker, 401)

        self.assertRaises(WrongCredentialsError, self.client.get, "test")
        self.assertRaises(WrongCredentialsError, self.client.post, "test")
        self.assertRaises(WrongCredentialsError, self.client.put, "test")
        self.assertRaises(WrongCredentialsError, self.client.delete, "test")

    def test_raises_confilct_error(self, request_mocker):
        self._register_addresses(request_mocker, 409)

        self.assertRaises(ResourceAlreadyExistsError, self.client.get, "test")
        self.assertRaises(ResourceAlreadyExistsError, self.client.post, "test")
        self.assertRaises(ResourceAlreadyExistsError, self.client.put, "test")
        self.assertRaises(ResourceAlreadyExistsError, self.client.delete, "test")

    def test_raises_any_error(self, request_mocker):
        self._register_addresses(request_mocker, 447)

        self.assertRaises(VerigatorError, self.client.get, "test")
        self.assertRaises(VerigatorError, self.client.post, "test")
        self.assertRaises(VerigatorError, self.client.put, "test")
        self.assertRaises(VerigatorError, self.client.delete, "test")

    @staticmethod
    def _register_addresses(request_mocker, code):
        request_mocker.register_uri('GET', 'http://test/test', json={}, status_code=code)
        request_mocker.register_uri('POST', 'http://test/test', json={}, status_code=code)
        request_mocker.register_uri('PUT', 'http://test/test', json={}, status_code=code)
        request_mocker.register_uri('DELETE', 'http://test/test', json={}, status_code=code)
