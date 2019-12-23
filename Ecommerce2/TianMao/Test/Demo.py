# Author:Aliex ZJ
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import datetime
import re
from time import sleep

import requests
from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver

# print(requests.get(url).text)
from selenium.webdriver.support.wait import WebDriverWait

from Utils.fileUtils import fileUtils
from Utils.stringUtils import delSpecialChars

add_time = datetime.datetime.now().strftime('%Y-%m-%d')
timeout=5

def TMProductInfos(topic):
    option = webdriver.ChromeOptions()
    option.add_argument('--proxy--server=127.0.0.1:8080')
    # 防止机器识别
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 不加载图片,加快访问速度
    option.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    # option.add_argument('headless')

    # 要换成适应自己操作系统的chromedriver
    driver = webdriver.Chrome(
        executable_path='D:\Maven\YadeaSpider\chromedriver.exe',
        chrome_options=option
    )
    # 登陆淘宝
    login_url= 'https://login.taobao.com/member/login.jhtml'
    driver.get(login_url)
    # 等待 密码登录选项 出现
    password_login = driver.find_element_by_xpath('//div[@class="login-links"]/a[@class="forget-pwd J_Quick2Static"]')
    password_login.click()
    # 等待 微博登录选项 出现
    weibo_login = driver.find_element_by_xpath('//a[@class="weibo-login"]')
    weibo_login.click()
    # 等待 微博账号 出现
    weibo_user = WebDriverWait(driver, timeout).until(
        lambda d: d.find_element_by_xpath('//div[@id="pl_login_logged"]/div/div[2]/div/input'))
    weibo_user.send_keys('18168546559')
    sleep(1)
    # 等待 微博密码 出现
    weibo_pwd = WebDriverWait(driver, timeout).until(
        lambda d: d.find_element_by_xpath('//div[@id="pl_login_logged"]/div/div[3]/div/input'))
    weibo_pwd.send_keys('zj123!')
    # 等待 登录按钮 出现
    submit = WebDriverWait(driver, timeout).until(
        lambda d: d.find_element_by_xpath('//div[@id="pl_login_logged"]/div/div[7]/div[1]/a/span'))
    submit.click()
    sleep(10)

    #产品信息集合
    products_lists=[]
    # 搜索主页（切换天猫）
    driver.get('https://www.tmall.com/')
    # qiehuan = WebDriverWait(driver, timeout).until(
    #     lambda d: d.find_element_by_xpath('/html/body/div[3]/div/ul[1]/li[1]/a'))
    # qiehuan.click()
    # driver.close()
    # 切换到右边
    # window_handles = driver.window_handles
    # driver.switch_to.window(window_handles[-1])
    # 搜索天猫
    search_input = WebDriverWait(driver, timeout).until(
        lambda d: d.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div[2]/form/fieldset/div/div/div/input'))
    search_input.send_keys(topic+'电动车')
    submit = WebDriverWait(driver, timeout).until(
        lambda d: d.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div[2]/form/fieldset/div/button'))
    submit.click()
    sleep(2)
    # 请求地址获取连接
    xpath_date = etree.HTML(driver.page_source)
    # 获取当前搜素商品总页数
    page_sum = xpath_date.xpath('//div[@class="ui-page-wrap"]/b[2]/form/input[3]/@value')[0]
    print("当前搜索总共"+page_sum+"页")
    # 循环获取每页的部分数据
    for index in range(0,int(page_sum)):
        print("开始获取第"+str(index+1)+"页商品数据")
        # 获取每个商品的xpath集合
        xpath_dates = etree.HTML(driver.page_source)
        product_lists = xpath_dates.xpath('//div[@id="J_ItemList"]/div')
        option.add_argument('headless')
        driver2 = webdriver.Chrome(
            executable_path='D:\Maven\YadeaSpider\chromedriver.exe',
            chrome_options=option
        )
        # 获取每个商品属性
        for product_list in product_lists:
            # 商品属性
            product_price = product_list.xpath('./div/p[@class="productPrice"]/em/@title')[0]
            product_price = product_price[:-((product_price.index('.'))-1)]
            if(int(product_price)<1000):
                print("价格小于1000，非整车，跳出循环")
                break
            product_title = product_list.xpath('./div/p[@class="productTitle"]/a/@title')[0]
            product_url = 'http:'+product_list.xpath('./div/p[@class="productTitle"]/a/@href')[0]
            product_id = re.findall('//detail.tmall.com/item.htm\?id=(\d+)&',product_url)[0]
            shop_url = 'http:'+product_list.xpath('./div/div[@class="productShop"]/a[@class="productShop-name"]/@href')[0]
            shop_id = re.findall('user_number_id=(\d+)&',shop_url)[0]
            shop_name = product_list.xpath('./div/p[@class="productStatus"]/span[3]/@data-nick')[0]
            month_sale = product_list.xpath('./div/p[@class="productStatus"]/span/em/text()')[0]
            comment_sum = product_list.xpath('./div/p[@class="productStatus"]/span[2]/a/text()')[0]

            # 跳转商品url，获取详细信息
            driver2.get(product_url)
            selector = etree.HTML(driver2.page_source)
            shop_items = selector.xpath('//*[@id="J_AttrUL"]/li')
            # 商品详细配置描述
            shop_list = []
            for shop_item in shop_items:
                shop_list.append(delSpecialChars(shop_item.xpath('./text()')[0]))
            # 店铺评分
            score_list = []
            scores = selector.xpath('//*[@id="shop-info"]/div[2]/div')
            for score in scores:
                res_score = delSpecialChars(score.xpath('./div[1]/text()')[0])+delSpecialChars(score.xpath('./div[2]/span/text()')[0])
                score_list.append(res_score)
            # 收藏人气
            # popularity = '0人气'
            # try:
            #     popularity = delSpecialChars(selector.xpath('/html/body/div[5]/div/div[2]/div/div[1]/div[2]/p/span[2]/text()'))
            # except BaseException:
            #     print("没有收藏数据")
            # finally:
            #     popularity = re.findall('\d+',popularity)

            # 保存字典表
            prduct_dict = {'product_title':product_title,'product_id':product_id,'product_url':product_url,'product_price':product_price,
                           'month_sale':month_sale,"shop_name":shop_name,"shop_url":shop_url,"shop_id":shop_id,"comment_sum":comment_sum,
                           'add_time':add_time,'topic':topic,'shop_list':shop_list,'score_list':score_list}
            print(prduct_dict)
            products_lists.append(prduct_dict)
            # sleep(1)
        try:
        # 跳转下一页
            next_button = WebDriverWait(driver, timeout).until(
                    lambda d: d.find_element_by_xpath('//div[@class="ui-page"]/div/b/a[@class="ui-page-next"]'))
            next_button.click()
        except BaseException:
            print("没有下一页，跳出循环")
            break
        sleep(5)
        driver2.quit()
    fileUtils().saveAsCsv(products_lists,'./Data/Products/{0}'.format(topic))
    driver.quit()

if __name__ == '__main__':
    topic='新日'
    TMProductInfos(topic)