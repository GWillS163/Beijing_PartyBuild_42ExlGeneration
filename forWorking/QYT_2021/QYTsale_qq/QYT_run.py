from QYTang_SalesQQ_dete import imgHistogram
from pykeyboard import *  # 模拟键盘所使用的包
import os, re, time

'''------------------------------------------------------'''  # 截图，并选中
def snap():
    k = PyKeyboard()
    k.tap_key(115)

# 图像比对 图片移动至log
def file_Rec():
    global path
    global previous_confidence
    bdcam_pic = 'bandicam.*.jpg'
    print('-<<[查找文件]>>--\t\t', end='')
    for i in os.listdir(path):
        if re.match(bdcam_pic, i):
            print(i)  # 打印文件名
            confidence = imgHistogram.Compare(path + benchmark, path + i)
            print('\t\t(pre_confid:', previous_confidence, ')')
            if confidence > 0.55:  # 如果达到阈值，发送
                if confidence != previous_confidence:
                    print('###confidence 一致 \t\t不发送')
                else:
                    # qytang_QQ_requests.message_API()
                    # qytang_QQ_requests.send_text(OCR.run_ocr(path,i))#调用API识别，并发送text至API,
                    print('testScripts\t发送成功')
            else:
                print('###confidence 未达阈值 \t不发送')
            previous_confidence = confidence  # 记录已匹配的阈值
            os.unlink(path + i)  # 移除文件

def run(tmi):
    for i in range(tmi):
        print('\n\n'+'-'*20+ str(i)+' /'+str(tmi))
        snap()
        time.sleep(0.3)
        file_Rec()
        time.sleep(5)


#设置一下基准benchamark文件 和path
path = 'C:\\Users\\admin\\Desktop\\'
benchmark = 'testScripts.jpg'
previous_confidence = 0

run()