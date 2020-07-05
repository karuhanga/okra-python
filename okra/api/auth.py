from typing import Optional, Any

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

    def by_customer(self, access_token: str, customer: str, page: Optional[int], limit: Optional[int]):
        return self._by_criteria(
            "getByCustomer",
            access_token,
            customer=customer,
            page=page,
            limit=limit,
        )

    def by_date(self, access_token: str, to: str, _from: str, page: Optional[int], limit: Optional[int]):
        return self._by_criteria(
            "getByDate",
            access_token,
            to=to,
            **{"from": _from},
            page=page,
            limit=limit,
        )

    def by_options(self, access_token: str, options: Any, page: Optional[int], limit: Optional[int]):
        return self._by_criteria(
            "byOptions",
            access_token,
            options=options,
            page=page,
            limit=limit,
        )

    def by_bank(self, access_token: str, bank: str, page: Optional[int], limit: Optional[int]):
        return self._by_criteria(
            "getByBank",
            access_token,
            bank=bank,
            page=page,
            limit=limit,
        )

    def by_id(self, access_token: str, _id: str, page: Optional[int], limit: Optional[int]):
        return self._by_criteria(
            "getById",
            access_token,
            id=_id,
            page=page,
            limit=limit,
        )

    def _by_criteria(self, endpoint: str, access_token: str, **kwargs):
        return self.client.post(
            "{}/{}".format(self.auth.url, endpoint),
            params=kwargs,
            auth=self.get_auth(access_token),
        )
