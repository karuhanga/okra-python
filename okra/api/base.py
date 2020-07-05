from requests.auth import AuthBase

from okra.client import Client


class API:
    def __init__(self, client: Client):
        self.client = client

    @property
    def url(self):
        return self.client.url

    @staticmethod
    def get_auth(access_token: str):
        return _TokenAuth(access_token)


class _TokenAuth(AuthBase):
    def __init__(self, access_token: str):
        self.access_token = access_token

    def __call__(self, request):
        request.headers["Authorization"] = "Bearer {}".format(self.access_token)
        return request
