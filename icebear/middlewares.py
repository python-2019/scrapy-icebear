# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
from time import sleep

from scrapy import signals
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
from logging import getLogger

from icebear.URLFilter import UrlFilterAndAdd


class IcebearSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class IcebearDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SeleniumMiddleware():
    def __init__(self, timeout=None, service_args=[]):
        self.is_first = True
        self.logger = getLogger(__name__)
        # self.timeout = timeout
        # self.driver = webdriver.Chrome(executable_path="E:/exe/chromdriver")
        self.driver = webdriver.Chrome()
        # self.driver.set_window_size(1400, 700)
        # self.driver.set_page_load_timeout(self.timeout)
        # self.wait = WebDriverWait(self.browser, self.timeout)
        self.dupefilter = UrlFilterAndAdd()

    def __del__(self):
        self.driver.close()

    def process_request(self, request, spider):
        """
        Chrome
        :param request: Request对象
        :param spider: Spider对象
        :return: HtmlResponse
        """
        self.driver.get(request.url)
        self.logger.debug('Chrome is Starting: %s' % request.url)
        if (self.is_first):
            print("首次进入: 开始等待页面加载...")
            sleep(3)
            js = "window.scrollTo(0, document.body.scrollHeight)"
            for i in range(1500):
                self.driver.execute_script(js)
                self.is_first = False
            print("页面加载完毕返回spider处理...")
            with open("a.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
                f.flush()
        if (self.is_first == False):
            self.dupefilter.add_url(request.url)
        return HtmlResponse(url=request.url, body=self.driver.page_source, request=request, encoding='utf-8',
                            status=200)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
                   service_args=crawler.settings.get('PHANTOMJS_SERVICE_ARGS'))
