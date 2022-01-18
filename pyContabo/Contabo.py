from .Instances import Instances
from .Secrets import Secrets

class contabo:

    def __init__(self, client_id, client_secret, api_user, api_password):
        self._http = APIClient(client_id, client_secret, api_user, api_password)
        self.Instances = Instances(self._http)
        self.Secrets = Secrets(self._http)