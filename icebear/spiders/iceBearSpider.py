# -*- coding: utf-8 -*-
import copy

import scrapy
from lxml import etree
from scrapy import Request
from icebear.items import IcebearItem


class iceBearSpider(scrapy.Spider):
    name = 'icebear'
    allowed_domains = ['icebear.me']
    host = 'https://icebear.me'
    start_urls = ["https://icebear.me/job.html#0!0!0!0!0!0!!1"]
    cookies = {
        "session_login_token_login_info": "NGyVd0L7R950C1ltEolEliOAQeEqEPKkB2CPH4X1BDtVIHjCNpwTRon2_1xwWH07MQRSSIWSxTSEMReUZWue5HmDpRUmz9ucscZHjAxBUHlESzOho5l-kcq1NNKWBD4DMZPeTmpF1bqgTSy5Fkd1pHPkC3M8r7mUpNgOssH7xeTBmPW9Mys21zm-IjWJNfHmruefxcWewEtJVCMTromBs_sC5KyTYiXuB6UwdoUvOOvno6f2FVOlSvCboxdPbOg5t2iGlIG-gwUFK1SBMy5HKiGy8STlk_yakrHV4w2nhttzG7dzaYe69r1TZltZDtOwyBndufzX1jM221MHKYIMKxKLY5VROd0kKPdSlQwbW05lUJ1H-zzJemicB2bcX3sG14X1WIEWuxofzoCbrIGx6MDSkYPI7Ej6DEUbw1jsU4DlGt0CRan7T1qjJWCD0wUNjxauQZ32_1_2JOCjM20T_kGO"}

    def start_requests(self):
        yield Request(url=self.start_urls[0], callback=self.parse, dont_filter=True, cookies=self.cookies)

    def parse(self, response):
        li_list = response.xpath("//li[@class='comItem']")
        for li in li_list:
            item = IcebearItem()
            item['company_name'] = li.xpath("./div/div[1]/div[1]/span[@class='companyName']/text()").extract_first()
            item['post_category'] = li.xpath("./div/div[1]/div[2]/span/text()").extract_first()
            item['city'] = li.xpath("./div/div[1]/div[3]/span/text()").extract_first()
            item['href'] = self.host + li.xpath("./div/div[1]/@data-url").extract_first()
            print(item['href'])
            # 详情
            yield scrapy.Request(
                item['href'],
                callback=self.parse_detail,
                dont_filter=False,
                meta={'item': copy.deepcopy(item)}, cookies=self.cookies)

    def parse_detail(self, response):
        item = response.meta["item"]
        item['deliver_way'] = response.xpath("//div[@class='flex-center']/span/text()").extract_first()
        item['deliver_desc'] = response.xpath("//div[@class='ft15']/p/text()").extract_first()
        item['company_desc'] = response.xpath("//li[@class='item']/p[2]/text()").extract_first()
        item['post_desc'] = response.xpath("//div[@class='positionList']").xpath("string(.)").extract_first()
        if item['deliver_way'] is None:
            item['deliver_way'] = response.xpath("//div[@class ='flex-center']/a/@href").extract_first()
            item['deliver_desc'] = '详情见网址'
        yield item
