import routes
from models import Service, User


# noinspection PyShadowingBuiltins
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

        data = {
            'fqdn': domain,
            'name': name
        }

        response = self.client.post(routes.CREATE_SERVICE, json=data)

        data = response.json()

        return Service(data['id'], data['ctime'], data['name'])

    def get(self, id):
        """Returns service with a given id.

        Args:
            id (str): The id of the service

        Returns:
            Service: Queried service

        """
        response = self.client.get(routes.GET_SERVICE.format(id))

        return self.__service_from_json(response.json())

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

    def get_all(self, service):
        """

        Args:
            service (str): .

        Returns:
            type: The return value. True for success, False otherwise.

        """
        response = self.client.get(routes.GET_USERS.format(service))

        data = response.json()

        return [self.__user_from_json(user) for user in data['users']]

    def get(self, service, id):
        """

        :param id:
        :param service:
        """
        response = self.client.get(routes.GET_USER.format(service.id, id))
        return self.__user_from_json(response.json())

    def create(self, service, number, username):
        """

        :param service: Service
        """
        response = self.client.post(routes.CREATE_USER.format(service.id), json={
            "phone_number": number,
            "id_in_service": username
        })
        return self.__user_from_json(response.json())

    def delete(self, service, id):
        """

        :param id:
        :param service:
        """
        self.client.delete(routes.DELETE_USER.format(service.id, id))

        return True

    @staticmethod
    def __user_from_json(json):
        return User(json['id'], json['ctime'], json['id_in_service'])


class Auth(object):
    METHOD_SMS = "sms"
    METHOD_TOTP = "totp"

    def __init__(self, client):
        self.client = client

    def initiate(self, service, user, method):
        response = self.client.post(routes.AUTH_INITIATE.format(service.id, user.id), json={
            "method": method
        })
        data = response.json()

        print(data)

        if data['method'] == "sms":
            return data['auth_id']

    def verify(self, service, user, method, token, auth_id=None):
        response = self.client.put(routes.AUTH_VERIFY.format(service.id, user.id), json={
            "method": method,
            "token": token,
            "auth_id": auth_id
        })

        return response.json()
