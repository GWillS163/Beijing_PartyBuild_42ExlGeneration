from selenium import webdriver
import time
import json
import re
from pykeyboard import *
from pymouse import *
M = PyMouse()
K = PyKeyboard()

def opera():
    driver = webdriver.Chrome()  # 有头浏览器
    # 2. 请求页面
    driver.get('https://space.bilibili.com/412127397/channel/detail?cid=71323')
    # driver.get('https://ccie.cloudapps.cisco.com/CCIE/Schedule_Lab/CCIEOnline/CCIEOnline')

    res = driver.page_source
    print(res)

if __name__ == '__main__':
    opera()




