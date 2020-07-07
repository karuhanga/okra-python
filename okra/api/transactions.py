from typing import Optional

from okra.api.base import API
from okra.api.utils import OptionalDict
from okra.client import Client


class Transactions(API):
    def __init__(self, client: Client):
        super().__init__(client)

        self.get = Get(client, self)

    @property
    def url(self):
        return "{}/transactions".format(super().url)


class Get(API):
    def __init__(self, client: Client, transactions: Transactions):
        super().__init__(client)
        self.transactions = transactions

    def __call__(self, access_token: str, page: Optional[int], limit: Optional[int]):
        return self.client.post(
            "{}/products/transactions".format(super().url),
            data=OptionalDict(page=page, limit=limit) or None,
            auth=self.get_auth(access_token),
        )

    @property
    def url(self):
        return self.transactions.url

    def by_account(self, access_token: str, account: str, page: Optional[int], limit: Optional[int]):
        return self._get_by_criteria("getByAccount", access_token, account=account, page=page, limit=limit,)

    def by_nuban(self, access_token: str, nuban: str, page: Optional[int], limit: Optional[int]):
        return self._get_by_criteria("getByNuban", access_token, nuban=nuban, page=page, limit=limit,)

    def by_type(self, access_token: str, _type: str, page: Optional[int], limit: Optional[int]):
        return self._get_by_criteria("getByType", access_token, **{"type": _type}, page=page, limit=limit,)
