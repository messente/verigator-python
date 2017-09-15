from functools import wraps

import routes
from models import Service, User
from .client import RestClient


def _validate_input(func):
    @wraps(func)
    def wrapper(*args):
        for arg in args[1:]:
            if not isinstance(arg, str):
                raise ValueError("{} should be string".format(arg))
        return func(*args)
    return wrapper


def _validate_client(func):
    @wraps(func)
    def wrapper(self, client):
        if not isinstance(client, RestClient):
            raise ValueError("client should be RestClient")
        return func(self, client)
    return wrapper


class Services(object):
    @_validate_client
    def __init__(self, client):
        self.client = client

    @_validate_input
    def create(self, domain, name):
        """Created ServiceController instance.

        Args:
            domain (str): The domain name.
            name (str): The name of the service.

        Returns:
            Service: created service

        """

        response = self.client.post(routes.CREATE_SERVICE, json={
            'fqdn': domain,
            'name': name
        })
        return self.__service_from_json(response)

    @_validate_input
    def get(self, id):
        """Returns service with a given id.

        Args:
            id (str): The id of the service

        Returns:
            Service: Queried service

        """
        response = self.client.get(routes.GET_SERVICE.format(id))

        return self.__service_from_json(response)

    @_validate_input
    def delete(self, id):
        """

        Args:
            id (str):

        Returns:
            bool:

        """
        self.client.delete(routes.DELETE_SERVICE.format(id))
        return True

    @staticmethod
    def __service_from_json(json):
        return Service(json['id'], json['ctime'], json['name'])


# noinspection PyShadowingBuiltins
class Users(object):
    @_validate_client
    def __init__(self, client):
        self.client = client

    @_validate_input
    def get_all(self, service_id):
        """

        Args:
            service_id (str): .

        Returns:
            list: The return value. True for success, False otherwise.

        """
        response = self.client.get(routes.GET_USERS.format(service_id))

        print(response)
        return [self.__user_from_json(user) for user in response['users']]

    @_validate_input
    def get(self, service_id, id):
        """

        :param id:
        :param service_id:
        """
        response = self.client.get(routes.GET_USER.format(service_id, id))
        return self.__user_from_json(response)

    @_validate_input
    def create(self, service_id, number, username):
        """

        :param username:
        :param number:
        :param service_id: Service
        """

        response = self.client.post(routes.CREATE_USER.format(service_id), json={
            "phone_number": number,
            "id_in_service": username
        })
        return self.__user_from_json(response)

    @_validate_input
    def delete(self, service_id, id):
        """

        :param id:
        :param service_id:
        """
        self.client.delete(routes.DELETE_USER.format(service_id, id))

        return True

    @staticmethod
    def __user_from_json(json):
        return User(json['id'], json['ctime'], json['id_in_service'])


class Auth(object):
    METHOD_SMS = "sms"
    METHOD_TOTP = "totp"

    @_validate_client
    def __init__(self, client):
        self.client = client

    @_validate_input
    def initiate(self, service_id, user_id, method):
        response = self.client.post(routes.AUTH_INITIATE.format(service_id, user_id), json={
            "method": method
        })

        if response['method'] == "sms":
            return response['auth_id']

    @_validate_input
    def verify(self, service_id, user_id, method, token, auth_id=None):
        json = {"method": method, "token": token}

        if auth_id:
            json["auth_id"] = auth_id

        response = self.client.put(routes.AUTH_VERIFY.format(service_id, user_id), json=json)

        verified = response['verified']
        error = response.get('status', None)

        return verified, error
