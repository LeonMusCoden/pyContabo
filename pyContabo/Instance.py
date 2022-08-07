import json
from typing import List
import logging

from .audits.InstanceActionsAudits import InstanceActionsAudits
from .Snapshots import Snapshots

# _log = logging.getLogger(__name__)


class Instance:
    def __init__(self, json, _http):

        self._http = _http

        self.tenantId = json["tenantId"]
        self.customerId = json["customerId"]
        self.name = json["name"]
        self.instanceId = json["instanceId"]
        self.region = json["region"]
        self.ipv4 = json["ipConfig"]["v4"]["ip"]
        self.ipv6 = json["ipConfig"]["v6"]["ip"]
        self.macAddress = json["macAddress"]
        self.ramMb = json["ramMb"]
        self.cpuCores = json["cpuCores"]
        self.osType = json["osType"]
        self.diskMb = json["diskMb"]
        self.createdDate = json["createdDate"]
        self.cancelDate = json["cancelDate"]
        self.status = json["status"]
        self.vHostId = json["vHostId"]
        self.addOns = json["addOns"]
        self.productType = json["productType"]

        self.rawJson = json
        self.Snapshots = Snapshots(json["instanceId"], _http)
        self.Audits = InstanceActionsAudits(_http)

    def start(self, x_request_id: str = None, x_trace_id: str = None) -> bool:
        """Start a compute instance / resource.

        Examples:
            >>> instance.start()
            True

        Args:
            x_request_id: Uuid4 to identify individual requests for support cases.
            x_trace_id: Identifier to trace group of requests.

        Returns:
            Bool respresenting if the instance/ressource has been succesfully started.
        """

        resp = self._http.request(
            type="post",
            url=f"https://api.contabo.com/v1/compute/instances/{str(self.instanceId)}/actions/start",
            x_request_id=x_request_id,
            x_trace_id=x_trace_id,
        )

        if resp.status_code == 201:
            return True
        return False

    def stop(self, x_request_id: str = None, x_trace_id: str = None) -> bool:
        """stop a compute instance / resource.

        Examples:
            >>> instance.stop()
            True

        Args:
            x_request_id: Uuid4 to identify individual requests for support cases.
            x_trace_id: Identifier to trace group of requests.

        Returns:
            Bool respresenting if the instance/ressource has been succesfully stopped.
        """

        resp = self._http.request(
            type="post",
            url=f"https://api.contabo.com/v1/compute/instances/{str(self.instanceId)}/actions/stop",
            x_request_id=x_request_id,
            x_trace_id=x_trace_id,
        )

        if resp.status_code == 201:
            return True
        return False

    def restart(self, x_request_id: str = None, x_trace_id: str = None) -> bool:
        """Restart a compute instance / resource.

        Examples:
            >>> instance.restart()
            True

        Args:
            x_request_id: Uuid4 to identify individual requests for support cases.
            x_trace_id: Identifier to trace group of requests.

        Returns:
            Bool respresenting if the instance/ressource has been succesfully restarted.
        """

        resp = self._http.request(
            type="post",
            url=f"https://api.contabo.com/v1/compute/instances/{str(self.instanceId)}/actions/restart",
            x_request_id=x_request_id,
            x_trace_id=x_trace_id,
        )

        if resp.status_code == 201:
            return True
        return False

    def reinstall(
        self,
        imageId: str,
        sshKeys: List[int] = None,
        rootPassword: int = None,
        userData: str = None,
        defaultUser: str = None,
        x_request_id: str = None,
        x_trace_id: str = None,
    ) -> bool:
        """reinstall a specific instance with a new image and optionally add ssh keys, a root password or cloud-init.

        Examples:
            >>> instance.reinstall(imageId="3f184ab8-a600-4e7c-8c9b-3413e21a3752", sshKeys="[123, 125]", rootPassword=1, userData="#cloud-config", defaultUser="root")
            True

        Args:
            x_request_id: Uuid4 to identify individual requests for support cases.
            x_trace_id: Identifier to trace group of requests.
            imageId: ImageId to be used to setup the compute instance.
            sshKeys: Array of `secretIds` of public SSH keys for logging into as `defaultUser` with administrator/root privileges. Applies to Linux/BSD systems. Please refer to Secrets Management API.
            rootPassword: `secretId` of the password for the `defaultUser` with administrator/root privileges. For Linux/BSD please use SSH, for Windows RDP. Please refer to Secrets Management API.
            userData: Cloud-Init Config in order to customize during start of compute instance.
            defaultUser: Default user name created for login during (re-)installation with administrative privileges. Allowed values for Linux/BSD are `admin` (use sudo to apply administrative privileges like root) or `root`. Allowed values for Windows are `admin` (has administrative privileges like administrator) or `administrator`.

        Returns:
            Bool respresenting if the instance has been succesfully reinstalled.
        """

        resp = self._http.request(
            type="patch",
            url=f"https://api.contabo.com/v1/compute/instances/{str(self.instanceId)}",
            data={
                "imageId": imageId,
                "sshKeys": sshKeys,
                "rootPassword": rootPassword,
                "userData": userData,
                "defaultUser": defaultUser
            },
            x_request_id=x_request_id,
            x_trace_id=x_trace_id,
        )

        if resp.status_code == 200:
            return True
        return False

    def cancel(self, x_request_id: str = None, x_trace_id: str = None) -> bool:
        """Cancel a compute instance.

        Examples:
            >>> instance.cancel()
            True

        Args:
            x_request_id: Uuid4 to identify individual requests for support cases.
            x_trace_id: Identifier to trace group of requests.

        Returns:
            Bool respresenting if the instance has been succesfully cancelled.
        """

        resp = self._http.request(
            type="post",
            url=f"https://api.contabo.com/v1/compute/instances/{str(self.instanceId)}/cancel",
            x_request_id=x_request_id,
            x_trace_id=x_trace_id,
        )

        if resp.status_code == 200:
            return True
        return False
