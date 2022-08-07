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
        """Update attributes of a snapshot. You may only specify the attributes you want to change. If an attribute is not set, it will retain its original value.

        Examples:
            >>> snapshot.update(name="name", description="desc")
            True

        Args:
            x_request_id: Uuid4 to identify individual requests for support cases.
            x_trace_id: Identifier to trace group of requests.
            name: The name of the snapshot. Tags may contain letters, numbers, colons, dashes, and underscores. There is a limit of 255 characters per snapshot.
            description: The description of the snapshot. There is a limit of 255 characters per snapshot.

        Returns:
            Bool respresenting if the snapshot has been succesfully updated.
        """

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
        """deletes the snapshot

        Examples:
            >>> snapshot.delete()
            True

        Args:
            x_request_id: Uuid4 to identify individual requests for support cases.
            x_trace_id: Identifier to trace group of requests.

        Returns:
            Bool respresenting if the snapshot has been succesfully deleted.
        """

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
        """Rollback instance to the snapshot.

        Examples:
            >>> snapshot.rollback()
            True

        Args:
            x_request_id: Uuid4 to identify individual requests for support cases.
            x_trace_id: Identifier to trace group of requests.

        Returns:
            Bool respresenting if the instance has been rolled back to the snapshot
        """

        resp = self._http.request(
            type="post",
            url=f"https://api.contabo.com/v1/compute/instances/{self.instanceId}/snapshots/{self.snapshotId}/rollback",
            x_request_id=x_request_id,
            x_trace_id=x_trace_id,
        )

        if resp.status_code == 200:
            return True
        return False
