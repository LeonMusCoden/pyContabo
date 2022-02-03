class Assignment:
    def __init__(self, json, _http):

        self._http = _http

        self.tenantId = json["tenantId"]
        self.customerId = json["customerId"]
        self.tagId = json["tagId"]
        self.tagName = json["tagName"]
        self.resourceType = json["resourceType"]
        self.resourceId = json["resourceId"]
        self.resourceName = json["resourceName"]

        self.rawJson = json

    def delete(self) -> bool:
        """deletes the secret"""

        resp = self._http.request(
            type="delete",
            url=f"https://api.contabo.com/v1/tags/{self.tagId}/assignments/{self.resourceType}/{self.resourceId}",
        )

        if resp.status_code == 204:
            return True
        return False
