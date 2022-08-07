class Image:
    def __init__(self, json, _http):

        self._http = _http

        self.tenantId = json["tenantId"]
        self.customerId = json["customerId"]
        self.imageId = json["imageId"]
        self.name = json["name"]
        self.description = json["description"]
        self.url = json["url"]
        self.sizeMb = json["sizeMb"]
        self.uploadedSizeMb = json["uploadedSizeMb"]
        self.osType = json["osType"]
        self.version = json["version"]
        self.format = json["format"]
        self.status = json["status"]
        self.errorMessage = json["errorMessage"]
        self.standardImage = json["standardImage"]
        self.creationDate = json["creationDate"]
        self.lastModifiedDate = json["lastModifiedDate"]

        self.rawJson = json

    def update(
        self, name: str, description: str, x_request_id: str = None, x_trace_id: str = None
    ) -> bool:
        """Update name of the custom image.

        Examples:
            >>> image.update(name="Arch Linux", description="btw")
            True

        Args:
            x_request_id: Uuid4 to identify individual requests for support cases.
            x_trace_id: Identifier to trace group of requests.
            name: Image Name
            description: Image Description

        Returns:
            Bool respresenting if the image has been succesfully updated.
        """


        resp = self._http.request(
            type="patch",
            url=f"https://api.contabo.com/v1/compute/images/{self.imageId}",
            data={"name": name, "description": description},
            x_request_id=x_request_id,
            x_trace_id=x_trace_id,
        )

        if resp.status_code == 200:
            return True
        return False

    def delete(self, x_request_id: str = None, x_trace_id: str = None) -> bool:
        """deletes the image

        Examples:
            >>> image.delete()
            True

        Args:
            x_request_id: Uuid4 to identify individual requests for support cases.
            x_trace_id: Identifier to trace group of requests.

        Returns:
            Bool respresenting if the image has been succesfully deleted.
        """

        resp = self._http.request(
            type="delete",
            url=f"https://api.contabo.com/v1/compute/images/{self.imageId}",
            x_request_id=x_request_id,
            x_trace_id=x_trace_id,
        )

        if resp.status_code == 204:
            return True
        return False
