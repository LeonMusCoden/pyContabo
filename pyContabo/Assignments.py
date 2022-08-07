import json

from .Assignment import Assignment
from .audits.TagAssignmentsAudits import TagAssignmentsAudits
from typing import List, Union


class Assignments:
    def __init__(self, _http, tagId):

        self._http = _http
        self.tagId = tagId
        self.Audits = TagAssignmentsAudits(_http)

    def get(
        self,
        resourceType: str = None,
        resourceId: str = None,
        page: int = None,
        pageSize: int = None,
        orderBy: str = None,
        x_request_id: str = None,
        x_trace_id: str = None,
    ) -> Union[Assignment, List[Assignment]]:
        """fetches any tag assignment(s) by id or other parameters

        Examples:
            >>> Assignments.get()
            [assignment]
            >>> Assignments.get(resourceType="instance", resourceId="d65ecf3b-30db-4dc2-9e88-dfc21a14a6bc", orderBy="name:asc")
            [assignment]
            >>> Assignments.get(resourceType="instance", resourceId="d65ecf3b-30db-4dc2-9e88-dfc21a14a6bc")
            assignment

        Args:
            x_request_id: Uuid4 to identify individual requests for support cases.
            x_trace_id: Identifier to trace group of requests.
            resourceType: The identifier of the resource type. Resource type is one of `instance|image|object-storage`
            resourceId: The identifier of the resource id
            page: Number of page to be fetched.
            pageSize: Number of elements per page.
            orderBy: Specify fields and ordering (ASC for ascending, DESC for descending) in following format `field:ASC|DESC`

        Returns:
            List of tag assignments
        """

        if resourceType and resourceId:
            resp = self._http.request(
                type="get",
                url=f"https://api.contabo.com/v1/tags/{self.tagId}/assignments/{resourceType}/{resourceId}",
                x_request_id=x_request_id,
                x_trace_id=x_trace_id,
            )

            if resp.status_code == 404:
                return []

            return Assignment(resp.json()["data"][0], self._http)

        else:
            url = f"https://api.contabo.com/v1/tags/{self.tagId}/assignments?{f'page={page}&' if page is not None else ''}{f'size={pageSize}&' if pageSize is not None else ''}{f'orderBy={orderBy}&' if orderBy is not None else ''}"
            url = url[:-1]  # Remove the "?" at the end of the url
            resp = self._http.request(
                type="get", url=url, x_request_id=x_request_id, x_trace_id=x_trace_id
            )

            data = resp.json()["data"]
            if len(data) == 0:
                return []

            assignment = []
            for i in resp.json()["data"]:
                assignment.append(Assignment(i, self._http))
            return assignment

    def assign(
        self,
        resourceType: str,
        resourceId: str,
        x_request_id: str = None,
        x_trace_id: str = None,
    ) -> bool:
        """Create a new tag assignment. This marks the specified resource with the specified tag for organizing purposes or to restrict access to that resource.

        Examples:
            >>> Assignments.assign(resourceType="instance", resourceId="d65ecf3b-30db-4dc2-9e88-dfc21a14a6bc")
            True

        Args:
            x_request_id: Uuid4 to identify individual requests for support cases.
            x_trace_id: Identifier to trace group of requests.
            resourceType: The identifier of the resource type. Resource type is one of `instance|image|object-storage`
            resourceId: The identifier of the resource id

        Returns:
            Bool respresenting if the assignment has been succesfully assigned.
        """

        resp = self._http.request(
            type="post",
            url=f"https://api.contabo.com/v1/tags/{self.tagId}/assignments/{resourceType}/{resourceId}",
            x_request_id=x_request_id,
            x_trace_id=x_trace_id,
        )

        if resp.status_code == 201:
            return True
        return False
