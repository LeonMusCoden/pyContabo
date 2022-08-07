import json
from typing import List, Union

from .Role import Role
from .audits.RolesAudits import RolesAudits
from .types.apiPermissions import apiPermission


class Roles:
    def __init__(self, _http):

        self._http = _http
        self.Audits = RolesAudits(_http)

    def get(
        self,
        roleType: str,
        id: str = None,
        page: int = None,
        pageSize: int = None,
        orderBy: str = None,
        name: str = None,
        apiName: str = None,
        tagName: str = None,
        type: str = None,
        x_request_id: str = None,
        x_trace_id: str = None,
    ) -> Union[Role, List[Role]]:
        """fetches any role(s) by id or other parameters

        Examples:
            >>> Roles.get()
            [role]
            >>> Roles.get(name="roleName", apiName="/v1/compute/instances", tagName="Web", type="custom")
            [role]
            >>> Roles.get(id="12345")
            role

        Args:
            x_request_id: Uuid4 to identify individual requests for support cases.
            x_trace_id: Identifier to trace group of requests.
            id: The identifier of the role.
            name: The name of the role.
            apiName: The name of api.
            tagName: The name of the tag
            type: The type of the tag. Can be either `default` or `custom`
            page: Number of page to be fetched.
            pageSize: Number of elements per page.
            orderBy: Specify fields and ordering (ASC for ascending, DESC for descending) in following format `field:ASC|DESC`

        Returns:
            List of roles
        """

        if id:
            resp = self._http.request(
                type="get",
                url=f"https://api.contabo.com/v1/roles/{roleType}/{id}",
                x_request_id=x_request_id,
                x_trace_id=x_trace_id,
            )

            if resp.status_code == 404:
                return []

            return Role(resp.json()["data"][0], self._http)

        else:
            url = f"https://api.contabo.com/v1/roles/{roleType}?{f'page={page}&' if page is not None else ''}{f'size={pageSize}&' if pageSize is not None else ''}{f'orderBy={orderBy}&' if orderBy is not None else ''}{f'name={name}&' if name is not None else ''}{f'apiName={apiName}&' if apiName is not None else ''}{f'tagName={tagName}&' if tagName is not None else ''}{f'type={type}&' if type is not None else ''}"
            url = url[:-1]
            resp = self._http.request(
                type="get", url=url, x_request_id=x_request_id, x_trace_id=x_trace_id
            )

            data = resp.json()["data"]
            if len(data) == 0:
                return []

            roles = []
            for i in resp.json()["data"]:
                roles.append(Role(i, self._http))
            return roles

    def create(
        self,
        roleType: str,
        name: str,
        admin: bool,
        accessAllResources: bool,
        apiPermissions: List[apiPermission] = None,
        x_request_id: str = None,
        x_trace_id: str = None,
    ) -> bool:
        """Creates a new role

        Examples:
            >>> Roles.create(name="Web", admin=True, accessAllResources=True, apiPermissions=[apiPermission("infrastructure", ["CREATE", "READ"], resources=[1, 2, 3])])
            True

        Args:
            x_request_id: Uuid4 to identify individual requests for support cases.
            x_trace_id: Identifier to trace group of requests.
            name: The name of the role. There is a limit of 255 characters per role.
            admin: If user is admin he will have permissions to all API endpoints and resources. Enabling this will superseed all role definitions and `accessAllResources`.
            accessAllResources: Allow access to all resources. This will superseed all assigned resources in a role.
            apiPermissions: Array of apiPermissions.

        Returns:
            Bool respresenting if the role has been succesfully created.
        """

        data = {"name": name, "admin": admin, "accessAllResources": accessAllResources}

        if apiPermissions:
            data["apiPermissions"] = []
            for i in apiPermissions:
                data["apiPermissions"].append(i.__dict__)

        resp = self._http.request(
            type="post",
            url=f"https://api.contabo.com/v1/roles/{roleType}",
            data=data,
            x_request_id=x_request_id,
            x_trace_id=x_trace_id,
        )

        if resp.status_code == 201:
            return True
        return False

    def getApiPermissions(
        self,
        page: int = None,
        pageSize: int = None,
        orderBy: str = None,
        apiName: str = None,
        x_request_id: str = None,
        x_trace_id: str = None,
    ) -> List[apiPermission]:
        """List all available API permissions.

        Examples:
            >>> Roles.getApiPermissions(apiName="/v1/compute/instances")
            [permissions]

        Args:
            x_request_id: Uuid4 to identify individual requests for support cases.
            x_trace_id: Identifier to trace group of requests.
            page: Number of page to be fetched.
            pageSize: Number of elements per page.
            orderBy: Specify fields and ordering (ASC for ascending, DESC for descending) in following format `field:ASC|DESC`
            apiName: The name of api.

        Returns:
            List of permissions.
        """

        url = f"https://api.contabo.com/v1/roles/api-permissions?{f'page={page}&' if page is not None else ''}{f'size={pageSize}&' if pageSize is not None else ''}{f'orderBy={orderBy}&' if orderBy is not None else ''}{f'apiName={apiName}&' if apiName is not None else ''}"
        url = url[:-1]
        resp = self._http.request(
            type="get", url=url, x_request_id=x_request_id, x_trace_id=x_trace_id
        )

        data = resp.json()["data"]
        if len(data) == 0:
            return []

        permissions = []
        for i in resp.json()["data"]:
            permissions.append(apiPermission(i["apiName"], i["actions"]))
        return permissions
