class BadAuth(Exception):
    """Exception raised for 401 respond code.
    Auth did not succeed or auth token expired
    """

    def __init__(self, message="Supplied bad authentication credentials"):
        self.message = message
        super().__init__(self.message)


class ConflictingRessources(Exception):
    """Exception raised for 409 respond code.
    Conflict with resources. For example violation of unique data contraints
    """

    def __init__(self, message="Conflict with resources"):
        self.message = message
        super().__init__(self.message)


class RateLimitReached(Exception):
    """Exception raised for 429 respond code.
    Rate-limit reached. Please wait for some time before doing more requests.
    """

    def __init__(self, message="Rate-limit reached"):
        self.message = message
        super().__init__(self.message)


class ServerError(Exception):
    """Exception raised for 500 respond code.
    Server-side beep boop gone wrong. In such cases please retry or contact the support.
    """

    def __init__(self, message="Server-side error"):
        self.message = message
        super().__init__(self.message)

