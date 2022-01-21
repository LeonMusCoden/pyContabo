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
        self.Audits = InstanceActionsAudits()

    def start(self):
        """starts the instance"""

        status = self._http.request(type="post",
                             url=f"https://api.contabo.com/v1/compute/instances/{str(self.instanceId)}/actions/start").status_code

        if status == 201:
            return True
        return False

    def stop(self):
        """stops the instance"""

        status = self._http.request(type="post",
                             url=f"https://api.contabo.com/v1/compute/instances/{str(self.instanceId)}/actions/stop").status_code

        if status == 201:
            return True
        return False

    def restart(self):
        """restarts the instance
        (technically, it's the same as start)"""

        status = self._http.request(type="post",
                             url=f"https://api.contabo.com/v1/compute/instances/{str(self.instanceId)}/actions/start").status_code

        if status == 201:
            return True
        return False

    def reinstall(self, imageId: str, sshKeys: List[int] = None, rootPassword: int = None, userData: str = None):
        """reinstalls the OS of the instance"""

        status = self._http.request(type="patch",
                             url=f"https://api.contabo.com/v1/compute/instances/{str(self.instanceId)}",
                             data={"imageId": imageId, "sshKeys": sshKeys, "rootPassword": rootPassword,
                                  "userData": userData}).status_code

        if status == 200:
            return True
        return False

    def cancel(self):
        """cancels the instance"""

        status = self._http.request(type="post",
                             url=f"https://api.contabo.com/v1/compute/instances/{str(self.instanceId)}/cancel").status_code

        if status == 200:
            return True
        return False
