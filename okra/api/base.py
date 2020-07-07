from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Any

from requests.auth import AuthBase

from okra.client import Client


class API(ABC):
    def __init__(self, client: Client):
        self.client = client

    @property
    @abstractmethod
    def url(self):
        return self.client.url

    @staticmethod
    def get_auth(access_token: str):
        return _TokenAuth(access_token)

    def _get_by_criteria(self, endpoint: str, access_token: str, **kwargs):
        return self.client.post("{}/{}".format(self.url, endpoint), params=kwargs, auth=self.get_auth(access_token),)

    def by_id(self, access_token: str, _id: str, page: Optional[int], limit: Optional[int]):
        return self._get_by_criteria("getById", access_token, id=_id, page=page, limit=limit,)

    def by_bank(self, access_token: str, bank: str, page: Optional[int], limit: Optional[int]):
        return self._get_by_criteria("getByBank", access_token, bank=bank, page=page, limit=limit,)

    def by_customer(self, access_token: str, customer: str, page: Optional[int], limit: Optional[int]):
        return self._get_by_criteria("getByCustomer", access_token, customer=customer, page=page, limit=limit,)

    def by_date(self, access_token: str, to: datetime, _from: datetime, page: Optional[int], limit: Optional[int]):
        return self._get_by_criteria(
            "getByDate", access_token, to=to.isoformat(), **{"from": _from.isoformat()}, page=page, limit=limit,
        )

    def by_options(self, access_token: str, options: Any, page: Optional[int], limit: Optional[int]):
        return self._get_by_criteria("byOptions", access_token, options=options, page=page, limit=limit,)


class _TokenAuth(AuthBase):
    def __init__(self, access_token: str):
        self.access_token = access_token

    def __call__(self, request):
        request.headers["Authorization"] = "Bearer {}".format(self.access_token)
        return request
