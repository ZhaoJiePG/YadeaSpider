# Author:Aliex ZJ
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import json
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#定义一个taobao类
class taobao_infos:

    #对象初始化
    def __init__(self):
        url = 'https://login.taobao.com/member/login.jhtml'
        self.url = url

        options = webdriver.ChromeOptions()
        # options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2}) # 不加载图片,加快访问速度
        options.add_experimental_option('excludeSwitches', ['enable-automation']) # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium

        self.browser = webdriver.Chrome(executable_path=chromedriver_path, options=options)
        self.wait = WebDriverWait(self.browser, 10) #超时时长为10s


    #登录淘宝
    def login(self):

        self.browser.maximize_window()#页面最大化
        # 打开网页
        self.browser.get(self.url)

        # 等待 密码登录选项 出现
        password_login = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.qrcode-login > .login-links > .forget-pwd')))
        password_login.click()

        # 等待 微博登录选项 出现
        weibo_login = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.weibo-login')))
        weibo_login.click()

        # 等待 微博账号 出现
        weibo_user = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.username > .W_input')))
        weibo_user.send_keys(weibo_username)

        # 等待 微博密码 出现
        weibo_pwd = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.password > .W_input')))
        weibo_pwd.send_keys(weibo_password)

        # 等待 登录按钮 出现
        submit = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.btn_tip > a > span')))
        submit.click()

        # 直到获取到淘宝会员昵称才能确定是登录成功
        taobao_name = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.site-nav-bd > ul.site-nav-bd-l > li#J_SiteNavLogin > div.site-nav-menu-hd > div.site-nav-user > a.site-nav-login-info-nick ')))
        # 输出淘宝昵称
        print(taobao_name.text)


        # 点击账号进入购物车
        self.browser.get('https://h5.m.taobao.com/cart/order.html?itemId=45310442213&item_num_id=45310442213&_input_charset=utf-8&buyNow=true&v=0&skuId=4229240488184&quantity=1&spm=a215p.8274340.4.d1&visa=701e9209f542c59d&_s')
        # submit = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.site-nav-login-info-nick')))
        # submit.click()
        # submit = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.mt-menu-item > dd > a')))
        # submit.click()



if __name__ == "__main__":
    chromedriver_path = "D:\Maven\YadeaSpider\chromedriver.exe"
    weibo_username = "18168546559"
    weibo_password = "zj123!"
