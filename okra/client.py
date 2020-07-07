from typing import Dict

import requests as requests

from okra.api import Auth
from okra.errors import RequestError, APIError
from okra.messages import COULD_NOT_COMPLETE_REQUEST


class Client:
    def __init__(self, environment="test", version="v1", raise_errors=True):
        self.environment = environment
        self.version = version
        self.raise_errors = raise_errors
        self.auth = Auth(self)

    @property
    def url(self):
        url = "https://api.okra.ng/{version}" if self.environment == "prod" else "https://dev-api.okra.ng/{version}"
        return url.format(version=self.version)

    def post(self, *args, **kwargs) -> Dict:
        response = requests.post(*args, **kwargs)
        try:
            data = response.json()
        except ValueError:
            error = dict(
                message=response.text,
                display_message=COULD_NOT_COMPLETE_REQUEST,
                raw_response=response,
                _status="ERROR",
            )
            if self.raise_errors:
                raise APIError.from_error_dict(error)
            else:
                return error

        if data.get("message") != "success":
            error = dict(message=data.msg, display_message=data.msg, raw_response=response, _status="ERROR",)
            if self.raise_errors:
                raise RequestError.from_error_dict(error)
            else:
                return error

        return dict(_status="SUCCESS", **data.data)
