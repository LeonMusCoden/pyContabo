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

    def update(
        self, name: str, value: str, x_request_id: str = None, x_trace_id: str = None
    ) -> bool:
        """Update attributes to your secret. Attributes are optional. If not set, the attributes will retain their original values. Only name and value can be updated.

        Examples:
            >>> secret.update(name="name", value="12345678")
            True

        Args:
            x_request_id: Uuid4 to identify individual requests for support cases.
            x_trace_id: Identifier to trace group of requests.
            name: The name of the secret to be saved
            value: The value of the secret to be saved

        Returns:
            Bool respresenting if the secret has been succesfully updated.
        """

        resp = self._http.request(
            type="patch",
            url=f"https://api.contabo.com/v1/secrets/{self.secretId}",
            data={"name": name, "value": value},
            x_request_id=x_request_id,
            x_trace_id=x_trace_id,
        )

        if resp.status_code == 200:
            return True
        return False

    def delete(self, x_request_id: str = None, x_trace_id: str = None) -> bool:
        """deletes the secret

        Examples:
            >>> secret.delete()
            True

        Args:
            x_request_id: Uuid4 to identify individual requests for support cases.
            x_trace_id: Identifier to trace group of requests.

        Returns:
            Bool respresenting if the secret has been succesfully deleted.
        """

        resp = self._http.request(
            type="delete",
            url=f"https://api.contabo.com/v1/secrets/{self.secretId}",
            x_request_id=x_request_id,
            x_trace_id=x_trace_id,
        )

        if resp.status_code == 204:
            return True
        return False
