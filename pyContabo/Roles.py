import json

from .Role import Role
from .audits.RolesAudits import RolesAudits
from .types.apiPermissions import apiPermissions


class Roles:

    def __init__(self, _http):

        self._http = _http
        self.Audits = RolesAudits(_http)

    def get(self, roleType: str, id: str = None, page: int = None, pageSize: int = None,
            orderBy: str = None, name: str = None, apiName: str = None, tagName: str = None):
        """gets any role by id or other parameters through the paging system"""

        if id:
            resp = self._http.request(type="get",
                               url=f"https://api.contabo.com/v1/roles/{roleType}/{id}")

            if resp.status_code == 404:
                return []

            return Role(resp.json()["data"][0], self._http)

        else:
            url = f"https://api.contabo.com/v1/roles/{roleType}?{f'page={page}&' if page is not None else ''}{f'size={pageSize}&' if pageSize is not None else ''}{f'orderBy={orderBy}&' if orderBy is not None else ''}{f'name={name}&' if name is not None else ''}{f'apiName={apiName}&' if apiName is not None else ''}{f'tagName={tagName}&' if tagName is not None else ''}"
            url = url[:-1]
            resp = self._http.request(type="get",
                               url=url)

            data = resp.json()["data"]
            if len(data) == 0:
                return []

            roles = []
            for i in resp.json()["data"]:
                roles.append(Role(i, self._http))
            return roles

    def create(self, roleType: str, name: str, resourcePermissions: List[int], apiPermissions: List[apiPermissions] = None):
        """creates a new role"""

        data = {"name": name, "resourcePermissions": resourcePermissions}

        if apiPermissions:
            data["apiPermissions"] = []
            for i in apiPermissions:
                data["apiPermissions"].append(i.__dict__)

        resp = self._http.request(type="post",
                           url=f"https://api.contabo.com/v1/roles/{roleType}",
                           data=data)

        if resp.status_code == 201:
            return True
        return False

    def getApiPermissions(self, page: int = None, pageSize: int = None,
            orderBy: str = None, apiName: str = None):
        """Lists all available API permissions"""

        url = f"https://api.contabo.com/v1/roles/api-permissions?{f'page={page}&' if page is not None else ''}{f'size={pageSize}&' if pageSize is not None else ''}{f'orderBy={orderBy}&' if orderBy is not None else ''}{f'apiName={apiName}&' if apiName is not None else ''}"
        url = url[:-1]
        resp = self._http.request(type="get",
                                  url=url)

        data = resp.json()["data"]
        if len(data) == 0:
            return []

        permissions = []
        for i in resp.json()["data"]:
            permissions.append(apiPermissions(i))
        return permissions

