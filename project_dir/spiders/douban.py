from scrapy_plus.core.spider import Spider
from scrapy_plus.http.request import Request
from scrapy_plus.item import Item


class DouBanSpider(Spider):

    def start_requests(self):
        start_url_pattern = 'http://movie.douban.com/top250?start={}'
        for num in range(0, 250, 25):
            start_url = start_url_pattern.format(num)

            yield Request(start_url)

    def parse(self, response):
        divs = response.xpath('//*[@id="content"]/div/div[1]/ol/li')
        for div in divs:
            dic = {}
            #dic['url'] = response.url
            dic['name'] = div.xpath('./div/div[2]/div[1]/a/span[1]/text()')[0]
            item = Item(dic)
            detail_url = div.xpath('./div/div[2]/div[1]/a/@href')[0]
            #yield item
            yield Request(detail_url,callback=self.parse_detail,meta={'item':item})

    def parse_detail(self, response):
        item = response.meta['item']
        print(item)
        return item

