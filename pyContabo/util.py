import uuid
from random import randint

import requests
from requests.structures import CaseInsensitiveDict

from .errors import *
from . import auth

def makeRequest(type, url, data=None):  # Might implement getToken here, I don't know
    """Makes the API request except for getToken()"""

    if data is None:
        data = {}

    headers = CaseInsensitiveDict()
    headers["Authorization"] = f"Bearer {auth.token}"
    headers["x-request-id"] = str(uuid.uuid4())
    headers["x-trace-id"] = str(randint(100000, 999999))

    if type == "get":
        headers["Content-Type"] = "application/json"
        return requests.get(url, headers=headers)

    elif type == "post":
        # headers["Content-Length"] = "0"
        headers["Content-Type"] = "application/json"
        if data:
            return requests.post(url, headers=headers, data=data)
        else:
            return requests.post(url, headers=headers)

    elif type == "delete":
        headers["Content-Type"] = "application/json"
        return requests.delete(url, headers=headers)

    elif type == "patch":
        headers["Content-Type"] = "application/json"
        return requests.patch(url, headers=headers, data=data)


def statusCheck(status):
    """replacement for a bunch of resp.status_code everywhere"""

    print(status)
    if status == 401:
        raise BadAuth()
    if status == 409:
        raise ConflictingRessources()
    elif status == 429:
        raise RateLimitReached()
    elif status == 500:
        raise ServerError()
