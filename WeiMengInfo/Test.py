# Author:Aliex ZJ
# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import datetime
import json
import time

from selenium import webdriver


option = webdriver.ChromeOptions()
driver = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=option)
driver.get('https://dopen.weimob.com/fuwu/b/oauth2/authorize?enter=wm&view=pc&response_type=code&scope=default&client_id=EDD3EAB6F807344E8AB5AE583A3E073C&redirect_uri=https://www.baidu.com')
