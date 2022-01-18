from .Instances import Instances
from .Secrets import Secrets
from .http import APIClient

class contabo:

    def __init__(self, client_id, client_secret, api_user, api_password):
        self._http = APIClient(client_id, client_secret, api_user, api_password)
        self.Instances = Instances(self._http)
        self.Secrets = Secrets(self._http)