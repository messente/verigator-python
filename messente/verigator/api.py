import routes
from client import RestClient
from controllers import Users, Services, Auth


class Api(object):
    """Main class for verigator api,
    contains references to other controllers

    Attributes:
        services (Services): controller for service resource
        users (Users): controller for user resource
        auth (Auth): controller for auth resource

    """

    def __init__(self, username, password, endpoint=routes.URL):

        """
        Initialize Verigator api
        Args:
            username (str): api username. Can be obtained from dashboard
            password (str): api password. Can be obtained from dashboard
            endpoint (str): api endpoint. Can be obtained from dashboard
        """
        client = RestClient(endpoint, username, password)
        self.users = Users(client)
        self.services = Services(client)
        self.auth = Auth(client)
