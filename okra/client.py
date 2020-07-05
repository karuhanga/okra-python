import requests as requests

from okra.api import Auth


class Client:
    post = requests.post

    def __init__(self):
        self.auth = Auth(self)
