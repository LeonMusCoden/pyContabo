import json
from typing import List, Union

from .User import User
from .audits.UsersAudits import UsersAudits


class Users:
    def __init__(self, _http):

        self._http = _http
        self.Audits = UsersAudits(_http)

    def get(
        self,
        id: str = None,
        page: int = None,
        pageSize: int = None,
        orderBy: str = None,
        email: str = None,
        enabled: bool = None,
        x_request_id: str = None,
        x_trace_id: str = None,
    ) -> Union[User, List[User]]:
        """gets any user by id or other parameters through the paging system"""

        if id:
            resp = self._http.request(
                type="get",
                url=f"https://api.contabo.com/v1/users/{id}",
                x_request_id=x_request_id,
                x_trace_id=x_trace_id,
            )

            if resp.status_code == 404:
                return []

            return User(resp.json()["data"][0], self._http)

        else:
            url = f"https://api.contabo.com/v1/compute/instances/{self.instanceId}/snapshots?{f'page={page}&' if page is not None else ''}{f'size={pageSize}&' if pageSize is not None else ''}{f'orderBy={orderBy}&' if orderBy is not None else ''}{f'email={email}&' if email is not None else ''}{f'enabled={enabled}&' if enabled is not None else ''}"
            url = url[:-1]
            resp = self._http.request(
                type="get", url=url, x_request_id=x_request_id, x_trace_id=x_trace_id
            )

            data = resp.json()["data"]
            if len(data) == 0:
                return []

            users = []
            for i in resp.json()["data"]:
                users.append(User(i, self._http))
            return users

    def create(
        self,
        firstName: str,
        lastName: str,
        email: str,
        enabled: bool,
        totp: bool,
        admin: bool,
        accessAllResources: bool,
        locale: str,
        roles: List[int],
        x_request_id: str = None,
        x_trace_id: str = None,
    ) -> bool:
        """creates a new user using name and desc."""

        data = {
            "firstName": firstName,
            "lastName": lastName,
            "email": email,
            "enabled": enabled,
            "totp": totp,
            "admin": admin,
            "accessAllResources": accessAllResources,
            "locale": locale,
        }

        if roles:
            data.append(roles)

        resp = self._http.request(
            type="post",
            url=f"https://api.contabo.com/v1/users",
            data=json.dumps(data),
            x_request_id=x_request_id,
            x_trace_id=x_trace_id,
        )

        print(resp.json())

        if resp.status_code == 201:
            return True
        return False
