import json
import uuid
from random import randint

import requests
from requests.structures import CaseInsensitiveDict


def makeRequest(type, url, access_token, data=None):
    if data is None:
        data = {}

    headers = CaseInsensitiveDict()
    headers["Authorization"] = f"Bearer {access_token}"
    headers["x-request-id"] = str(uuid.uuid4())
    headers["x-trace-id"] = str(randint(100000, 999999))

    if type == "get":
        headers["Content-Type"] = "application/json"
        return requests.get(url, headers=headers)

    elif type == "post":
        headers["Content-Length"] = "0"
        return requests.post(url, headers=headers, data=data)

    elif type == "delete":
        headers["Content-Type"] = "application/json"
        return requests.get(url, headers=headers)


class computeInstances:

    def __init__(self, client_id, client_secret, api_user, api_password):

        self.client_id = client_id
        self.client_secret = client_secret
        self.api_user = api_user
        self.api_password = api_password

    def getToken(self):

        url = "https://auth.contabo.com/auth/realms/contabo/protocol/openid-connect/token"
        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        data = f"client_id={self.client_id}&client_secret={self.client_secret}&grant_type=password&username={self.api_user}&password={self.api_password}"
        resp = requests.post(url, headers=headers, data=data)

        if int(resp.status_code) == 200:
            self.access_token = resp.json()["access_token"]
            return self.access_token
        else:
            return resp.status_code

    def getInstances(self):

        resp = makeRequest(type="get", url="https://api.contabo.com/v1/compute/instances",
                           access_token=self.access_token)

        if int(resp.status_code) == 200:
            self.instaces = []
            for i in resp.json()["data"]:
                self.instaces.append(Instance(json=i))
            return self.instaces

        return resp.status_code

    def getInstanceById(self, id):

        resp = makeRequest(type="get", url=f"https://api.contabo.com/v1/compute/instances/{id}",
                           access_token=self.access_token)

        if int(resp.status_code) == 200:
            return Instance(json=resp.json()["data"][0])
        else:
            return resp.status_code


class Instance:

    def __init__(self, json=None):

        if json:
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

        self.snapshots = []

    def getSpecs(self):

        return (
            f"IPv4:\t{self.ipv4}\nCPU Cores:\t{self.cpuCores}\nRAM:\t{self.ramMb}\nDrive:\t{self.diskMb} ({self.productType})")

    def start(self):

        return makeRequest(type="post",
                           url=f"https://api.contabo.com/v1/compute/instances/{str(self.instanceId)}/actions/start").status_code

    def stop(self):

        return makeRequest(type="post",
                           url=f"https://api.contabo.com/v1/compute/instances/{str(self.instanceId)}/actions/stop").status_code

    def restart(self):

        return makeRequest(type="post",
                           url=f"https://api.contabo.com/v1/compute/instances/{str(self.instanceId)}/actions/start").status_code

    def getSnapshots(self, access_token):

        resp = makeRequest(type="get",
                           url=f"https://api.contabo.com/v1/compute/instances/{str(self.instanceId)}/snapshots",
                           access_token=access_token)

        if int(resp.status_code) == 200:
            self.snapshots = []
            for i in resp.json()["data"]:
                self.snapshots.append(Snapshot(self.instanceId, json=i))
            return self.snapshots

        return resp.status_code

    def getSnapshotById(self, id, access_token):

        resp = makeRequest(type="get",
                           url=f"https://api.contabo.com/v1/compute/instances/{id}",
                           access_token=access_token)

        if int(resp.status_code) == 200:
            return Instance(self.instanceId, json=resp.json()["data"][0])
        else:
            return resp.status_code

    def createSnapshot(self, access_token, name, description):
        resp = makeRequest(type="get",
                           url=f"https://api.contabo.com/v1/compute/instances/{str(self.instanceId)}/snapshots",
                           access_token=access_token,
                           data=json.dumps({"name": name, "description": description}))
        print(resp.status_code)
        print(json.dumps(resp.json(), indent=4))


class Snapshot:

    def __init__(self, instanceId, json=None):
        if json:
            self.tenantId = json["tenantId"]
            self.customerId = json["customerId"]
            self.snapshotId = json["snapshotId"]
            self.imageId = json["imageId"]
            self.imageName = json["imageName"]

        self.instaceId = instanceId

    def delete(self, access_token):
        resp = makeRequest(type="delete",
                           url=f"https://api.contabo.com/v1/compute/instances/{self.instanceId}/snapshots/{self.snapshotId}",
                           access_token=access_token)
        return resp.status_code

    def rollback(self, access_token):
        resp = makeRequest(type="post",
                           url=f"https://api.contabo.com/v1/compute/instances/{self.instanceId}/snapshots/{self.snapshotId}/rollback",
                           access_token=access_token)
        return resp.status_code


if __name__ == '__main__':
    client_id = input("Client ID: ")
    client_secret = input("Client Secret: ")
    api_user = input("API Username: ")
    api_password = input("API Password: ")
    cont = computeInstances(client_id, client_secret, api_user, api_password)
    token = cont.getToken()
    instance = cont.getInstances()[0]
    print(instance.getSpecs())
