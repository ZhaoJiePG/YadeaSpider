import re
from time import sleep

import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from Utils.stringUtils import delSpecialChars


timeout = 10
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

url = 'https://detail.tmall.com/item.htm?id=596816395443&skuId=4315774262712&areaId=320200&user_id=2817130358&cat_id=2&is_b=1&rn=46d9826dde3d0497b455413d55cd753e&on_comment=1'
driver.get(url)
# 等待评论数据渲染
selector = etree.HTML(driver.page_source)
sleep(10)

rate_list = selector.xpath('//div[@id="J_Reviews"]/div/div[6]/table/tbody/tr')
for rate in rate_list:
    print(delSpecialChars(rate.xpath('./td[1]/div[1]/div[1]/text()')[0]))
    print("====================")

# 点击下一页
# next_button = WebDriverWait(driver, timeout).until(
#     lambda d: d.find_element_by_xpath('/html/body/div[5]/div/div[4]/div/div[1]/div/div[10]/div[1]/div/div[7]/div/a[3]'))
# next_button.click()

print(selector.xpath('/html/body/div[5]/div/div[4]/div/div[1]/div/div[10]/div[1]/div/div[7]/div/a[3]/text()'))
