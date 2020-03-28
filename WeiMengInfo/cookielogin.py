# Author:Aliex ZJ
# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import json
import time

from selenium import webdriver


def getCookie(driver, login_url):
    driver.get(login_url)
    time.sleep(20)
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

    login_url = 'http://account.weimob.com/?back=http%3A%2F%2Fdopen.weimob.com%2Ffuwu%2Fb%2Foauth2%2Fauthorize%3Fenter%3Dwm%26view%3Dpc%26response_type%3Dcode%26scope%3Ddefault%26client_id%3DEDD3EAB6F807344E8AB5AE583A3E073C%26redirect_uri%3Dhttps%3A%2F%2Fwww.baidu.com'


    getCookie(driver,login_url)
    time.sleep(10)
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
    time.sleep(5)
    driver.get(login_url)

