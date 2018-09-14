# -*- coding: utf-8 -*-
import re
from copy import deepcopy

import scrapy


class SuningSpider(scrapy.Spider):
    name = 'suning'
    allowed_domains = ['suning.com']
    start_urls = ['http://book.suning.com/']

    def parse(self, response):

        dls = response.xpath('//div[@class="menu-item"]/dl')
        sub_divs = response.xpath('//div[contains(@class, menu-sub)]')
        # sub_divs = response.xpath('//div[@class="menu-item"]/dl/dt/h3/a')
        for index, dl in enumerate(dls):
            item = {}
            item['b_category_name'] = dl.xpath('./dt/h3/a/text()').extract_first()
            item['b_category_url'] = dl.xpath('./dt/h3/a/@href').extract_first()

            a_s = dl.xpath('./dd/a')

            if len(a_s) == 0:
                sub_div = sub_divs[index]
                a_s = sub_div.xpath('./div[1]/ul/li/a')

            for a in a_s:
                item['s_category_name'] = a.xpath('./text()').extract_first()
                item['s_category_url'] = a.xpath('./@href').extract_first()

                yield scrapy.Request(item['s_category_url'],callback=self.parse_book_list,meta={'item':deepcopy(item)})

    def parse_book_list(self,response):
        item = response.meta['item']

        lis = response.xpath('//*[@id="filter-results"]/ul/li')
        for li in lis:
            item['book_img'] = 'https:'+li.xpath('./div/div/div/div[1]/div/a/img/@src2').extract_first()
            item['book_title'] = li.xpath('./div/div/div/div[2]/p[2]/a/text()').extract_first()

            url = 'https:' + li.xpath('./div/div/div/div[2]/p[2]/a/@href').extract_first()
            yield scrapy.Request(url,callback=self.book_detail,meta={'item':deepcopy(item)})

        # 出版商

    def book_detail(self, response):
        item = response.meta['item']

        item['book_publisher']=response.xpath('//*[@id="productName"]/a/text()').extract_first()

        price_url = 'https://pas.suning.com/nspcsale_0_000000000{}_000000000{}_{}_190_020_0200101.html'
        # 价格信息
        rs = re.findall(r'https://product.suning.com/(\d+)/(\d+).html', response.url)[0]
        price_url = price_url.format(rs[1],rs[1],rs[0])

        yield scrapy.Request(price_url,callback=self.parse_book_detail,meta={'item':item})

    def parse_book_detail(self,response):

        item = response.meta['item']

        price = re.findall('"promotionPrice":\s*"(\d+.\d+)"', response.text)
        if len(price) == 0:
            price = re.findall('"netPrice":\s*"(\d+.\d+)"', response.text)
        item['book_price'] = price[0]

        yield item
