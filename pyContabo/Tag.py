from .Assignments import Assignments
from .types.resources import resource


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

    def update(
        self, name: str, color: str, x_request_id: str = None, x_trace_id: str = None
    ) -> bool:
        """Update attributes to your tag. Attributes are optional. If not set, the attributes will retain their original values.

        Examples:
            >>> tag.update(name="name", color="#0A78C3")
            True

        Args:
            x_request_id: Uuid4 to identify individual requests for support cases.
            x_trace_id: Identifier to trace group of requests.
            name: The name of the tag. Tags may contain letters, numbers, colons, dashes, and underscores. There is a limit of 255 characters per tag.
            color: The color of the tag. Color can be specified using hexadecimal value. Default color is #0A78C3

        Returns:
            Bool respresenting if the tag has been succesfully updated.
        """

        resp = self._http.request(
            type="patch",
            url=f"https://api.contabo.com/v1/tags/{self.tagId}",
            data={"name": name, "color": color},
            x_request_id=x_request_id,
            x_trace_id=x_trace_id,
        )

        if resp.status_code == 200:
            return True
        return False

    def delete(self, x_request_id: str = None, x_trace_id: str = None) -> bool:
        """deletes the tag

        Examples:
            >>> tag.delete()
            True

        Args:
            x_request_id: Uuid4 to identify individual requests for support cases.
            x_trace_id: Identifier to trace group of requests.

        Returns:
            Bool respresenting if the tag has been succesfully deleted.
        """

        resp = self._http.request(
            type="delete",
            url=f"https://api.contabo.com/v1/tags/{self.tagId}",
            x_request_id=x_request_id,
            x_trace_id=x_trace_id,
        )

        if resp.status_code == 204:
            return True
        return False

    def assign(
        self,
        resourceType: resource,
        resourceId: str,
        x_request_id: str = None,
        x_trace_id: str = None,
    ) -> bool:
        """Create a new tag assignment. This marks the specified resource with the specified tag for organizing purposes or to restrict access to that resource.

        Examples:
            >>> tag.assign(resourceType=ressource.instance, resourceId="d65ecf3b-30db-4dc2-9e88-dfc21a14a6bc")
            True

        Args:
            x_request_id: Uuid4 to identify individual requests for support cases.
            x_trace_id: Identifier to trace group of requests.
            resourceType: The identifier of the resource type. Resource type is one of `instance|image|object-storage`
            resourceId: The identifier of the resource id

        Returns:
            Bool respresenting if the tag has been succesfully assigned.
        """

        resp = self._http.request(
            type="post",
            url=f"https://api.contabo.com/v1/tags/{self.tagId}/assignments/{resourceType.name}/{resourceId}",
            x_request_id=x_request_id,
            x_trace_id=x_trace_id,
        )

        if resp.status_code == 201:
            return True
        return False
