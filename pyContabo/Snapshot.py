from .util import makeRequest, statusCheck


class Snapshot:

    def __init__(self, json, access_token):

        self.tenantId = json["tenantId"]
        self.customerId = json["customerId"]
        self.snapshotId = json["snapshotId"]
        self.name = json["name"]
        self.description = json["description"]
        self.instanceId = json["instanceId"]
        self.createdDate = json["createdDate"]
        self.autoDeleteDate = json["autoDeleteDate"]
        self.imageId = json["imageId"]
        self.imageName = json["imageName"]

        self.rawJson = json
        self.access_token = access_token

    def update(self, name: str, desc: str):

        status = makeRequest(type="patch",
                             url=f"https://api.contabo.com/v1/compute/instances/{self.instanceId}/snapshots/{self.snapshotId}",
                             access_token=self.access_token).status_code

        statusCheck(status)
        if status == 200:
            return True
        return False

    def delete(self):

        status = makeRequest(type="delete",
                             url=f"https://api.contabo.com/v1/compute/instances/{self.instanceId}/snapshots/{self.snapshotId}",
                             access_token=self.access_token).status_code

        statusCheck(status)
        if status == 204:
            return True
        return False

    def rollback(self):

        status = makeRequest(type="post",
                             url=f"https://api.contabo.com/v1/compute/instances/{self.instanceId}/snapshots/{self.snapshotId}/rollback",
                             access_token=self.access_token).status_code

        statusCheck(status)
        if status == 200:
            return True
        return False