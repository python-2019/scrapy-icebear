#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lxml import etree
from lxml.html.clean import Cleaner

if __name__ == '__main__':
    """
    使用cookie登录
        {"session_login_token_login_info":"NGyVd0L7R950C1ltEolEliOAQeEqEPKkB2CPH4X1BDtVIHjCNpwTRon2_1xwWH07MQRSSIWSxTSEMReUZWue5HmDpRUmz9ucscZHjAxBUHlESzOho5l-kcq1NNKWBD4DMZPeTmpF1bqgTSy5Fkd1pHPkC3M8r7mUpNgOssH7xeTBmPW9Mys21zm-IjWJNfHmruefxcWewEtJVCMTromBs_sC5KyTYiXuB6UwdoUvOOvno6f2FVOlSvCboxdPbOg5t2iGlIG-gwUFK1SBMy5HKiGy8STlk_yakrHV4w2nhttzG7dzaYe69r1TZltZDtOwyBndufzX1jM221MHKYIMKxKLY5VROd0kKPdSlQwbW05lUJ1H-zzJemicB2bcX3sG14X1WIEWuxofzoCbrIGx6MDSkYPI7Ej6DEUbw1jsU4DlGt0CRan7T1qjJWCD0wUNjxauQZ32_1_2JOCjM20T_kGO"}
    """
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