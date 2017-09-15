from unittest import TestCase

from mock import MagicMock

from messente.verigator.client import RestClient
from messente.verigator.controllers import Auth
from verigator import routes


class TestAuth(TestCase):
    def setUp(self):
        self.client = RestClient("http://test", "test", "test")
        self.auth = Auth(self.client)
        self.sms_init_response = {
            "method": "sms",
            "auth_id": "auth_id"
        }
        self.totp_init_response = {
            "method": "totp"
        }

        self.verified_response = {
            "verified": True
        }
        self.failed_response = {
            "verified": False,
            "status": {
                "throttled": False,
                "expired": False,
                "invalid": True,
                "result": "INVALID"
            },
        }

    def test_initiate_sms(self):
        self.client.post = MagicMock(return_value=self.sms_init_response)
        res = self.auth.initiate("sid", "uid", self.auth.METHOD_SMS)

        self.client.post.assert_called_with(routes.AUTH_INITIATE.format("sid", "uid"),
                                            json={"method": "sms"})
        self.assertEqual(res, self.sms_init_response['auth_id'])

    def test_initiate_totp(self):
        self.client.post = MagicMock(return_value=self.totp_init_response)
        res = self.auth.initiate("sid", "uid", self.auth.METHOD_TOTP)

        self.client.post.assert_called_with(routes.AUTH_INITIATE.format("sid", "uid"),
                                            json={"method": "totp"})
        self.assertIsNone(res)

    def test_verify_sms(self):
        self.client.put = MagicMock(return_value=self.verified_response)
        verified, error = self.auth.verify("sid", "uid", self.auth.METHOD_SMS, "token", "auth_id")

        self.client.put.assert_called_with(routes.AUTH_VERIFY.format("sid", "uid"),
                                           json={"method": "sms", "token": "token", "auth_id": "auth_id"})
        self.assertTrue(verified)

    def test_verify_totp(self):
        self.client.put = MagicMock(return_value=self.verified_response)
        verified, error = self.auth.verify("sid", "uid", self.auth.METHOD_TOTP, "token")

        self.client.put.assert_called_with(routes.AUTH_VERIFY.format("sid", "uid"),
                                           json={"method": "totp", "token": "token"})
        self.assertTrue(verified)

    def test_verify_failed(self):
        self.client.put = MagicMock(return_value=self.failed_response)
        verified, error = self.auth.verify("sid", "uid", self.auth.METHOD_TOTP, "token")

        self.client.put.assert_called_with(routes.AUTH_VERIFY.format("sid", "uid"),
                                           json={"method": "totp", "token": "token"})
        self.assertFalse(verified)

    def test_invalid_input(self):
        self.assertRaises(ValueError, Auth, None)
        self.assertRaises(ValueError, self.auth.initiate, None, None, None)
        self.assertRaises(ValueError, self.auth.verify, None, None, None, None)
