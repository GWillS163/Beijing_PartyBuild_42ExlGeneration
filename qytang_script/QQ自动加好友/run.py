import time, os, re
from pymouse import *                   # 模拟鼠标所使用的包
from pykeyboard import *                # 模拟键盘所使用的包
import random
M = PyMouse()
K = PyKeyboard()
import win32clipboard as w
import win32con
import pyperclip

# --------批量发送QQ消息----------
# 获取QQ号list
def get_txt_text(path):
    global qqlst
    bdcam_pic = '.*.txt'   # 定义正则匹配式
    print('-<<[查找文件]>>--\t\t', end='')
    for i in os.listdir(path):           # 遍历一遍
        if re.match(bdcam_pic, i):        # 找到符合正则的文件
            print(i)                      # 打印文件名

            with open(i, 'r') as f:
                print('-<<[文件内容]>>--\t\t')
                for i in f.readlines():
                    print(i, end='  ')
                    qqlst.append(i)



def run_qq():
    os.system('"C:\Program Files (x86)\Tencent\QQ\Bin\QQScLauncher.exe"')
    time.sleep(4)                           # 等待QQ启动登陆成功
    # 添加好友1：等待登录
def open_qq_panel():
    M.move(1510, 1)
    time.sleep(1)
    # 2. 打开添加窗口，
    time.sleep(1)

def search_contact(qqNum, refiy_Msg, add1_win2):
    # 3. 点击【搜索框】，输入QQ号
    M.click(1456, 140)
    M.click(1456, 140)
    time.sleep(2)
    K.type_string(str(qqNum).strip('\n'), 0.06)
    print('准备打开添加')
    # time.sleep(2)# 点击添加好友按钮
    # M.move(1652, 266)
    # time.sleep(2)
    # M.click(1652, 266)
    time.sleep(1)
    K.tap_key(38)  # 面板选择
    K.tap_key(38)
    time.sleep(0.5)
    K.tap_key(38)
    time.sleep(1)
    K.tap_key(K.enter_key)
    print('添加暂停')
    time.sleep(3)
    if add1_win2 == 1:
        #  ___________无共同群， 发送好友验证消息____________________
        M.click(835, 412)  # 点击输入框
        input_Msg(str(refiy_Msg), round(random.random(), 2))  # 输入文本
        time.sleep(round(random.random(),2)*10)
        M.click(947, 658)  # 下一步
        M.click(947, 658)  #
        M.click(1028, 656)  # 完成
    elif add1_win2 == 2:
        #  ___________有共同群，打开临时会话窗口_____________
        M.click(810, 772)  # 点击输入框
        input_Msg(str(refiy_Msg))  # 输入文本
        time.sleep(round(random.random(),2)*10)
        K.tap_key(K.enter_key)
    print('发送消息完毕\n')

def input_Msg(refiy_Msg):
    print(refiy_Msg)
    time.sleep(round(random.random(),2)*10)
    # 以下语句模拟键盘点击ctrl+v
    K.press_key(K.control_key)
    K.tap_key('v')
    K.release_key(K.control_key)

qqlst = []
if __name__ == '__main__':
    # run_qq()
    # lst = ['2154024779', '605658506', '809526307', '1274667113']
    get_txt_text('.\\')
    n = 0
    for i in qqlst:  # 遍历QQ号，执行添加好友
        n = n + 1
        print(n, end='\t')
        print(i, end='    ')
        open_qq_panel()
        search_contact(i, '我这里有一些学习资料，您需要的', add1_win2=1)
# 'Im BOT_USER that is python auto add contact'
