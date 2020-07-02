import win32gui,time
from PIL import ImageGrab
import os
def Open_Vsphere():
    t1 = time.time()
    '系统调度'
    os.system('start VpxClient')
    print('\n\tstartAPP used time:\t', round(time.time()-t1, 3), end='\n')

def Open_VPN():
    t1 = time.time()
    '方案二，系统调度'
    os.system('start /MAX anyconnect')
    print('\n\tused time:\t', round(time.time()-t1, 3), end='\n')



title_name = 'Cisco AnyConnect Secure Mobility Client'
win = win32gui.FindWindow('#32770', title_name)
print("找到句柄：%x" % win)
def open_app():
    for i in range(1,3):
        if win != 0:
            left, top, right, bottom = win32gui.GetWindowRect(win)
            print(left, top, right, bottom)
            print(right - left, bottom - top)
            win32gui.SetForegroundWindow(win)
            break
            print('未break')
        else:
            print('重试',i)
            Open_VPN()
            print('请注意：找不到{}个人（或群），请激活窗口！'.format(title_name))


time.sleep(0.6)
bbox = win32gui.GetWindowRect(win)
img = ImageGrab.grab(bbox)

img.show()
img.save('img.BMP', 'BMP')
