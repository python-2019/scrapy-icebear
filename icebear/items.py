# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IcebearItem(scrapy.Item):
    # define the fields for your item here like:
    # 公司
    company_name = scrapy.Field()
    # 职位类别
    post_category = scrapy.Field()
    # 职位描述
    post_desc = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 详情链接
    href = scrapy.Field()
    # 投递方式
    deliver_way = scrapy.Field()
    # 投递说明
    deliver_desc = scrapy.Field()
    # 公司简介
    company_desc = scrapy.Field()
