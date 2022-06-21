import time
import sys
import os
import re
import queue
q = queue.Queue()

sys.path.append(os.path.abspath("SO_site-packages"))
import pyperclip  # 引入模块

recent_value = ""
tmp_value = ""  # 初始化（应该也可以没有这一行，感觉意义不大。但是对recent_value的初始化是必须的）
from spider_pronunciation import phonetic_spelling, iciban
from get_multithreading_value import MyThread

def multithread_requests(words):
    t1 = MyThread(iciban,  (words[0],))
    t2 = MyThread(iciban,  (words[1],))
    t3 = MyThread(iciban, (words[2]),)
    t4 = MyThread(iciban,  (words[3],))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    result = t1.get_result()+t2.get_result()+t3.get_result()+t4.get_result()
    return result

print('开始监控剪贴板, 请复制如一下形式的文本Pieces Clothes Watches Voices')
while True:  # 不间断监控剪贴板
    tmp_value = pyperclip.paste()  # 读取剪切板复制的内容
    ret_text = ''
    try:
        if tmp_value != recent_value:  # 如果检测到剪切板内容有改动，那么就进入文本的修改
            recent_value = tmp_value
            words = [i for i in recent_value.split(' ')] # 切割剪贴板
            if len(words) != 4:
                continue
            # 以下进行操作
            print('检测到异动:', words)
            # tmp_value = 'Pieces Clothes Watches Voices'
            # ret_text = multithread_requests(words) # iciban 正则有问题 暂时不用
            for word in words:
                print('正在访问:' + word)
                ret_text += '[' + phonetic_spelling(word) + ']'
            print('访问完毕:', ret_text)
            pyperclip.copy(ret_text)
        time.sleep(0.1)
    except KeyboardInterrupt:  # 如果有ctrl+c，那么就退出这个程序。  （不过好像并没有用。无伤大雅）
        break

    if tmp_value == 'getend':  # 如果复制的是getend，就退出程序。（这个主要是为了方便我在spyder中运行、退出的时候用的。）
        break
