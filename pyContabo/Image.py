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

    def update(self, name: str, value: str) -> bool:
        """updates the name and the value of the image"""

        resp = self._http.request(
            type="patch",
            url=f"https://api.contabo.com/v1/compute/images/{self.imageId}",
            data={"name": name, "value": value},
        )

        if resp.status_code == 200:
            return True
        return False

    def delete(self) -> bool:
        """deletes the image"""

        resp = self._http.request(
            type="delete",
            url=f"https://api.contabo.com/v1/compute/images/{self.imageId}",
        )

        if resp.status_code == 204:
            return True
        return False
