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
    ) -> Union[Tag, List[Tag]]:
        """gets any tag by id or other parameters through the paging system"""

        if id:
            resp = self._http.request(
                type="get", url=f"https://api.contabo.com/v1/tags/{id}"
            )

            if resp.status_code == 404:
                return []

            return Tag(resp.json()["data"][0], self._http)

        else:
            url = f"https://api.contabo.com/v1/tags?{f'page={page}&' if page is not None else ''}{f'size={pageSize}&' if pageSize is not None else ''}{f'orderBy={orderBy}&' if orderBy is not None else ''}{f'name={name}&' if name is not None else ''}"
            url = url[:-1]  # Remove the "?" at the end of the url
            resp = self._http.request(type="get", url=url)

            data = resp.json()["data"]
            if len(data) == 0:
                return []

            tags = []
            for i in resp.json()["data"]:
                tags.append(Tag(i, self._http))
            return tags

    def create(self, name: str, color: str) -> bool:
        """creates new tag using name, url, OS type, OS version and description"""

        data = json.dumps({"name": name, "color": color})

        resp = self._http.request(
            type="post", url=f"https://api.contabo.com/v1/tags", data=data
        )

        if resp.status_code == 201:
            return True
        return False
