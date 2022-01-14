from . import auth
from .Instances import Instances
from .http import APIClient


class computeInstances:

    def __init__(self, client_id, client_secret, api_user, api_password):
        self.http = APIClient(client_id, client_secret, api_user, api_password)
        self.Instances = Instances(self.http)
