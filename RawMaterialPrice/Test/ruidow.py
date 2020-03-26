import datetime
import random
import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd
import pymysql
from lxml import etree
import requests
import json
import requests
import base64
from io import BytesIO
from PIL import Image
from sys import version_info
from PIL import Image
import os
from Utils import stringUtils
from Utils.stringUtils import delSpecialChars


def base64_api(uname, pwd, img):
    img = img.convert('RGB')
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    if version_info.major >= 3:
        b64 = str(base64.b64encode(buffered.getvalue()), encoding='utf-8')
    else:
        b64 = str(base64.b64encode(buffered.getvalue()))
    data = {"username": uname, "password": pwd, "image": b64}
    result = json.loads(requests.post("http://api.ttshitu.com/base64", json=data).text)
    if result['success']:
        return result["data"]["result"]
    else:
        return result["message"]
    return ""

def delFileDirs(name):
    for root, dirs, files in os.walk(name, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
    for name in dirs:
        os.rmdir(os.path.join(root, name))
    os.removedirs('test')

login_url = 'https://www.ruidow.com/login'

option = webdriver.ChromeOptions()
# option.add_argument('headless')
driver = webdriver.Chrome(executable_path='../chromedriver.exe', chrome_options=option)

driver.get(login_url)

# 账号密码
userName = driver.find_element_by_xpath("/html/body/div[3]/div/div[2]/div/div/div[2]/div/input")
userName.send_keys('hengci')
password = driver.find_element_by_xpath("/html/body/div[3]/div/div[2]/div/div/div[3]/div/input")
password.send_keys('123321')

print("保存gif到本地")
image = driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/div/div[4]/div/img')
url = image.get_attribute('src')

# 删除文件
try:
    delFileDirs('test')
except UnboundLocalError:
    print("文件不存在，不需要删除")
driver.maximize_window()
sleep(1)
driver.save_screenshot('screen.png')

# gif转img
response = requests.get(url)
with open("./test.gif",'wb') as file:
    file.write(response.content)

gifFileName = './test.gif'
#使用Image模块的open()方法打开gif动态图像时，默认是第一帧
im = Image.open(gifFileName)
pngDir = gifFileName[:-4]
#创建存放每帧图片的文件夹
os.mkdir(pngDir)
try:
    while True:
        #保存当前帧图片
        current = im.tell()
        im.save(pngDir+'/'+str(current)+'.png')
        #获取下一帧图片
        im.seek(current+1)
except EOFError:
    pass

print("保存图片")
driver.maximize_window()
sleep(1)
driver.save_screenshot('screen.png')

im = Image.open('screen.png')

# 图片的宽度和高度
img_size = im.size
print("图片宽度和高度分别是{}".format(img_size))
'''
裁剪：传入一个元组作为参数
元组里的元素分别是：（距离图片左边界距离x， 距离图片上边界距离y，距离图片左边界距离+裁剪框宽度x+w，距离图片上边界距离+裁剪框高度y+h）
'''
# 截取图片中一块宽和高都是250的
x = 940
y = 430
w = 90
h = 30
region = im.crop((x, y, x+w, y+h))
region.save("screen.png")



img_path = "screen.png"
img = Image.open(img_path)
result = base64_api(uname='luanjing312', pwd='lj940312', img=img)
print("验证码是"+result)


yanzhengma = driver.find_element_by_xpath("/html/body/div[3]/div/div[2]/div/div/div[4]/div/input")
yanzhengma.send_keys(result)

driver.find_element_by_xpath("/html/body/div[3]/div/div[2]/div/div/div[5]/input").click()
sleep(10)
driver.get('https://www.ruidow.com/market/detail?id=15844133425715')
sleep(2)

selector = etree.HTML(driver.page_source)
print(selector.xpath('/html/body/div[3]/div/div[2]/div/div[2]/table[1]/tbody/tr[1]/td[1]/text()'))
print(selector.xpath('/html/body/div[3]/div/div[2]/div/div[2]/table[1]/tbody/tr[1]/td[3]/text()'))