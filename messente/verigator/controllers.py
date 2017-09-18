from functools import wraps

import routes
from models import Service, User
from .client import RestClient


def _validate_input(func):
    # decorator for validating that passed arguments are all string
    @wraps(func)
    def wrapper(*args):
        for arg in args[1:]:
            if not isinstance(arg, str):
                raise ValueError("{} should be string".format(arg))
        return func(*args)

    return wrapper


def _validate_client(func):
    # decorator for validating that passed client is RestClient
    @wraps(func)
    def wrapper(self, client):
        if not isinstance(client, RestClient):
            raise ValueError("client should be RestClient")
        return func(self, client)

    return wrapper


class Services(object):
    """
    Controller for service resource
    """

    @_validate_client
    def __init__(self, client):
        """

        Args:
            client (RestClient):
        """
        self.client = client

    @_validate_input
    def create(self, domain, name):
        """Creates new service.

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
        """Fetches service with a given id from the server.

        Args:
            id (str): The id of the service

        Returns:
            Service: Fetched service

        """
        response = self.client.get(routes.GET_SERVICE.format(id))

        return self.__service_from_json(response)

    @_validate_input
    def delete(self, id):
        """Deletes service with id

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
    """Controller for service resource
    """

    @_validate_client
    def __init__(self, client):
        """

        Args:
            client (RestClient):
        """
        self.client = client

    @_validate_input
    def get_all(self, service_id):
        """Fetches all users for the given service

        Args:
            service_id (str): service id to search users for

        Returns:
            list[User]: list of users

        """
        response = self.client.get(routes.GET_USERS.format(service_id))

        print(response)
        return [self.__user_from_json(user) for user in response['users']]

    @_validate_input
    def get(self, service_id, id):
        """Fetches single user with given id for the given service

        Args:
            service_id (str): service id
            id (str): user id

        Returns:
            User: fetched user

        """
        response = self.client.get(routes.GET_USER.format(service_id, id))
        return self.__user_from_json(response)

    @_validate_input
    def create(self, service_id, number, username):
        """Creates new user for the given service

        Args:
            service_id (str): service id
            number (str): users phone number, used for 2fa
            username (str): username

        Returns:
            User: created user

        """

        response = self.client.post(routes.CREATE_USER.format(service_id), json={
            "phone_number": number,
            "id_in_service": username
        })
        return self.__user_from_json(response)

    @_validate_input
    def delete(self, service_id, id):
        """Deleted user with given id for the given service

        Args:
            service_id (str): service id
            id (str): user id

        Returns:
            bool: True on success raises exception on error

        """
        self.client.delete(routes.DELETE_USER.format(service_id, id))

        return True

    @staticmethod
    def __user_from_json(json):
        return User(json['id'], json['ctime'], json['id_in_service'])


class Auth(object):
    """Controller for service resource

    """

    METHOD_SMS = "sms"
    METHOD_TOTP = "totp"

    @_validate_client
    def __init__(self, client):
        """

        Args:
            client (RestClient):
        """
        self.client = client

    @_validate_input
    def initiate(self, service_id, user_id, method):
        """Initiates authentication process
        sends sms in case of sms authentication

        Args:
            service_id (str): service id
            user_id (str): user id
            method (str): auth method (sms or totp) use Auth.METHOD_SMS or Auth.METHOD_TOTP

        Returns:
            str: auth_id if sms auth else None, raises exception on error

        """
        response = self.client.post(routes.AUTH_INITIATE.format(service_id, user_id), json={
            "method": method
        })

        if response['method'] == "sms":
            return response['auth_id']

    @_validate_input
    def verify(self, service_id, user_id, method, token, auth_id=None):
        """Verifies user input validity

        Args:
            service_id (str): service id
            user_id (str): user id
            method (str): auth method (sms or totp) use Auth.METHOD_SMS or Auth.METHOD_TOTP
            token (str): user provided token
            auth_id (str): in case of sms auth, auth_id you got when initiated authentication

        Returns:
            (bool, dict): boolean indicating verification status and error dict in case verification fails

        """
        json = {"method": method, "token": token}

        if auth_id:
            json["auth_id"] = auth_id

        response = self.client.put(routes.AUTH_VERIFY.format(service_id, user_id), json=json)

        verified = response['verified']
        error = response.get('status', None)

        return verified, error
