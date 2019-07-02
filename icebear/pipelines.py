# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime

import xlsxwriter
from scrapy.conf import settings


class IcebearPipeline(object):
    def open_spider(self, spider):
        self.col = "A"
        self.row_num = 1
        file_path = settings.get("FILE_PATH") + '白熊实习.xlsx'
        self.workbook = xlsxwriter.Workbook(file_path)
        headers = ['公司', '职位类别', '职位描述', '城市', '详情链接', '投递方式', '投递说明', '公司简介']
        # 新建sheet（sheet的名称为"sheet1"）
        self.worksheet = self.workbook.add_worksheet('sheet1')
        # 插入头部
        self.worksheet.write_row("A1", headers)

    def process_item(self, item, spider):
        company_name = item['company_name']
        post_category = item['post_category']
        post_desc = item['post_desc']
        city = item['city']
        href = item['href']
        deliver_way = item['deliver_way']
        deliver_desc = item['deliver_desc']
        company_desc = item['company_desc']
        row = [company_name, post_category, post_desc, city, href, deliver_way, deliver_desc, company_desc]
        self.row_num = self.row_num + 1
        col_row = self.col + str(self.row_num)
        self.worksheet.write_row(col_row, row)
        print(company_name)
        return item

    def close_spider(self, spider):
        self.workbook.close()
