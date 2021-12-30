import json
from typing import List

from .Instance import Instance
from .errors import NotFound
from .types.licenses import license
from .types.products import product
from .types.regions import region
from .util import makeRequest, statusCheck
from .Snapshot import Snapshot


class Snapshots:

    def __init__(self, contabo, instanceId):

        self.contabo = contabo
        self.instanceId = instanceId

    def get(self, id=None, page=None, pageSize=None, orderByFields=None, orderBy=None, name=None, region=None,
            instanceId=None, status=None):

        if id:
            resp = makeRequest(type="get",
                               url=f"https://api.contabo.com/v1/compute/instances/{self.instanceId}/snapshots/{id}",
                               access_token=self.contabo.access_token)

            statusCheck(resp.status_code)
            if resp.status_code == 404:
                raise NotFound("Snapshot", {"snapshotId": id})

            return Snapshot(json=resp.json()["data"][0])  # TODO: Create Snapshot using JSON

        else:
            resp = makeRequest(type="get",
                               url=f"https://api.contabo.com/v1/compute/instances/{self.instanceId}/snapshots?page={page}&size={pageSize}&orderBy={orderByFields}:{orderBy}&name={name}",
                               access_token=self.contabo.access_token)

            statusCheck(resp.status_code)
            data = resp.json()["data"]
            if len(data) == 0:
                raise NotFound("Snapshot", locals())

            snapshots = []
            for i in resp.json()["data"]:
                snapshots.append(Snapshot(json=i))  # TODO: Create Snapshot using JSON
            return snapshots

    def create(self, name: str, description: str = None):

        resp = makeRequest(type="post",
                           url=f"https://api.contabo.com/v1/compute/instances/{self.instanceId}/snapshots",
                           access_token=self.contabo.access_token,
                           data=json.dumps({"name": name, "description": description}))

        statusCheck(resp.status_code)

        # TODO: Return SnapshotAudit object
        return resp.json()["data"][0]
