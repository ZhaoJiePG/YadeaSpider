# Author:Aliex ZJ
#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from selenium import  webdriver
import time
from selenium.webdriver.common.by import  By
from selenium.webdriver import ActionChains

# 防止机器识别
option = webdriver.ChromeOptions()
option.add_argument('--proxy--server=127.0.0.1:8080')
# 防止机器识别
option.add_experimental_option('excludeSwitches', ['enable-automation'])
# option.add_argument('headless')

# 要换成适应自己操作系统的chromedriver
browser = webdriver.Chrome(
    executable_path='D:\Maven\YadeaSpider\chromedriver.exe',
    chrome_options=option
)
url = "https://login.taobao.com/member/login.jhtml"

browser.get(url)
href = browser.find_element_by_class_name("J_Quick2Static")
print(href)
href.click()
time.sleep(3)
#sreach_window = browser.current_window_handle  #获取当前页面
browser.maximize_window()#页面最大化

#输入账号密码跳转
number = browser.find_element(By.ID, 'TPL_username_1')#账号输入框
password  = browser.find_element(By.ID, 'TPL_password_1')#密码输入框
button = browser.find_element(By.ID,'J_SubmitStatic')
number.send_keys("1390577786@qq.com")
password.send_keys("1")
button.click()
# 刷新本页
browser.execute_script("location.reload()")


#获取滑块的大小
span_background = browser.find_element_by_css_selector("#nc_1__scale_text > span")
span_background_size = span_background.size
print(span_background_size)

# 获取滑块的位置
button = browser.find_element_by_css_selector("#nc_1_n1z")
button_location = button.location
print(button_location)

# 拖动操作：drag_and_drop_by_offset
# 将滑块的位置由初始位置，右移一个滑动条长度（即为x坐标在滑块位置基础上，加上滑动条的长度，y坐标保持滑块的坐标位置）
x_location = button_location["x"] + span_background_size["width"]
y_location = button_location["y"]
ActionChains(browser).drag_and_drop_by_offset(button, x_location, y_location).perform()


#再次跳转
button = browser.find_element(By.ID,'J_SubmitStatic')
password.send_keys("zj654321!")
button.click()
#browser.close()
