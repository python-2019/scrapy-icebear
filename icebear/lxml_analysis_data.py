#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lxml import etree
from lxml.html.clean import Cleaner

if __name__ == '__main__':
    host = "https://icebear.me"
    with open("a.html", 'r', encoding='utf-8') as f:
        content = f.read()
    cleaner = Cleaner(style=True, scripts=True, page_structure=False, safe_attrs_only=False)
    htmlEmt = etree.HTML(cleaner.clean_html(content))
    li_list = htmlEmt.xpath("//li[@class='comItem']")
    print(len(li_list))
    for li in li_list:
        dict = {}
        dict['company_name'] = li.xpath("./div/div[1]/div[1]/span[@class='companyName']/text()")
        dict['post'] = li.xpath("./div/div[1]/div[2]/span/text()")
        dict['city'] = li.xpath("./div/div[1]/div[3]/span/text()")
        dict['href'] = host+li.xpath("./div/div[1]/@data-url")[0]
        print(dict)