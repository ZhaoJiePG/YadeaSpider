# Author:Aliex ZJ
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from selenium import webdriver


class googleWebDriver:
    def __init__(self):
        option = webdriver.ChromeOptions()
        option.add_argument('--proxy--server=127.0.0.1:8080')
        # 防止机器识别
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 不加载图片,加快访问速度
        # option.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        # option.add_argument('headless')

        # 要换成适应自己操作系统的chromedriver
        driver = webdriver.Chrome(
            executable_path='D:\Maven\YadeaSpider\chromedriver.exe',
            chrome_options=option
        )
