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
        """starts the instance"""

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
        """stops the instance"""

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
        """restarts the instance"""

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
        x_request_id: str = None,
        x_trace_id: str = None,
    ) -> bool:
        """reinstalls the OS of the instance"""

        resp = self._http.request(
            type="patch",
            url=f"https://api.contabo.com/v1/compute/instances/{str(self.instanceId)}",
            data={
                "imageId": imageId,
                "sshKeys": sshKeys,
                "rootPassword": rootPassword,
                "userData": userData,
            },
            x_request_id=x_request_id,
            x_trace_id=x_trace_id,
        )

        if resp.status_code == 200:
            return True
        return False

    def cancel(self, x_request_id: str = None, x_trace_id: str = None) -> bool:
        """cancels the instance"""

        resp = self._http.request(
            type="post",
            url=f"https://api.contabo.com/v1/compute/instances/{str(self.instanceId)}/cancel",
            x_request_id=x_request_id,
            x_trace_id=x_trace_id,
        )

        if resp.status_code == 200:
            return True
        return False
