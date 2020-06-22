import os
from PIL import Image
import datetime
import time
import random

def screen():
    t = time.time()
    os.system('adb shell screencap -p /sdcard/screen.png')
    os.system('adb pull sdcard/screen.png ./screen.png')
    print("图像上传完成"+ "耗时"+str(time.time()-t))

def getDistance():
    image = Image.open('screen.png')
    width = image.size[0]
    height = image.size[1]

    '''for i in range(124, 130):
        for j in range(205,215):
            if image.getpixel((i, j))[:3] == (255,219,115,):
                print(i,j)
                print("转圈一周")
    '''
def main():
    'for i in range(1,10):'
    i = 0
    while True:
        i += 1
        os.system('adb shell input swipe {} 1500 {} 255 {}'.format(random.randrange(480,600),
                                                                   random.randrange(490,620),
                                                                   random.randrange(100,700)))
        print("swipe {}~".format(i))
        #screen()
        t =time.time()
        time.sleep(random.randrange(4,26))
        print(time.time()-t)


main()