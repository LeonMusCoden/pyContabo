import json
from .errors import NotFound
from .util import makeRequest, statusCheck
from .Snapshot import Snapshot


class Snapshots:

    def __init__(self, access_token: str, instanceId: int):

        self.access_token = access_token
        self.instanceId = instanceId

    def get(self, id=None, page=None, pageSize=None, orderByFields=None, orderBy=None, name=None):

        if id:
            resp = makeRequest(type="get",
                               url=f"https://api.contabo.com/v1/compute/instances/{self.instanceId}/snapshots/{id}",
                               access_token=self.access_token)

            statusCheck(resp.status_code)
            if resp.status_code == 404:
                raise NotFound("Snapshot", {"snapshotId": id})

            return Snapshot(resp.json()["data"][0], self.access_token)  # TODO: Create Snapshot using JSON

        else:
            url=f"https://api.contabo.com/v1/compute/instances/{self.instanceId}/snapshots?{f'page={page}&' if page is not None else ''}{f'size={pageSize}&' if pageSize is not None else ''}{f'orderBy={orderByFields}:{orderBy}&' if orderByFields is not None else ''}{f'name={name}&' if name is not None else ''}"
            url = url[:-1]
            resp = makeRequest(type="get",
                               url=url,
                               access_token=self.access_token)

            statusCheck(resp.status_code)
            data = resp.json()["data"]
            if len(data) == 0:
                raise NotFound("Snapshot")

            snapshots = []
            for i in resp.json()["data"]:
                snapshots.append(Snapshot(i, self.access_token))  # TODO: Create Snapshot using JSON
            return snapshots

    def create(self, name: str, description: str = ""):

        resp = makeRequest(type="post",
                           url=f"https://api.contabo.com/v1/compute/instances/{self.instanceId}/snapshots",
                           access_token=self.access_token,
                           data=json.dumps({"name": name, "description": description}))

        statusCheck(resp.status_code)
        print(resp.json())

        # TODO: Return SnapshotAudit object
        return resp.json()["data"][0]
