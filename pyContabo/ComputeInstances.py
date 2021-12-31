from . import auth
from .Instances import Instances


class computeInstances:

    def __init__(self, client_id, client_secret, api_user, api_password):
        auth.init(client_id, client_secret, api_user, api_password)
        self.Instances = Instances()

    def updateToken(self):
        auth.token = auth.updateToken()
