from .Role import Role
from typing import List


class User:
    def __init__(self, json, _http):

        self._http = _http

        self.tenantId = json["tenantId"]
        self.customerId = json["customerId"]
        self.userId = json["userId"]
        self.firstName = json["firstName"]
        self.lastName = json["lastName"]
        self.email = json["email"]
        self.emailVerified = json["emailVerified"]
        self.enabled = json["enabled"]
        self.totp = json["totp"]
        self.admin = json["admin"]
        self.accessAllResources = json["accessAllResources"]
        self.locale = json["locale"]
        self.roles = []

        for i in json["locale"]:
            self.roles.append(Role(i, self._http))

        self.rawJson = json

    def update(
        self,
        firstName: str,
        lastName: str,
        email: str,
        enabled: bool,
        totp: bool,
        admin: bool,
        accessAllResources: bool,
        locale: str,
        roles: List[int],
        x_request_id: str = None,
        x_trace_id: str = None,
    ) -> bool:
        """updates user info"""

        data = {}

        if firstName:
            data.append(firstName)
        if lastName:
            data.append(lastName)
        if email:
            data.append(email)
        if enabled:
            data.append(enabled)
        if totp:
            data.append(totp)
        if admin:
            data.append(admin)
        if accessAllResources:
            data.append(accessAllResources)
        if locale:
            data.append(locale)
        if roles:
            data.append(roles)

        resp = self._http.request(
            type="patch",
            url=f"https://api.contabo.com/v1/users/{self.userId}",
            data=data,
            x_request_id=x_request_id,
            x_trace_id=x_trace_id,
        )

        if resp.status_code == 200:
            return True
        return False

    def delete(self, x_request_id: str = None, x_trace_id: str = None) -> bool:
        """deletes the user"""

        resp = self._http.request(
            type="delete",
            url=f"https://api.contabo.com/v1/users/{self.userId}",
            x_request_id=x_request_id,
            x_trace_id=x_trace_id,
        )

        if resp.status_code == 204:
            return True
        return False

    def resetPassword(
        self, redirectUrl: str = None, x_request_id: str = None, x_trace_id: str = None
    ) -> bool:
        """sends reset password email"""

        if redirectUrl:
            resp = self._http.request(
                type="post",
                url=f"https://api.contabo.com/v1/users/{self.userId}/reset-password",
                data={"redirectUrl": redirectUrl},
                x_request_id=x_request_id,
                x_trace_id=x_trace_id,
            )
        else:
            resp = self._http.request(
                type="post",
                url=f"https://api.contabo.com/v1/users/{self.userId}/reset-password",
                x_request_id=x_request_id,
                x_trace_id=x_trace_id,
            )

        if resp.status_code == 204:
            return True
        return False

    def resendEmailVerification(
        self, redirectUrl: str = None, x_request_id: str = None, x_trace_id: str = None
    ) -> bool:
        """sends reset password email"""

        if redirectUrl:
            resp = self._http.request(
                type="post",
                url=f"https://api.contabo.com/v1/users/{self.userId}/resend-email-verification",
                data={"redirectUrl": redirectUrl},
                x_request_id=x_request_id,
                x_trace_id=x_trace_id,
            )
        else:
            resp = self._http.request(
                type="post",
                url=f"https://api.contabo.com/v1/users/{self.userId}/resend-email-verification",
                x_request_id=x_request_id,
                x_trace_id=x_trace_id,
            )

        if resp.status_code == 204:
            return True
        return False

    def isPasswordSet(self, x_request_id: str = None, x_trace_id: str = None) -> bool:
        """checks if user password is set (API DOCUMENTATION IS INCOMPLETE)"""

        resp = self._http.request(
            type="get",
            url=f"https://api.contabo.com/v1/users/{self.userId}/is-password-set",
            x_request_id=x_request_id,
            x_trace_id=x_trace_id,
        )

        if resp.status_code == 200:
            return True
        return False
