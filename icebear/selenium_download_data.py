#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from selenium import webdriver

if __name__ == '__main__':
    # 调用环境变量指定的PhantomJS浏览器创建浏览器对象
    # driver = webdriver.PhantomJS()
    driver = webdriver.Chrome()
    driver.get("https://icebear.me/job.html#0!0!0!0!0!0!!1")
    js = "window.scrollTo(0, document.body.scrollHeight)"
    for i in range(500):
        print("滚动: " + str(i))
        driver.execute_script(js)
    print("===滚动完毕===")
    span_list = driver.find_element_by_xpath("//*[@class='companyName']")
    text = span_list.text
    print(text)
    print(type(span_list))
    source = driver.page_source
    with open("a.html", "w", encoding="utf-8") as f:
        f.write(source)
        f.flush()
