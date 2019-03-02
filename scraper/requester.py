import sys
import requests
import logging


class PageRequester(object):

    def __init__(self):
        """"""
        self.uri = ""
        self.url = "{0}{1}".format(self.uri, "")
        # self.credentials = (user_name, password)

    def simple_request(self):
        try:
            # req = requests.get(self.url, auth=self.credentials)
            req = requests.get(self.url)
            return req.text
        except RuntimeError as e:
            print(e)
            print("Invalid input")
            sys.exit(1)

