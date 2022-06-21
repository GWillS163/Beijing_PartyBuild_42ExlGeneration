#from Open_VPN import *
from pykeyboard import *
import time
import os
k = PyKeyboard()


#切换到前端后，暂停tim秒
def alt_tab(tim):
    # 切换到上一个任务 前端
    k.press_key(k.alt_key)
    #k.press_key(k.shift_key)
    k.tap_key(k.tab_key)
    #k.release_key(k.shift_key)
    k.release_key(k.alt_key)
    time.sleep(float(tim))

#输入usrnam，tab
def input_usrnam(usrnam): #
    print('\t###正 在 输 入 Usrnam\t###')
    k.type_string(usrnam, 0.02)
    time.sleep(0.1)
    k.tap_key(k.tab_key)

#输入密码，回车
def input_passwd(passwd): #
    print('\t###正 在 输 入 Passwd\t###')
    k.type_string(passwd, 0.02)
    time.sleep(0.2)
    k.tap_key(k.enter_key)

#打开VPN软件
def Open_VPN():
    t1= time.time()
    # '方案一，模拟人工 win搜索打开'
    # #win
    # k.tap_key(k.windows_l_key)
    # # vpn
    # time.sleep(0.05)
    # k.type_string('VPN',0.05)
    # #enter
    # time.sleep(0.2)
    # k.tap_key(k.enter_key)
    # time.sleep(1.5)
    '方案二，系统调度'
    os.system('start /MAX anyconnect')
    print('\n\tused time:\t',round(time.time()-t1,3),end='\n')

#回车连接， 等待1.5s弹出新窗口， input_passwd()， 然后循环调用alt_tab()和input_passwd。
def link_VPN(passwd):
    print('\t应该已启动\tConnect！')
    k.tap_key(k.enter_key)
    # wait__to input
    print('\t###静候3s，等待输入框\t###')
    time.sleep(3)
    input_passwd(passwd)
    print('\t### 流 程 结 束 \t###')
    print('\t按Ctrl + CC 或等待5s自动退出')

def reinput_VPN(passwd):
    # 再次尝试输入:
    while True:
        if input('\n\n是否需要再次输入<Enter确认/Ctrl + CC退出>') == '':
            alt_tab(0.3)
            input_passwd(passwd)

def run_linkVPN(timeout,frequency=1):
    if os.system('ping -w {} -n {} 172.16.66.166'.format(timeout,frequency)) == 0:
        print('\n\n已连接至内网',end='')
    else:
        passwd = '7Vr.K0s5'
        Open_VPN()
        time.sleep(2.7)
        # sleep_wait start
        link_VPN(passwd)


#打开Vsphere
def Open_Vsphere():
    t1= time.time()
    '系统调度'
    os.system('start VpxClient')
    print('\n\tstartAPP used time:\t',round(time.time()-t1,3),end='\n')

# 回车连接， 等待1.5s弹出新窗口， input_passwd()， 然后循环调用alt_tab()和input_passwd。
def link_Vsphere(username, passwd):
# usrnam
    input_usrnam(username)
# passwd
    input_passwd(passwd)

def Open_rsecTeacher():
    os.system('start GoogleChrome 172.16.66.166')  # mengjq _ rsec

def Open_nbteacher():
    os.system('start MicrosoftEdge 172.16.66.166')  # nb_mengjq

import sys, time, msvcrt


def readInput(caption, default, timeout=5):
    start_time = time.time()
    sys.stdout.write('%s(%d秒自动跳过):' % (caption, timeout))
    sys.stdout.flush()
    input = ''
    while True:
        ini = msvcrt.kbhit()
        try:
            if ini:
                chr = msvcrt.getche()
                if ord(chr) == 13:  # enter_key
                    break
                elif ord(chr) >= 32:
                    input += chr.decode()
        except Exception as e:
            pass
        if len(input) == 0 and time.time() - start_time > timeout:
            break
    print('')  # needed to move to next line
    if len(input) > 0:
        return input + ''
    else:
        return default


# 使用方法


if __name__ == '__main__':
#测试网络,
    run_linkVPN(200)
#开始选择
    print('\t\tCtrl+C,Enter默认选择vSphere')
    try:
        senntaku = input('0.默认打开vSphere,\n1.打开Chrome_Teacher,\n2.打开Edge_student\t')
        if senntaku == '' or '0' or '1' or '2':
            print('')
        else:
            print("啥也不是,reInput!")
    except KeyboardInterrupt:
        senntaku = ''
        print('用户中断,默认选择')

# 进入判断
    if senntaku == '':
        print('默认选择')
        Open_Vsphere()
        time.sleep(2)
        print('\t###静候1.5s，等待输入框\t###')
        # alt_tab(1.5)
        link_Vsphere('mengjq', '7Vr.K0s5')
    elif senntaku == '1':
        Open_rsecTeacher()
    elif senntaku == '2':
        Open_nbteacher()
    else:
        print("啥也不是,reInput!")
    time.sleep(4)
#退出
    print('\t按Ctrl + CC 或等待10s自动退出')
    time.sleep(10)

# if __name__ == '__main__':
#     if test_net(200) == 0:
#         print('\n\n已连接至内网',end='')
#     else:
#         #senntaku = '0'
#         run_linkVPN()
# #开始计时
#
#     #print('\t\t五秒超时,Ctrl+C,Enter默认选择vSphere')
#     try:
#         iscaiji = readInput('请输入你的名字', 'aaa')
#         senntaku = input('0.默认打开vSphere,\n1.打开Chrome_安全mengjq,\n2.打开Edge_nb_teacher\t')
#     except KeyboardInterrupt:
#         senntaku = ''
#         print('用户中断,默认选择')
#
#     if senntaku == '':
#         print('默认选择')
#         Open_Vsphere()
#         time.sleep(2)
#         print('\t###静候1.5s，等待输入框\t###')
#         # alt_tab(1.5)
#         link_Vsphere('mengjq', '7Vr.K0s5')
#     elif senntaku == '1':
#         Open_rsecTeacher()
#     elif senntaku == '2':
#         Open_nbteacher()
#     else:
#         print("啥也不是,reInput!")
#     time.sleep(4)
# #超时就是默认执行
#     print('\t按Ctrl + CC 或等待10s自动退出')
#     time.sleep(10)