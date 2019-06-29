# -*- coding: utf-8 -*-
import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['icebear.me']
    start_urls = ['http://icebear.me/']

    def parse(self, response):
        pass
