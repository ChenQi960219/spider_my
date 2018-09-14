# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

class TencentFilePipeline(object):

    def open_spider(self, spider):
        """
        当前爬虫启动的时候执行, 只会执行一次
        :param spider: 爬虫名称
        用于: 打开文件, 建立数据连接
        """
        if spider.name == 'hr':
            self.file = open('hr.jsonlines', 'w', encoding='utf8')


    def process_item(self, item, spider):
        """
            item : 数据
            spider: 该数据对应爬虫
            引擎获取到没一个数据都会调用该方法, 调用频率非常高
            如果每次都在这里打开和关闭文件效率非常差.

            with open('hr.jsonlines', 'a', encoding='utf8') as f:
        """
        if spider.name == 'hr':
            #  Object of type 'TencentItem' is not JSON serializable
            # 把item转换字典: dict(item)
            json.dump(dict(item), self.file, ensure_ascii=False)
            self.file.write('\n')


        # 为了后面管道能够使用该数据, 就必须返回
        # 否则后面的管道就获取不到数据了.
        return item

    def close_spider(self, spider):
        """
        当爬虫关闭的时候执行, 只执行一次
        :param spider: 爬虫对象
        作用: 关闭文件, 关闭数据库连接
        """
        if spider.name == 'hr':
            self.file.close()


# 写一个ItemPipeline用于把数据存储到MongoDB
from pymongo import MongoClient

class TencentMongoItem(object):

    def open_spider(self, spider):
        """建立MongoDB数据连接, 获取要操作的集合"""
        if spider.name == 'hr':
            self.client = MongoClient('127.0.0.1', 27017)
            self.col = self.client['tencent']['hr']

    def process_item(self, item, spider):
        """把数据插入到MongoDB中"""
        if spider.name == 'hr':
            # TencentItem 对象 => dict
            self.col.insert(dict(item))

        return item

    def close_spider(self, spider):
        if spider.name == 'hr':
            # 关闭MongoDB数据库连接
            self.client.close()