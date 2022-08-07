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
        firstName: str = None,
        lastName: str = None,
        email: str = None,
        enabled: bool = None,
        totp: bool = None,
        admin: bool = None,
        accessAllResources: bool = None,
        locale: str = None,
        roles: List[int] = None,
        x_request_id: str = None,
        x_trace_id: str = None,
    ) -> bool:
        """Update attributes of a user. You may only specify the attributes you want to change. If an attribute is not set, it will retain its original value.

        Examples:
            >>> user.update(firstName="name", lastNAme="name", email="example@example.com")
            True

        Args:
            x_request_id: Uuid4 to identify individual requests for support cases.
            x_trace_id: Identifier to trace group of requests.
            firstName: The name of the user. Names may contain letters, numbers, colons, dashes, and underscores. There is a limit of 255 characters per user.
            lastName: The last name of the user. Users may contain letters, numbers, colons, dashes, and underscores. There is a limit of 255 characters per user.
            email: The email of the user to which activation and forgot password links are being sent to. There is a limit of 255 characters per email.
            enabled: If uses is not enabled, he can't login and thus use services any longer.
            totp: Enable or disable two-factor authentication (2FA) via time based OTP.
            locale: The locale of the user. This can be `de-DE`, `de`, `en-US`, `en`.
            roles: The roles as list of `roleId`s of the user.

        Returns:
            Bool respresenting if the user has been succesfully updated.
        """

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
        """deletes the user

        Examples:
            >>> user.delete()
            True

        Args:
            x_request_id: Uuid4 to identify individual requests for support cases.
            x_trace_id: Identifier to trace group of requests.

        Returns:
            Bool respresenting if the user has been succesfully deleted.
        """

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
        """Send reset password email to the user.

        Examples:
            >>> user.resetPassword(redirectUrl="https://test.contabo.de")
            True

        Args:
            x_request_id: Uuid4 to identify individual requests for support cases.
            x_trace_id: Identifier to trace group of requests.
            redirectUrl: The redirect url used for resetting password

        Returns:
            Bool respresenting if the user's password has been succesfully reset.
        """

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
        """Resend email verification for the specific user.

        Examples:
            >>> user.resendEmailVerification(redirectUrl="https://test.contabo.de")
            True

        Args:
            x_request_id: Uuid4 to identify individual requests for support cases.
            x_trace_id: Identifier to trace group of requests.
            redirectUrl: The redirect url used for resetting password

        Returns:
            Bool respresenting if the email verification has been succesfully sent.
        """

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
