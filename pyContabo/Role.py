from .types.apiPermissions import apiPermissions
from typing import List


class Role:
    def __init__(self, json, _http):

        self._http = _http

        self.tenantId = json["tenantId"]
        self.customerId = json["customerId"]
        self.roleId = json["roleId"]
        self.name = json["name"]
        self.roleType = json["roleType"]
        self.apiPermissions = []
        self.resourcePermissions = []

        self.rawJson = json

    def update(
        self,
        name: str,
        resourcePermissions: List[int],
        apiPermissions: List[apiPermissions] = None,
        x_request_id: str = None,
        x_trace_id: str = None,
    ) -> bool:
        """updates name, API permissions and ressource permissions of the role"""

        data = {"name": name, "resourcePermissions": resourcePermissions}

        if apiPermissions:
            data["apiPermissions"] = []
            for i in apiPermissions:
                data["apiPermissions"].append(i.__dict__)

        resp = self._http.request(
            type="patch",
            url=f"https://api.contabo.com/v1/roles/{self.roleType}/{self.roleId}",
            data=data,
            x_request_id=x_request_id,
            x_trace_id=x_trace_id,
        )

        if resp.status_code == 200:
            return True
        return False

    def delete(self, x_request_id: str = None, x_trace_id: str = None) -> bool:
        """deletes the role"""

        resp = self._http.request(
            type="delete",
            url=f"https://api.contabo.com/v1/roles/{self.roleType}/{self.roleId}",
            x_request_id=x_request_id,
            x_trace_id=x_trace_id,
        )

        if resp.status_code == 204:
            return True
        return False
