from project_dir.spiders.douban import DouBanSpider
from scrapy_plus.core.engine import Engine
from spiders.baidu import BaiduSpider

if __name__ == '__main__':
    spider = BaiduSpider()
    #engine = Engine(spider)
    douban = DouBanSpider()
    engine = Engine(douban)
    engine.start()