import re
from time import sleep

import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from Utils.stringUtils import delSpecialChars
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

url = 'https://detail.tmall.com/item.htm?id=596816395443&skuId=4315774262712&areaId=320200&user_id=2817130358&cat_id=2&is_b=1&rn=46d9826dde3d0497b455413d55cd753e&on_comment=1'
driver.get(url)
# 等待评论数据渲染
element = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, '//div[@class="rate-grid"]'))
)
selector = etree.HTML(driver.page_source)
rates_list = selector.xpath('//div[@class="rate-grid"]/table/tbody/tr')
for rates in rates_list:
    print(rates.xpath('./td[@class="tm-col-master"]/div[@class="tm-rate-content"]/div[@class="tm-rate-fulltxt"]/text()'))
print(selector.xpath('/html/body/div[5]/div/div[4]/div/div[1]/div/div[10]/div[1]/div/div[6]/table/tbody/tr[1]/td[1]/div[1]/div[1]/text()'))




