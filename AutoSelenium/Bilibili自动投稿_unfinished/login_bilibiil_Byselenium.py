from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException
import time
import base64
from PIL import Image
from io import BytesIO
import random


class Binance(object):
    def __init__(self):
        options = webdriver.ChromeOptions()
        # 设置为开发者模式
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.driver = webdriver.Chrome(options=options)
        self.USERNAME = '1274667113@qq.com'
        self.PASSWARD = '69412981'

    def get_login_btn(self):
        # 打开网址
        self.driver.get("https://passport.bilibili.com/login")
        username = WebDriverWait(self.driver, 10, 0.5).until(EC.presence_of_element_located((By.ID, 'login-username')))
        username.clear()
        username.send_keys(self.USERNAME)
        time.sleep(2)
        pwd = WebDriverWait(self.driver, 10, 0.5).until(EC.presence_of_element_located((By.ID, 'login-passwd')))
        pwd.clear()
        pwd.send_keys(self.PASSWARD)
        time.sleep(2)

        # 点击登录，弹出滑块验证码
        login_btn = WebDriverWait(self.driver, 10, 0.5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@class="btn-box"]//a[@class="btn btn-login"]')))
        login_btn.click()
        WebDriverWait(self.driver, 10, 0.5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'geetest_slider_button')))

    def get_geetest_image(self):
        """
        获取验证码图片
        :return: 图片对象
        """
        # 执行 JS 代码并拿到完整图 base64 数据
        JS = 'return document.getElementsByClassName("geetest_canvas_fullbg")[0].toDataURL("image/png");'
        im_info = self.driver.execute_script(JS)
        # print(im_info)
        # 拿到base64编码的图片信息
        im_base64 = im_info.split(',')[1]
        # 转为bytes类型
        image1 = base64.b64decode(im_base64)
        # 加载图片
        image1 = Image.open(BytesIO(image1))
        # 保存图片
        image1.save('image1.png')

        # 执行 JS 代码并拿到只带阴影图 base64 数据
        JS = 'return document.getElementsByClassName("geetest_canvas_bg")[0].toDataURL("image/png");'
        im_info = self.driver.execute_script(JS)
        # print(im_info)
        # 拿到base64编码的图片信息
        im_base64 = im_info.split(',')[1]
        # 转为bytes类型
        image2 = base64.b64decode(im_base64)
        # 加载图片
        image2 = Image.open(BytesIO(image2))
        # 保存图片
        image2.save('image2.png')

        return image1, image2

    def is_pixel_equal(self, image1, image2, x, y):
        """
        判断两张图片 各个位置的像素是否相同
        :param image1:不带缺口的图片
        :param image2: 带缺口的图片
        :param x: 位置x
        :param y: 位置y
        :return: (x,y)位置的像素是否相同
        """
        # 获取两张图片指定位置的像素点
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        # 设置一个阈值 允许有误差
        threshold = 10
        # 彩色图 每个位置的像素点有三个通道
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
                pixel1[2] - pixel2[2]) < threshold:
            return True
        return False

    def get_gap(self, image1, image2):
        """
        获取缺口偏移量
        :param image1:不带缺口的图片
        :param image2: 带缺口的图片
        :return:
        """
        left = 60  # 定义一个左边的起点 缺口一般离图片左侧有一定的距离 有一个滑块
        for i in range(60, image1.size[0]):  # 从左到右 x方向
            for j in range(image1.size[1]):  # 从上到下 y方向
                if not self.is_pixel_equal(image1, image2, i, j):
                    left = i  # 找到缺口的左侧边界 在x方向上的位置
                    return left
        return left

    def login_successfully(self):
        """
        判断是否登陆成功
        :return:
        """
        try:
            # 登录成功后 界面上会有一个消息按钮
            return bool(
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[text()="消息"]')))
            )
        except TimeoutException:
            print('超时了!!!')
            return False

    def analog_drag(self):
        # 刷新一下验证图片
        element = self.driver.find_element_by_xpath('//a[@class="geetest_refresh_1"]')
        element.click()
        time.sleep(1)
        # 保存两张图片
        full_image, cut_image = self.get_geetest_image()
        # 根据两个图片计算距离
        distance = self.get_gap(cut_image, full_image)
        # 开始移动
        self.start_move(distance)
        # 判断是否验证成功
        if self.login_successfully():
            print("登录成功")
        else:
            print('正在重试.....')
            self.run()

    def start_move(self, distance):
        element = self.driver.find_element_by_xpath('//div[@class="geetest_slider_button"]')
        # 这里就是根据移动进行调试，计算出来的位置不是百分百正确的，加上一点偏移
        distance -= element.size.get('width') / 2
        distance += 25
        print('缺口位置:' + str(distance))
        # 按下鼠标左键
        ActionChains(self.driver).click_and_hold(element).perform()
        time.sleep(0.5)
        while distance > 0:
            if distance > 10:
                # 如果距离大于10，就让他移动快一点
                span = random.randint(5, 8)
            else:
                # 快到缺口了，就移动慢一点
                span = random.randint(2, 3)
            ActionChains(self.driver).move_by_offset(span, 0).perform()
            distance -= span
            print(f'本次滑动距离:{str(span)}  还剩:{str(distance)}')
            time.sleep(random.randint(10, 50) / 100)

        # 往回滑点
        ActionChains(self.driver).move_by_offset(distance, 1).perform()
        ActionChains(self.driver).release(on_element=element).perform()

    def run(self):
        # 登陆弹出验证码
        self.get_login_btn()
        # 点击滑块并滑动
        self.analog_drag()


if __name__ == '__main__':
    ok = Binance()
    ok.run()