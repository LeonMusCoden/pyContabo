class Snapshot:
    def __init__(self, json, _http):

        self._http = _http

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

    def update(
        self,
        name: str,
        description: str = None,
        x_request_id: str = None,
        x_trace_id: str = None,
    ) -> bool:
        """updates name and description of the snapshot"""

        if description:
            resp = self._http.request(
                type="patch",
                url=f"https://api.contabo.com/v1/compute/instances/{self.instanceId}/snapshots/{self.snapshotId}",
                data={"name": name, "description": description},
                x_request_id=x_request_id,
                x_trace_id=x_trace_id,
            )
        else:
            resp = self._http.request(
                type="patch",
                url=f"https://api.contabo.com/v1/compute/instances/{self.instanceId}/snapshots/{self.snapshotId}",
                data={"name": name, "description": description},
                x_request_id=x_request_id,
                x_trace_id=x_trace_id,
            )

        if resp.status_code == 200:
            return True
        return False

    def delete(self, x_request_id: str = None, x_trace_id: str = None) -> bool:
        """deletes the snapshot"""

        resp = self._http.request(
            type="delete",
            url=f"https://api.contabo.com/v1/compute/instances/{self.instanceId}/snapshots/{self.snapshotId}",
            x_request_id=x_request_id,
            x_trace_id=x_trace_id,
        )

        if resp.status_code == 204:
            return True
        return False

    def rollback(self, x_request_id: str = None, x_trace_id: str = None) -> bool:
        """restores the instance to the snapshot"""

        resp = self._http.request(
            type="post",
            url=f"https://api.contabo.com/v1/compute/instances/{self.instanceId}/snapshots/{self.snapshotId}/rollback",
            x_request_id=x_request_id,
            x_trace_id=x_trace_id,
        )

        if resp.status_code == 200:
            return True
        return False
