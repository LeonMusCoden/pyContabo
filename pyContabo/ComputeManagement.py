from .Instances import Instances


class computeMagement:

    def __init__(self, access_token):

        self.access_token = access_token
        self.Instances = Instances(access_token)