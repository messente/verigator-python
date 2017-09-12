from client import RestClient
from controllers import Users, Services, Auth


class Api(object):
    def __init__(self, endpoint, username, password):
        """

        :type password: str
        :type username: str
        :type endpoint: str
        """
        client = RestClient(endpoint, username, password)
        self.users = Users(client)
        self.services = Services(client)
        self.auth = Auth(client)
