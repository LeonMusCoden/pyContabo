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
        admin: bool,
        accessAllResources: bool,
        apiPermissions: List[apiPermissions] = None,
        x_request_id: str = None,
        x_trace_id: str = None,
    ) -> bool:
        """Update attributes to your role. Attributes are optional. If not set, the attributes will retain their original values.

        Examples:
            >>> role.update(name="aRole", admin=True, accessAllResources=True, apiPermissions=apiPermissions)
            True

        Args:
            x_request_id: Uuid4 to identify individual requests for support cases.
            x_trace_id: Identifier to trace group of requests.
            name: The name of the role. There is a limit of 255 characters per role.
            admin: If user is admin he will have permissions to all API endpoints and resources. Enabling this will superseed all role definitions and `accessAllResources`.
            accessAllResources: Allow access to all resources. This will superseed all assigned resources in a role
            apiPermissions: Array of apiPermissions

        Returns:
            Bool respresenting if the role has been succesfully updated.
        """

        data = {"name": name, "admin": admin, "accessAllResources": accessAllResources}

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
        """deletes the image

        Examples:
            >>> role.delete()
            True

        Args:
            x_request_id: Uuid4 to identify individual requests for support cases.
            x_trace_id: Identifier to trace group of requests.

        Returns:
            Bool respresenting if the role has been succesfully deleted.
        """

        resp = self._http.request(
            type="delete",
            url=f"https://api.contabo.com/v1/roles/{self.roleType}/{self.roleId}",
            x_request_id=x_request_id,
            x_trace_id=x_trace_id,
        )

        if resp.status_code == 204:
            return True
        return False
