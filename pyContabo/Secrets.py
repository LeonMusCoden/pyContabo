import json
from typing import List, Union

from .Secret import Secret
from .audits.SecretsAudits import SecretsAudits


class Secrets:
    def __init__(self, _http):

        self._http = _http
        self.Audits = SecretsAudits(_http)

    def get(
        self,
        id: str = None,
        page: int = None,
        pageSize: int = None,
        orderBy: str = None,
        name: str = None,
        type: str = None,
    ) -> Union[Secret, List[Secret]]:
        """gets any secret by id or other parameters through the paging system"""

        if id:
            resp = self._http.request(
                type="get", url=f"https://api.contabo.com/v1/secrets/{id}"
            )

            if resp.status_code == 404:
                return []

            return Secret(resp.json()["data"][0], self._http)

        else:
            url = f"https://api.contabo.com/v1/secrets?{f'page={page}&' if page is not None else ''}{f'size={pageSize}&' if pageSize is not None else ''}{f'orderBy={orderBy}&' if orderBy is not None else ''}{f'name={name}&' if name is not None else ''}{f'name={type}&' if type is not None else ''}"
            url = url[:-1]  # Remove the "?" at the end of the url
            resp = self._http.request(type="get", url=url)

            data = resp.json()["data"]
            if len(data) == 0:
                return []

            secrets = []
            for i in resp.json()["data"]:
                secrets.append(Secret(i, self._http))
            return snapshots

    def create(self, name: str, value: str, type: str) -> bool:
        """creates a new secret using name, value and type"""

        data = json.dumps({"name": name, "value": value, "type": type})

        resp = self._http.request(
            type="post", url=f"https://api.contabo.com/v1/secrets", data=data
        )

        if resp.status_code == 201:
            return True
        return False
