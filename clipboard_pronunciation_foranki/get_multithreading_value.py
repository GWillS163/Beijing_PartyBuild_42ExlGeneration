# 「星火燎愿」原文链接：https: // blog.csdn.net / xpt211314 / article / details / 109543014
# -*- coding: utf-8 -*-
import threading, time

"""
用类包装线程；调用时可以获取线程的return返回值
"""


# 定义一个MyThread.py线程类
class MyThread(threading.Thread):
    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        time.sleep(2)
        self.result = self.func(*self.args)

    def get_result(self):
        threading.Thread.join(self)  # 等待线程执行完毕
        try:
            return self.result
        except Exception:
            return None


# 获取多线程return返回值的测试方法
def admin(number):
    uiu = number
    for i in range(10):
        uiu = uiu + i
    return uiu


if __name__ == "__main__":
    # 创建四个线程
    more_th1 = MyThread(admin, (5,))
    more_th2 = MyThread(admin, (10,))
    more_th3 = MyThread(admin, (50,))
    more_th4 = MyThread(admin, (78,))

    # 启动线程
    more_th1.start()
    more_th2.start()
    more_th3.start()
    more_th4.start()

    # 线程等待（即：等待四个线程都运行完毕，才会执行之后的代码）
    more_th1.join()
    more_th2.join()
    more_th3.join()
    more_th4.join()

    # 输出线程执行方法后的的返回值
    print(more_th1.get_result())
    print(more_th2.get_result())
    print(more_th3.get_result())
    print(more_th4.get_result())