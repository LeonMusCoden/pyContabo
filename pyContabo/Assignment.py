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

    def delete(self, x_request_id: str = None, x_trace_id: str = None) -> bool:
        """deletes the secret"""

        resp = self._http.request(
            type="delete",
            url=f"https://api.contabo.com/v1/tags/{self.tagId}/assignments/{self.resourceType}/{self.resourceId}",
            x_request_id=x_request_id,
            x_trace_id=x_trace_id,
        )

        if resp.status_code == 204:
            return True
        return False
