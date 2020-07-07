from abc import ABC, abstractmethod
from typing import Dict

from requests import Response


class BaseError(Exception, ABC):
    """
    A Plaid API error.

    :message:            A developer-friendly error message. Not safe for programmatic use.
    :display_message:    A user-friendly error message. Not safe for programmatic use. May be None.
    :request_id:         A unique id returned for all server responses.
    :raw_response:       The actual response the API sent back
    """

    def __init__(
        self, message: str, display_message: str, request_id=None, raw_response: Response = None,
    ):
        super().__init__(message)

        # In Python 3, the Exception class does not expose a `message`
        # attribute so we need to set it explicitly. See
        # https://www.python.org/dev/peps/pep-0352/#retracted-ideas.
        self.message = message

        self.display_message = display_message
        self.request_id = request_id
        self.raw_response = raw_response

    @classmethod
    def from_error_dict(cls, error: Dict):
        return cls(
            message=error["message"],
            display_message=error["display_message"],
            request_id=error.get("request_id"),
            raw_response=error.get("raw_response"),
        )

    @staticmethod
    @abstractmethod
    def code():
        pass


class APIError(BaseError):
    code = "API_ERROR"
    """Unspecified error with the request"""

    pass


class RequestError(BaseError):
    code = "REQUEST_ERROR"
    """The request could not be completed and we have details about why"""
    pass
