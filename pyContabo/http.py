import requests
from requests.structures import CaseInsensitiveDict
from time import time
from uuid import uuid4
from random import randint

from .errors import BadAuth

class APIClient:

    def __init__(self, client_id, client_secret, api_user, api_password):
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_user = api_user
        self.api_password = api_password
        self.expiration = 0
        self.bearer = None

    def getBearer(self):

        url = "https://auth.contabo.com/auth/realms/contabo/protocol/openid-connect/token"
        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        data = f"client_id={self.client_id}&client_secret={self.client_secret}&grant_type=password&username={self.api_user}&password={self.api_password}"
        resp = requests.post(url, headers=headers, data=data)

        if int(resp.status_code) == 200:
            self.expiration = time() + 300
            return resp.json()["access_token"]
        else:
            raise BadAuth()

    class Decorators():
        @staticmethod
        def refreshBearer(decorated):
            # the function that is used to check
            # the JWT and refresh if necessary
            def wrapper(self, *args, **kwargs):
                if time() > self.expiration:
                    self.bearer = self.getBearer()
                return decorated(self, *args, **kwargs)

            return wrapper

    @Decorators.refreshBearer
    def request(self, type: str, url: str, data: dict=None, x_request_id: str=None, x_trace_id: str=None):
        """Makes the API request except for getToken()"""

        if not x_request_id:
            x_request_id = str(uuid4())
        if not x_trace_id:
            x_trace_id = str(randint(100000, 999999))

        headers = CaseInsensitiveDict()
        headers["Authorization"] = f"Bearer {self.bearer}"
        headers["x-request-id"] = x_request_id
        headers["x-trace-id"] = x_trace_id
        if type in ["get", "post"]:
            headers["Content-Type"] = "application/json"

        if data:
            return requests.request(type.capitalize(), url, headers=headers, data=data)
        return requests.request(type.capitalize(), url, headers=headers)

