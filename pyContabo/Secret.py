class Secret:
    def __init__(self, json, _http):

        self._http = _http

        self.tenantId = json["tenantId"]
        self.customerId = json["customerId"]
        self.secretId = json["secretId"]
        self.name = json["name"]
        self.type = json["type"]
        self.value = json["value"]
        self.createdAt = json["createdAt"]
        self.updatedAt = json["updatedAt"]

        self.rawJson = json

    def update(self, name: str, value: str) -> bool:
        """updates the name and the value of the secret"""

        resp = self._http.request(
            type="patch",
            url=f"https://api.contabo.com/v1/secrets/{self.secretId}",
            data={"name": name, "value": value},
        )

        if resp.status_code == 200:
            return True
        return False

    def delete(self) -> bool:
        """deletes the secret"""

        resp = self._http.request(
            type="delete", url=f"https://api.contabo.com/v1/secrets/{self.secretId}"
        )

        if resp.status_code == 204:
            return True
        return False
