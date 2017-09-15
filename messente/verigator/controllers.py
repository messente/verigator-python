import routes
from models import Service, User


class Services(object):
    def __init__(self, client):
        self.client = client

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

    def get(self, id):
        """Returns service with a given id.

        Args:
            id (str): The id of the service

        Returns:
            Service: Queried service

        """
        response = self.client.get(routes.GET_SERVICE.format(id))

        return self.__service_from_json(response)

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
    def __init__(self, client):
        self.client = client

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

    def get(self, service_id, id):
        """

        :param id:
        :param service_id:
        """
        response = self.client.get(routes.GET_USER.format(service_id, id))
        return self.__user_from_json(response)

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

    def __init__(self, client):
        self.client = client

    def initiate(self, service_id, user_id, method):
        response = self.client.post(routes.AUTH_INITIATE.format(service_id, user_id), json={
            "method": method
        })

        if response['method'] == "sms":
            return response['auth_id']

    def verify(self, service_id, user_id, method, token, auth_id=None):
        json = {"method": method, "token": token}

        if auth_id:
            json["auth_id"] = auth_id

        response = self.client.put(routes.AUTH_VERIFY.format(service_id, user_id), json=json)

        verified = response['verified']
        error = response.get('status', None)

        return verified, error
