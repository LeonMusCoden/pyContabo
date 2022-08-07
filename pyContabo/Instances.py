import json
from typing import List, Union
import logging


from .Instance import Instance
from .audits.InstancesAudits import InstancesAudits
from .types.licenses import license
from .types.products import product
from .types.regions import region

# _log = logging.getLogger(__name__)


class Instances:
    def __init__(self, _http):

        self.Audits = InstancesAudits(_http)
        self._http = _http

    def get(
        self,
        id: str=None,
        page: int=None,
        pageSize: int=None,
        orderBy: str=None,
        name: str=None,
        region: str=None,
        instanceIds: str=None,
        status: str=None,
        x_request_id: str = None,
        x_trace_id: str = None,
    ) -> Union[Instance, List[Instance]]:
        """fetches any instances(s) by id or other parameters

        Examples:
            >>> Instances.get()
            [instance]
            >>> Instances.get(name="vmd12345", region="EU", status="provisioning")
            [instance]
            >>> Instances.get(id="100")
            instance

        Args:
            x_request_id: Uuid4 to identify individual requests for support cases.
            x_trace_id: Identifier to trace group of requests.
            id: The identifier of the instance
            page: Number of page to be fetched.
            pageSize: Number of elements per page.
            orderBy: Specify fields and ordering (ASC for ascending, DESC for descending) in following format `field:ASC|DESC`
            name: The name of the instance
            region: The Region of the instance
            instanceIds: Comma separated instances identifiers
            status: The status of the instance

        Returns:
            List of instances
        """

        if id:
            resp = self._http.request(
                type="get",
                url=f"https://api.contabo.com/v1/compute/instances/{id}",
                x_request_id=x_request_id,
                x_trace_id=x_trace_id,
            )

            if resp.status_code == 404:
                return []

            # _log.info("fetched instance with id=%s", id)
            return Instance(resp.json()["data"][0], self._http)

        else:
            url = f"https://api.contabo.com/v1/compute/instances?{f'page={page}&' if page is not None else ''}{f'size={pageSize}&' if pageSize is not None else ''}{f'orderBy={orderBy}&' if orderBy is not None else ''}{f'name={name}&' if name is not None else ''}{f'region={region}&' if region is not None else ''}{f'instanceIds={instanceIds}&' if instanceIds is not None else ''}{f'status={status}&' if status is not None else ''}"
            url = url[:-1]
            resp = self._http.request(
                type="get", url=url, x_request_id=x_request_id, x_trace_id=x_trace_id
            )

            data = resp.json()["data"]
            if len(data) == 0:
                return []

            instances = []
            for i in data:
                instances.append(Instance(i, self._http))

            # _log.info("fetched %s instances with page=%s pageSize=%s orderByField=%s orderBy=%s name=%s region=%s instanceId=%s status=%s", len(instances), page, pageSize, orderByField, orderBy, name, region, instanceId, status)

            return instances

    def create(
        self,
        imageId: str,
        productId: product,
        region: region,
        period: int,
        sshKeys: List[int] = [],
        rootPassword: str = "",
        userData: str = "",
        licenseName: license = None,
        displayName: str = None,
        defaultUser: str = None,
        x_request_id: str = None,
        x_trace_id: str = None,
    ) -> bool:
        """Creates a new instance

        Examples:
            >>> Instances.create(imageId="db1409d2-ed92-4f2f-978e-7b2fa4a1ec90", productId=product.P1, region=region.EU, period="1", licenseName=license.cPanel5)
            True

        Args:
            x_request_id: Uuid4 to identify individual requests for support cases.
            x_trace_id: Identifier to trace group of requests.
            imageId: ImageId to be used to setup the compute instance. Default is Ubuntu 20.04.
            productId: Product ID. Default is V1.
            region: Instance Region where the compute instance should be located. Default is EU.
            sshKeys: Array of `secretIds` of public SSH keys for logging into as `defaultUser` with administrator/root privileges. Applies to Linux/BSD systems. Please refer to Secrets Management API.
            rootPassword: `secretId` of the password for the `defaultUser` with administrator/root privileges. For Linux/BSD please use SSH, for Windows RDP. Please refer to Secrets Management API.
            userData: Cloud-Init Config in order to customize during start of compute instance.
            licenseName: Additional licence in order to enhance your chosen product, mainly needed for software licenses on your product (not needed for windows).
            period: Initial contract period in months. Available periods are: 1, 3, 6 and 12 months. Default to 1 month
            displayName: The display name of the instance
            defaultUser: Default user name created for login during (re-)installation with administrative privileges. Allowed values for Linux/BSD are `admin` (use sudo to apply administrative privileges like root) or `root`. Allowed values for Windows are `admin` (has administrative privileges like administrator) or `administrator`.

        Returns:
            Bool respresenting if the instance has been succesfully created.
        """

        resp = self._http.request(
            type="post",
            url="https://api.contabo.com/v1/compute/instances",
            data={
                "imageId": imageId,
                "productId": productId.name,
                "region": region.name,
                "sshKeys": sshKeys,
                "rootPassword": rootPassword,
                "userData": userData,
                "license": licenseName.name,
                "period": period,
                "displayName": displayName,
                "defaultUser": defaultUser
            },
            x_request_id=x_request_id,
            x_trace_id=x_trace_id,
        )

        # _log.info("created new instance with imageId=%s productId=%s region=%s period=%s sshKeys=%s rootPassword=%s userData=%s, licenseName=%s", imageId, productId, region, period, sshKeys, rootPassword, userData, licenseName)

        if resp.status_code == 201:
            return True
        return False
