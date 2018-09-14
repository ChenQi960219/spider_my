from lxml import etree
import re
import json


class Response(object):

    def __init__(self, url, status_code, headers={}, body=None, meta=None):

        self.url = url
        self.staut_code = status_code
        self.headers =headers
        self.body =body
        self.meta = meta




    def xpath(self, path):
        element = etree.HTML(self.body)
        return element.xpath(path)

    def find_all(self, pattern, content=None):
        if content is None:
            content = self.body.decode()
            rs = re.findall(pattern, content)

    def json(self):

        return json.loads(self.body.decode())