from ..http.request import Request
from ..item import Item


class Spider(object):

    start_url = []

    def start_requests(self):

        for url in self.start_url:

            yield Request(url)


    def parse(self, response):
        item = Item(response.url)
        return item