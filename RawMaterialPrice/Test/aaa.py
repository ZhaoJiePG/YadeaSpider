# Author:Aliex ZJ
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from time import sleep

from PIL import Image
from bs4 import element
from selenium import webdriver

option = webdriver.ChromeOptions()
# option.add_argument('headless')
driver = webdriver.Chrome(executable_path='../chromedriver.exe', chrome_options=option)

driver.get('https://www.ruidow.com/login')

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
w = 100
h = 40
region = im.crop((x, y, x+w, y+h))
region.save("screenshot1.png")

