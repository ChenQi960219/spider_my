from collections import Iterator
from datetime import  datetime

from ..http.request import Request
from .downloader import Downloader
from .scheduler import Scheduler

from .pipeline import Pipeline
from ..middlewares.spider_middlewares import SpiderMiddleware
from ..middlewares.downler_middlewares import DownloaderMiddleware
from ..utils.log import logger

class Engine(object):

    def __init__(self, spider):

        self.spider = spider
        self.scheduler = Scheduler()
        self.downloader = Downloader()
        self.pipeline = Pipeline()
        self.spider_middle = SpiderMiddleware()
        self.downloader_middle = DownloaderMiddleware()

        self.get_response_nums = 0

    def start(self):
        start = datetime.now()
        logger.info('开始运行时间: %s' %start)
        self.__start()
        end = datetime.now()
        logger.info('结束运行时间: %s' %end)
        logger.info('耗时: %.2f 秒' %(end-start).total_seconds())

    def __start(self):

        self.add_url_request()

        while True:
            self.get_response()

            if self.get_response_nums >= self.scheduler.total_response_nums:
                break

    def get_response(self):
        request = self.scheduler.get_request()

        request = self.downloader_middle.process_request(request)
        response = self.downloader.get_response(request)

        response.meta = request.meta

        response = self.downloader_middle.process_response(response)
        response = self.spider_middle.process_response(response)

        if request.callback:
            results = request.callback(response)
        else:
            results = self.spider.parse(response)
        if not isinstance(results, Iterator):
            results = [results]
        for result in results:
            if isinstance(result, Request):
                result = self.spider_middle.process_request(result)
                self.scheduler.add_request(result)

            else:
                self.pipeline.process_item(result)

        self.get_response_nums += 1

    def add_url_request(self):
        for request in self.spider.start_requests():
            request = self.spider_middle.process_request(request)
            self.scheduler.add_request(request)



