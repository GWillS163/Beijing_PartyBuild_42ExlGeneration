from login_bilibiil_Byselenium import Binance
from selenium import webdriver
import time

if __name__ == '__main__':
    driver = Binance()
    driver.run()
    # 创建浏览器对象
    # driver = webdriver.Chrome()
    # driver.PhantomJS(executable_path='C:\\工具\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')

    # 1.点击到投稿页

    # 2.请求页面
    # driver.get('https://www.cisco.com')
    driver.get('https://member.bilibili.com/v2#/upload/video/frame')

    # 3.交互操作 输入，点击
    driver.find_element_by_id('bili-upload-btn').click()
    time.sleep(3)
    driver.save_screenshot('already_login.png')
    print('页面源', driver.page_source)
    print('当前cookies', driver.get_cookies())
    print('当前url:', driver.current_url)
    driver.close()  # 关闭标签页
    driver.quit()  # 关闭浏览器