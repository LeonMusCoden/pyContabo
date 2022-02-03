from .Instances import Instances
from .Secrets import Secrets
from .Images import Images
from .Tags import Tags
from .Users import Users
from .Roles import Roles
from .util.http import APIClient


class contabo:

    def __init__(self, client_id, client_secret, api_user, api_password):
        self._http = APIClient(client_id, client_secret, api_user, api_password)
        self.Instances = Instances(self._http)
        self.Secrets = Secrets(self._http)
        self.Images = Images(self._http)
        self.Tags = Tags(self._http)
        self.Users = Users(self._http)
        self.Roles = Roles(self._http)
