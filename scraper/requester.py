import sys
import requests
import logging

logger = logging.basicConfig(filename='../logging.conf', level=logging.DEBUG)

class PageRequester():

    def __init__(self, base_url, uri, url_id):
        """"""
        self.base_url = base_url
        self.uri = uri
        self.url_id = url_id
        self.url = "{0}{1}{2}".format(self.base_url, self.uri, self.url_id)

    def simple_request(self):
        try:
            session = requests.Session()
            session.headers = {'User-agent': 'Mozilla/5.0 Chrome/57.0.2987.110'}
            session.headers.update({
                'content-type': 'application/x-www-form-urlencoded'
            })
            req = session.post(self.url)
            return req.text
        except RuntimeError as e:
            print(e)
            print("Invalid input")
            sys.exit(1)

