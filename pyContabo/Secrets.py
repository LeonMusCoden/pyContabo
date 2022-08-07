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
        x_request_id: str = None,
        x_trace_id: str = None,
    ) -> Union[Secret, List[Secret]]:
        """fetches any secret(s) by id or other parameters

        Examples:
            >>> Secrets.get()
            [secret]
            >>> Secrets.get(name="mysecret", type="password")
            [secret]
            >>> Secrets.get(id="100")
            secret

        Args:
            x_request_id: Uuid4 to identify individual requests for support cases.
            x_trace_id: Identifier to trace group of requests.
            id: The identifier of the secret
            page: Number of page to be fetched.
            pageSize: Number of elements per page.
            orderBy: Specify fields and ordering (ASC for ascending, DESC for descending) in following format `field:ASC|DESC`
            name: The name of the instance.
            type: The type of the secret. Can be `password` or `ssh`.

        Returns:
            List of secrets
        """

        if id:
            resp = self._http.request(
                type="get",
                url=f"https://api.contabo.com/v1/secrets/{id}",
                x_request_id=x_request_id,
                x_trace_id=x_trace_id,
            )

            if resp.status_code == 404:
                return []

            return Secret(resp.json()["data"][0], self._http)

        else:
            url = f"https://api.contabo.com/v1/secrets?{f'page={page}&' if page is not None else ''}{f'size={pageSize}&' if pageSize is not None else ''}{f'orderBy={orderBy}&' if orderBy is not None else ''}{f'name={name}&' if name is not None else ''}{f'name={type}&' if type is not None else ''}"
            url = url[:-1]  # Remove the "?" at the end of the url
            resp = self._http.request(
                type="get", url=url, x_request_id=x_request_id, x_trace_id=x_trace_id
            )

            data = resp.json()["data"]
            if len(data) == 0:
                return []

            secrets = []
            for i in resp.json()["data"]:
                secrets.append(Secret(i, self._http))
            return secrets

    def create(
        self,
        name: str,
        value: str,
        type: str,
        x_request_id: str = None,
        x_trace_id: str = None,
    ) -> bool:
        """Creates a new secret

        Examples:
            >>> Secrets.create(name="aName", value="12345678", type="password", period="1")
            True

        Args:
            x_request_id: Uuid4 to identify individual requests for support cases.
            x_trace_id: Identifier to trace group of requests.
            name: The name of the secret.
            value: The secret value that needs to be saved.
            type: The type of the secret. Can be `password` or `ssh`.

        Returns:
            Bool respresenting if the secret has been succesfully created.
        """

        data = json.dumps({"name": name, "value": value, "type": type})

        resp = self._http.request(
            type="post",
            url=f"https://api.contabo.com/v1/secrets",
            data=data,
            x_request_id=x_request_id,
            x_trace_id=x_trace_id,
        )

        if resp.status_code == 201:
            return True
        return False
