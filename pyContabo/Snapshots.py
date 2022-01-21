import json

from .Snapshot import Snapshot
from .audits.SnapshotsAudits import SnapshotsAudits


class Snapshots:

    def __init__(self, instanceId: int, _http):

        self._http = _http
        self.instanceId = instanceId
        self.Audits = SnapshotsAudits(_http)

    def get(self, id: str = None, page: int = None, pageSize: int = None,
            orderBy: str = None, name: str = None):
        """gets any snapshot by id or other parameters through the paging system"""

        if id:
            resp = self._http.request(type="get",
                               url=f"https://api.contabo.com/v1/compute/instances/{self.instanceId}/snapshots/{id}")

            if resp.status_code == 404:
                return []

            return Snapshot(resp.json()["data"][0], self._http)

        else:
            url = f"https://api.contabo.com/v1/compute/instances/{self.instanceId}/snapshots?{f'page={page}&' if page is not None else ''}{f'size={pageSize}&' if pageSize is not None else ''}{f'orderBy={orderBy}&' if orderBy is not None else ''}{f'name={name}&' if name is not None else ''}"
            url = url[:-1]
            resp = self._http.request(type="get",
                               url=url)

            data = resp.json()["data"]
            if len(data) == 0:
                return []

            snapshots = []
            for i in resp.json()["data"]:
                snapshots.append(Snapshot(i, self._http))
            return snapshots

    def create(self, name: str, description: str = None):
        """creates a new snapshot using name and desc."""

        if description:
            data = json.dumps({"name": name, "description": description})
        else:
            data = json.dumps({"name": name})

        resp = self._http.request(type="post",
                           url=f"https://api.contabo.com/v1/compute/instances/{self.instanceId}/snapshots",
                           data=data)

        print(resp.json())

        if resp.status_code == 201:
            return True
        return False
