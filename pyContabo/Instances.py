import json
from typing import List
import logging


from .Instance import Instance
from .InstancesAudits import InstancesAudits
from .types.licenses import license
from .types.products import product
from .types.regions import region

# _log = logging.getLogger(__name__)


class Instances:

    def __init__(self, _http):

        self.Audits = InstancesAudits(_http)
        self._http = _http

    def get(self, id=None, page=None, pageSize=None, orderBy=None, name=None, region=None,
            instanceId=None, status=None):
        """gets any instance by id or other parameters through the paging system"""

        if id:
            resp = self._http.request(type="get",
                               url=f"https://api.contabo.com/v1/compute/instances/{id}")

            if resp.status_code == 404:
                return []

            # _log.info("fetched instance with id=%s", id)
            return Instance(resp.json()["data"][0], self._http)

        else:
            url = f"https://api.contabo.com/v1/compute/instances?{f'page={page}&' if page is not None else ''}{f'size={pageSize}&' if pageSize is not None else ''}{f'orderBy={orderBy}&' if orderBy is not None else ''}{f'name={name}&' if name is not None else ''}{f'region={region}&' if region is not None else ''}{f'instanceId={instanceId}&' if instanceId is not None else ''}{f'status={status}&' if status is not None else ''}"
            url = url[:-1]
            resp = self._http.request(type="get",
                               url=url)

            data = resp.json()["data"]
            if len(data) == 0:
                return []

            instances = []
            for i in data:
                instances.append(Instance(i, self._http))

            # _log.info("fetched %s instances with page=%s pageSize=%s orderByField=%s orderBy=%s name=%s region=%s instanceId=%s status=%s", len(instances), page, pageSize, orderByField, orderBy, name, region, instanceId, status)

            return instances

    def create(self, imageId: str, productId: product, region: region, period: int, sshKeys: List[int] = [],
               rootPassword: str = "", userData: str = "", licenseName: license = None):
        """creates a new instance"""

        resp = self._http.request(type="post",
                           url="https://api.contabo.com/v1/compute/instances",
                           data={"imageId": imageId, "productId": productId, "region": region, "sshKeys": sshKeys,
                                "rootPassword": rootPassword, "userData": userData, "license": licenseName,
                                "period": period})

        # _log.info("created new instance with imageId=%s productId=%s region=%s period=%s sshKeys=%s rootPassword=%s userData=%s, licenseName=%s", imageId, productId, region, period, sshKeys, rootPassword, userData, licenseName)

        if resp.status_code == 201:
            return True
        return False
