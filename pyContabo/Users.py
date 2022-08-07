import json
from typing import List, Union

from .User import User
from .audits.UsersAudits import UsersAudits
from .types.locales import locale


class Users:
    def __init__(self, _http):

        self._http = _http
        self.Audits = UsersAudits(_http)

    def get(
        self,
        id: str = None,
        page: int = None,
        pageSize: int = None,
        orderBy: str = None,
        email: str = None,
        enabled: bool = None,
        owner: bool = None,
        x_request_id: str = None,
        x_trace_id: str = None,
    ) -> Union[User, List[User]]:
        """fetches any user(s) by id or other parameters

        Examples:
            >>> Users.get()
            [user]
            >>> Users.get(email="mysecret", type="password")
            [user]
            >>> Users.get(id="6cdf5968-f9fe-4192-97c2-f349e813c5e8")
            user

        Args:
            x_request_id: Uuid4 to identify individual requests for support cases.
            x_trace_id: Identifier to trace group of requests.
            id: The identifier of the secret
            page: Number of page to be fetched.
            pageSize: Number of elements per page.
            orderBy: Specify fields and ordering (ASC for ascending, DESC for descending) in following format `field:ASC|DESC`
            email: Filter as substring match for user emails.
            enabled: Filter if user is enabled or not.
            owner: Filter if user is owner or not.

        Returns:
            List of users
        """

        if id:
            resp = self._http.request(
                type="get",
                url=f"https://api.contabo.com/v1/users/{id}",
                x_request_id=x_request_id,
                x_trace_id=x_trace_id,
            )

            if resp.status_code == 404:
                return []

            return User(resp.json()["data"][0], self._http)

        else:
            url = f"https://api.contabo.com/v1/compute/instances/{self.instanceId}/snapshots?{f'page={page}&' if page is not None else ''}{f'size={pageSize}&' if pageSize is not None else ''}{f'orderBy={orderBy}&' if orderBy is not None else ''}{f'email={email}&' if email is not None else ''}{f'enabled={enabled}&' if enabled is not None else ''}{f'owner={owner}&' if owner is not None else ''}"
            url = url[:-1]
            resp = self._http.request(
                type="get", url=url, x_request_id=x_request_id, x_trace_id=x_trace_id
            )

            data = resp.json()["data"]
            if len(data) == 0:
                return []

            users = []
            for i in resp.json()["data"]:
                users.append(User(i, self._http))
            return users

    def create(
        self,
        email: str,
        enabled: bool,
        totp: bool,
        locale: locale,
        firstName: str = None,
        lastName: str = None,
        roles: List[int] = None,
        x_request_id: str = None,
        x_trace_id: str = None,
    ) -> bool:
        """Creates a new user

        Examples:
            >>> Users.create(email="example@example.com", enabled=True, totp=False, locale=locale)
            True

        Args:
            x_request_id: Uuid4 to identify individual requests for support cases.
            x_trace_id: Identifier to trace group of requests.
            email: The email of the user to which activation and forgot password links are being sent to. There is a limit of 255 characters per email.
            enabled: If user is not enabled, he can't login and thus use services any longer.
            totp: Enable or disable two-factor authentication (2FA) via time based OTP.
            locale: The locale of the user. This can be `de-DE`, `de`, `en-US`, `en`.
            firstName: The name of the user. Names may contain letters, numbers, colons, dashes, and underscores. There is a limit of 255 characters per user.
            lastName: The last name of the user. Users may contain letters, numbers, colons, dashes, and underscores. There is a limit of 255 characters per user.
            roles: The roles as list of `roleId`s of the user.

        Returns:
            Bool respresenting if the secret has been succesfully created.
        """

        data = {
            "firstName": firstName,
            "lastName": lastName,
            "email": email,
            "enabled": enabled,
            "totp": totp,
            "locale": locale.name,
        }

        if roles:
            data.append(roles)

        resp = self._http.request(
            type="post",
            url=f"https://api.contabo.com/v1/users",
            data=json.dumps(data),
            x_request_id=x_request_id,
            x_trace_id=x_trace_id,
        )

        if resp.status_code == 201:
            return True
        return False
