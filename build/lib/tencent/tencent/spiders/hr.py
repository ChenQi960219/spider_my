# -*- coding: utf-8 -*-
import scrapy

# 导入该类
from tencent.items import TencentItem

"""
增加提取详情页的工作职责信息

1. 修改TencentItem增加工作职责字段
2. 构建详情页的请求, 交给引擎
3. 定义一个函数, 来处理详情的请求
"""


class HrSpider(scrapy.Spider):
    # 爬虫名称
    name = 'hr'
    # 允许域名
    allowed_domains = ['tencent.com']
    # 起始的URL
    start_urls = ['https://hr.tencent.com/position.php']

    def parse(self, response):
        """提取数据"""
        # 提取招聘的职位名称, 职位类别, 发布时间信息
        # 1. 获取包含招聘信息tr列表
        # 注意: Element中有tbody但是, response没有, 所以我们写XPATH中也不能有tbody
        # 第1行是表头, 最后一行是分页
        trs = response.xpath('//*[@id="position"]/div[1]/table/tr')[1:-1]
        # print(trs)
        # 遍历trs, 获取需要的数据
        for tr in trs:
            # item = {}
            item = TencentItem()
            # 职位名称, 职位类别, 发布时间信息
            item['name'] = tr.xpath('./td[1]/a/text()').extract_first()
            item['category'] = tr.xpath('./td[2]/text()').extract_first()
            item['publish_time'] = tr.xpath('./td[last()]/text()').extract_first()
            # 把数据交给引擎
            # yield item
            # 2. 构建详情页的请求, 交给引擎
            # 2.1 获取详情页URL
            # position_detail.php?id=43965&keywords=&tid=0&lid=0
            detail_url = tr.xpath('./td[1]/a/@href').extract_first()
            # 把URL补全
            detail_url = response.urljoin(detail_url)
            # 2.2 构建Request请求, 交给引擎
            # 详情页对应响应数据交给parse_detail函数进行处理
            yield scrapy.Request(detail_url, callback=self.parse_detail, meta={'item':item})

        # 实现列表的翻页
        # 1. 获取下一页的URL
        next_url = response.xpath('//a[text()="下一页"]/@href').extract_first()
        if next_url != 'javascript:;':
            # 有下一页
            # next_url = 'https://hr.tencent.com/' + next_url
            # response.urljoin可以自动拼接URL: 本质就是用响应的URL, 对URL进行补全
            next_url = response.urljoin(next_url)

            # 构造一个Request请求, 交给引擎
            # callback: next_url对应数据, 交给那个函数来处理
            # 如果不指定, 就交给parse函数处理
            yield scrapy.Request(next_url, callback=self.parse)


    def parse_detail(self, response):
        """处理详情页"""
        item = response.meta['item']
        # 提取详情页数据
        item['content'] = ''.join(response.xpath('//*[@id="position_detail"]/div/table/tr[3]/td/ul//text()').extract())
        # 把数据交给引擎
        # return item
        yield item