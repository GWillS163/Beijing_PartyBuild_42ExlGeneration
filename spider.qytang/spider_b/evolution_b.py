from selenium import webdriver
import time
import json
from pykeyboard import *
from pymouse import *
M = PyMouse()
K = PyKeyboard()

def login_cisco_com(driver, username, passwd):
    # 无头游览器_ 注释掉driver.PhantomJS(executable_path='C:\\工具\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')

    # 2. 请求页面
    driver.get('https://space.bilibili.com/412127397/channel/detail?cid=73579')

    # # 3.交互操作 输入，点击
    # time.sleep(2)
    # driver.find_element_by_id('userInput').send_keys(username)
    # driver.find_element_by_id('login-button').click()
    # print('wait 5s')
    # time.sleep(5)
    # driver.find_element_by_id('password').send_keys(passwd + '\n')
    # driver.save_screenshot('already_login.png')
    # # print('页面源', driver.page_source)

    driver.find_element('row video-list clearfix')

    # 写入cookie
    cookie = driver.get_cookies()
    print('当前cookies:\n\t', cookie,)

    jsonCookies = json.dumps(cookie)
    print('json.dumps_cookies:\n\t', jsonCookies,)
    # with open('cisco_Cookie.json', 'w') as f:
    #     f.write(jsonCookies)
    return jsonCookies

def CCIE_choices(driver):
    time.sleep(5)
    driver.find_element_by_xpath('liExamSchedular').click()

if __name__ == '__main__':
    t = time.time()
    # 1. 创建浏览器对象
    driver = webdriver.Chrome()  # 有头浏览器

    listCookies = login_cisco_com(driver, '1426793517@qq.com', '01281738@loveWF\n')
    listCookies = json.loads(listCookies)
    # login_cisco_com(driver, '1426793517@qq.com', '01281738@loveWF\n')
    # with open('cisco_Cookie.json', 'r', encoding='utf-8') as f:
    #     listCookies = json.loads(f.read())

    cookie = [item["name"] + "=" + item["value"] for item in listCookies]
    cookie_str = '; '.join(item for item in cookie)
    print('整理后的cookie：\n\t', cookie_str)
    print('浏览共耗时：', round(time.time()-t, 3))



