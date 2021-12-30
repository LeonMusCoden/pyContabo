import uuid
from random import randint

import requests
from requests.structures import CaseInsensitiveDict


class RequestsManager:

    def __init__(self, token):

        self.access_token = token
        self.instances = None
        self.snapshots = None
        self.instancesaudit = None

    def createInstances(self):
        return RequestsManager.Instances(self)

    def createSnapshots(self, instance):
        return RequestsManager.Snapshots(instance, self)

    def createInstancesAudits(self, instance):
        return RequestsManager.InstancesAudits(instance, self)



    def request(self, type, url, data={}):

        headers = CaseInsensitiveDict()
        headers["Authorization"] = f"Bearer {self.access_token}"
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

    class Instances:

        def __init__(self, requestmanager):
            self.page = 1
            self.totalPages = None
            self.pageSize = None
            self.totalElements = None
            self.json = None
            self.pagination = None
            self.data = None
            self.links = None
            self.requestmanager = requestmanager

        def get(self, page=None, size=None, orderByField=None, order=None, name=None, region=None, instanceId=None, status=None):
            resp = self.requestmanager.makeRequest(type="delete",
                               url=f"https://api.contabo.com/v1/compute/instances/{self.instanceId}/snapshots/{self.snapshotId}",
                               access_token=self.requestmanager.access_token)

        def next(self):
            pass

        def previous(self):
            pass

    class Snapshots:

        def __init__(self, instance, requestmanager):
            self.instance = instance
            self.page=1
            self.totalPages = None
            self.pageSize = None
            self.totalElements = None
            self.json = None
            self.pagination = None
            self.data = None
            self.links = None
            self.requestmanager = requestmanager

        def get(self, page=None, size=None, orderByField=None, order=None, name=None):
            pass

        def next(self):
            pass

        def previous(self):
            pass

    class InstancesAudits:

        def __init__(self, instance, requestmanager):
            self.instance = instance
            self.page=1
            self.totalPages = None
            self.pageSize = None
            self.totalElements = None
            self.json = None
            self.pagination = None
            self.data = None
            self.links = None
            self.requestmanager = requestmanager

        def get(self, page=None, size=None, orderByField=None, order=None, requestId=None, changedBy=None):
            pass

        def next(self):
            pass

        def previous(self):
            pass




