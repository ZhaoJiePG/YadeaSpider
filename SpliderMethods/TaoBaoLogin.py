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
        # submit = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.site-nav-login-info-nick')))
        # submit.click()
        # submit = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.mt-menu-item > dd > a')))
        # submit.click()

        # 选择购买
        # sleep(5)
        # submit = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_SelectAll1 > .cart-checkbox')))
        # submit.click()
        # submit = self.browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div[4]/div[2]/div[3]/div[5]/a')
        # submit.click()

        # 这里是为了等待手机扫码登录, 登录后回车即可
        input("请回车登录")
        dictCookies = self.browser.get_cookies()
        jsonCookies = json.dumps(dictCookies)
        # 登录完成后,将cookies保存到本地文件
        with open("./cookies_tao.json", "w") as fp:
            fp.write(jsonCookies)

        a.browser.quit()

if __name__ == "__main__":
    chromedriver_path = "D:\Maven\YadeaSpider\chromedriver.exe"
    weibo_username = "18168546559"
    weibo_password = "zj123!"

    #登录
    # a = taobao_infos()
    # a.login()

    # 使用cookie跳转
    b = taobao_infos()
    # 删除第一次登录是储存到本地的cookie
    b.browser.delete_all_cookies()
    # 读取登录时储存到本地的cookie
    with open("D:\Maven\YadeaSpider\SpliderMethods\cookies_tao.json", "r", encoding="utf8") as fp:
        ListCookies = json.loads(fp.read())
    for cookie in ListCookies:
        b.browser.add_cookie({
            'domain': '.taobao.com',  # 此处xxx.com前，需要带点
            'name': cookie['name'],
            'value': cookie['value'],
            'path': '/',
            'expires': None
        })
    b.browser.get('https://detail.tmall.com')