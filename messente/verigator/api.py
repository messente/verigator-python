import routes
from client import RestClient
from controllers import Users, Services, Auth


class Api(object):
    def __init__(self, username, password, endpoint=routes.URL):
        """

        :type password: str
        :type username: str
        :type endpoint: str
        """
        print(__name__)
        client = RestClient(endpoint, username, password)
        self.users = Users(client)
        self.services = Services(client)
        self.auth = Auth(client)
