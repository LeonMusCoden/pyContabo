import requests
from requests.structures import CaseInsensitiveDict

from .errors import BadAuth


def init(client_id, client_secret, api_user, api_password):
    global credentials
    credentials = {
        "client_id": client_id,
        "client_secret": client_secret,
        "api_user": api_user,
        "api_password": api_password
    }
    global token
    token = updateToken()


def updateToken():
    url = "https://auth.contabo.com/auth/realms/contabo/protocol/openid-connect/token"
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    data = f"client_id={credentials['client_id']}&client_secret={credentials['client_secret']}&grant_type=password&username={credentials['api_user']}&password={credentials['api_password']}"
    resp = requests.post(url, headers=headers, data=data)

    if int(resp.status_code) == 200:
        return resp.json()["access_token"]
    else:
        raise BadAuth()
