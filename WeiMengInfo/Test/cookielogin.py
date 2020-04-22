# Author:Aliex ZJ
# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import json
import re
import time

from selenium import webdriver


def getCookie(driver, login_url):
    driver.get(login_url)
    time.sleep(30)
    print(driver.current_url)
    text = driver.page_source
    cookie = driver.get_cookies()
    print(cookie)
    jsonCookies = json.dumps(cookie)
    with open('WeiMengCookie.json', 'w') as f:
        f.write(jsonCookies)


def getCode(driver):
    pass


if __name__ == '__main__':
    option = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path='D:\Maven\YadeaSpider\RawMaterialPrice\chromedriver.exe',
                              chrome_options=option)


    login_url = "http://account.weimob.com/"
    getCookie(driver,login_url)



    driver.get(login_url)
    driver.delete_all_cookies()



    fr = open('WeiMengCookie.json', 'r')
    cookielist = json.load(fr)


    print(cookielist)

    fr.close()
    for cookie in cookielist:
        if 'expiry' in cookie:
            del cookie['expiry']
        driver.add_cookie(cookie)

    time.sleep(2)
    login_url = 'https://dopen.weimob.com/fuwu/b/oauth2/authorize?enter=wm&view=pc&response_type=code&scope=default&client_id=EDD3EAB6F807344E8AB5AE583A3E073C&redirect_uri=https://www.baidu.com'
    driver.get(login_url)
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/form/div[2]/a').click()
    time.sleep(1)
    print(driver.current_url)
    print(re.findall('code=(.*)',driver.current_url)[0])



