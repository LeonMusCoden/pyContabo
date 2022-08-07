import json
from typing import List, Union

from .Tag import Tag
from .audits.TagsAudits import TagsAudits


class Tags:
    def __init__(self, _http):

        self._http = _http
        self.Audits = TagsAudits(_http)

    def get(
        self,
        id: str = None,
        page: int = None,
        pageSize: int = None,
        orderBy: str = None,
        name: str = None,
        x_request_id: str = None,
        x_trace_id: str = None,
    ) -> Union[Tag, List[Tag]]:
        """fetches any tag(s) by id or other parameters

        Examples:
            >>> Tags.get()
            [tag]
            >>> Tags.get(name="mysecret")
            [tag]
            >>> Tags.get(id="12345")
            tag

        Args:
            x_request_id: Uuid4 to identify individual requests for support cases.
            x_trace_id: Identifier to trace group of requests.
            id: The identifier of the tag
            page: Number of page to be fetched.
            pageSize: Number of elements per page.
            orderBy: Specify fields and ordering (ASC for ascending, DESC for descending) in following format `field:ASC|DESC`
            name: The name of the tag.

        Returns:
            List of tags
        """

        if id:
            resp = self._http.request(
                type="get",
                url=f"https://api.contabo.com/v1/tags/{id}",
                x_request_id=x_request_id,
                x_trace_id=x_trace_id,
            )

            if resp.status_code == 404:
                return []

            return Tag(resp.json()["data"][0], self._http)

        else:
            url = f"https://api.contabo.com/v1/tags?{f'page={page}&' if page is not None else ''}{f'size={pageSize}&' if pageSize is not None else ''}{f'orderBy={orderBy}&' if orderBy is not None else ''}{f'name={name}&' if name is not None else ''}"
            url = url[:-1]  # Remove the "?" at the end of the url
            resp = self._http.request(
                type="get", url=url, x_request_id=x_request_id, x_trace_id=x_trace_id
            )

            data = resp.json()["data"]
            if len(data) == 0:
                return []

            tags = []
            for i in resp.json()["data"]:
                tags.append(Tag(i, self._http))
            return tags

    def create(
        self, name: str, color: str, x_request_id: str = None, x_trace_id: str = None
    ) -> bool:
        """Creates a new tag

        Examples:
            >>> Tags.create(name="aName", color="#0A78C3")
            True

        Args:
            x_request_id: Uuid4 to identify individual requests for support cases.
            x_trace_id: Identifier to trace group of requests.
            name: The name of the tag.
            color: The color of the tag. Color can be specified using hexadecimal value. Default color is #0A78C3

        Returns:
            Bool respresenting if the tag has been succesfully created.
        """

        data = json.dumps({"name": name, "color": color})

        resp = self._http.request(
            type="post",
            url=f"https://api.contabo.com/v1/tags",
            data=data,
            x_request_id=x_request_id,
            x_trace_id=x_trace_id,
        )

        if resp.status_code == 201:
            return True
        return False
