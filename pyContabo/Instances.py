import json
from typing import List

from .Instance import Instance
from .errors import NotFound
from .types.licenses import license
from .types.products import product
from .types.regions import region
from .util import makeRequest, statusCheck


class Instances:

    def __init__(self, contabo):

        self.contabo = contabo

    def get(self, id=None, page=None, pageSize=None, orderByFields=None, orderBy=None, name=None, region=None,
            instanceId=None, status=None):

        if id:
            resp = makeRequest(type="get", url=f"https://api.contabo.com/v1/compute/instances/{id}",
                               access_token=self.contabo.access_token)

            statusCheck(resp.status_code)
            if resp.status_code == 404:
                raise NotFound("Instance", {"instanceId": id})

            return Instance(json=resp.json()["data"][0])  # TODO: Create Instance using JSON

        else:
            resp = makeRequest(type="get",
                               url=f"https://api.contabo.com/v1/compute/instances?page={page}&size={pageSize}&orderBy={orderByFields}:{orderBy}&name={name}&region={region}&instanceId={instanceId}&status={status}",
                               access_token=self.contabo.access_token)

            statusCheck(resp.status_code)
            data = resp.json()["data"]
            if len(data) == 0:
                raise NotFound("Instance", locals())

            instances = []
            for i in resp.json()["data"]:
                instances.append(Instance(json=i))  # TODO: Create Instance using JSON
            return instances

    def create(self, imageId: str, productId: product, region: region, period: int, sshKeys: List[int] = None,
               rootPassword: str = None, userData: str = None, licenseName: license = None):

        resp = makeRequest(type="post",
                           url="https://api.contabo.com/v1/compute/instances",
                           access_token=self.contabo.access_token,
                           data=json.dumps(
                               {"imageId": imageId, "productId": productId, "region": region, "sshKeys": sshKeys,
                                "rootPassword": rootPassword, "userData": userData, "license": license,
                                "period": period}))

        statusCheck(resp.status_code)

        # TODO: Return InstanceAudit object
        return resp.json()["data"][0]
