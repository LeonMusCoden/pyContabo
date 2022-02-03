from .Assignments import Assignments


class Tag:
    def __init__(self, json, _http):

        self._http = _http
        self.Assignments = Assignments(_http, json["tagId"])

        self.tenantId = json["tenantId"]
        self.customerId = json["customerId"]
        self.tagId = json["tagId"]
        self.name = json["name"]
        self.color = json["color"]

        self.rawJson = json

    def update(self, name: str, color: str) -> bool:
        """updates the name and the value of the tag"""

        resp = self._http.request(
            type="patch",
            url=f"https://api.contabo.com/v1/tags/{self.tagId}",
            data={"name": name, "color": color},
        )

        if resp.status_code == 200:
            return True
        return False

    def delete(self) -> bool:
        """deletes the tag"""

        resp = self._http.request(
            type="delete", url=f"https://api.contabo.com/v1/tags/{self.tagId}"
        )

        if resp.status_code == 204:
            return True
        return False

    def assign(self, resourceType, resourceId) -> bool:
        """assigns tag to resource"""

        resp = self._http.request(
            type="post",
            url=f"https://api.contabo.com/v1/tags/{self.tagId}/assignments/{resourceType}/{resourceId}",
        )

        if resp.status_code == 201:
            return True
        return False
