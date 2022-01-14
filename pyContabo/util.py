import uuid
from random import randint

import requests
from requests.structures import CaseInsensitiveDict

from . import auth
from .errors import *


def makeRequest(type: str, url: str, data: dict=None, x_request_id: str=None, x_trace_id: str=None):  # Might implement getToken here, I don't know
    """Makes the API request except for getToken()"""

    if not x_request_id:
        x_request_id = str(uuid.uuid4())
    if not x_trace_id:
        x_trace_id = str(randint(100000, 999999))

    headers = CaseInsensitiveDict()
    headers["Authorization"] = f"Bearer {auth.token}"
    headers["x-request-id"] = x_request_id
    headers["x-trace-id"] = x_trace_id
    if type in ["get", "post"]:
        headers["Content-Type"] = "application/json"

    if data:
        return requests.request(type.capitalize(), url, headers=headers, data=data)
    return requests.request(type.capitalize(), url, headers=headers)


def statusCheck(status):
    """replacement for a bunch of resp.status_code everywhere"""

    if status == 401:
        raise BadAuth()
    elif status == 409:
        raise ConflictingRessources()
    elif status == 429:
        raise RateLimitReached()
    elif status == 500:
        raise ServerError()

