from typing import Optional

from okra.api.base import API
from okra.api.utils import OptionalDict
from okra.client import Client


class Auth(API):
    def __init__(self, client: Client):
        super().__init__(client)

        self.get = Get(client, self)

    @property
    def url(self):
        return "{}/auth".format(super().url)


class Get(API):
    def __init__(self, client: Client, auth: Auth):
        super().__init__(client)
        self.auth = auth

    def __call__(self, access_token: str, page: Optional[int], limit: Optional[int]):
        return self.client.post(
            "{}/products/auths".format(super().url),
            data=OptionalDict(page=page, limit=limit) or None,
            auth=self.get_auth(access_token),
        )

    @property
    def url(self):
        return self.auth.url
