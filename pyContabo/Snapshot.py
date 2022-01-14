from .util import makeRequest, statusCheck


class Snapshot:

    def __init__(self, json, ):

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

    def update(self, name: str, description: str=None):
        """updates name and description of a snapshot"""

        if description:
            resp = makeRequest(type="patch",
                               url=f"https://api.contabo.com/v1/compute/instances/{self.instanceId}/snapshots/{self.snapshotId}",
                               data={"name": name, "description": description})
        else:
            resp = makeRequest(type="patch",
                               url=f"https://api.contabo.com/v1/compute/instances/{self.instanceId}/snapshots/{self.snapshotId}",
                               data={"name": name, "description": description})

        statusCheck(resp.status_code)
        if resp.status_code == 200:
            return True
        return False

    def delete(self):
        """deletes a snapshot"""

        resp = makeRequest(type="delete",
                             url=f"https://api.contabo.com/v1/compute/instances/{self.instanceId}/snapshots/{self.snapshotId}")

        statusCheck(resp.status_code)
        if resp.status_code == 204:
            return True
        return False

    def rollback(self):
        """rollbacks the instance to a snapshot"""

        resp = makeRequest(type="post",
                             url=f"https://api.contabo.com/v1/compute/instances/{self.instanceId}/snapshots/{self.snapshotId}/rollback")

        statusCheck(resp.status_code)
        if resp.status_code == 200:
            return True
        return False
