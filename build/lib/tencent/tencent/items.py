# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TencentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()  # 职位名称
    category = scrapy.Field()  # 职位类别
    publish_time = scrapy.Field()  # 发布时间
    content = scrapy.Field()  # 工作职责