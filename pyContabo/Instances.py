import json
from typing import List

from .Instance import Instance
from .InstancesAudits import InstancesAudits
from .errors import NotFound
from .types.licenses import license
from .types.products import product
from .types.regions import region


class Instances:

    def __init__(self, _http):

        self.Audits = InstancesAudits(_http)
        self._http = _http

    def get(self, id=None, page=None, pageSize=None, orderByFields=None, orderBy=None, name=None, region=None,
            instanceId=None, status=None):
        """gets any snapshot by id or other parameters through the paging system"""

        if id:
            resp = self._http.request(type="get",
                               url=f"https://api.contabo.com/v1/compute/instances/{id}")

            if resp.status_code == 404:
                raise NotFound("Instance", {"instanceId": id})

            return Instance(resp.json()["data"][0], self._http)

        else:
            url = f"https://api.contabo.com/v1/compute/instances?{f'page={page}&' if page is not None else ''}{f'size={pageSize}&' if pageSize is not None else ''}{f'orderBy={orderByFields}:{orderBy}&' if orderByFields is not None else ''}{f'name={name}&' if name is not None else ''}{f'region={region}&' if region is not None else ''}{f'instanceId={instanceId}&' if instanceId is not None else ''}{f'status={status}&' if status is not None else ''}"
            url = url[:-1]
            resp = self._http.request(type="get",
                               url=url)

            data = resp.json()["data"]
            if len(data) == 0:
                raise NotFound("Instance")

            instances = []
            for i in resp.json()["data"]:
                instances.append(Instance(i, self._http))
            return instances

    def create(self, imageId: str, productId: product, region: region, period: int, sshKeys: List[int] = [],
               rootPassword: str = "", userData: str = "", licenseName: license = None):
        """creates a new instance"""

        resp = self._http.request(type="post",
                           url="https://api.contabo.com/v1/compute/instances",
                           data={"imageId": imageId, "productId": productId, "region": region, "sshKeys": sshKeys,
                                "rootPassword": rootPassword, "userData": userData, "license": licenseName,
                                "period": period})

        print(resp.json())

        # TODO: Return InstanceAudit object
        if resp.status_code == 201:
            return True
        return False
