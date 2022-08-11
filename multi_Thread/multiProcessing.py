#  Author : Github: @GWillS163
#  Time: $(Date)
import time
from multiprocessing import Process


class MyProcess(Process):  # 继承Process类
    def __init__(self, name):
        super(MyProcess, self).__init__()
        self.name = name
    # add the decoration to private the function
    @staticmethod
    @classmethod
    def run(name):
        # print slash mark loading animation
        for i in range(10):
            print('\r{} {}'.format(self.name, '#' * (i + 1))
                  , end='\n')
            time.sleep(0.1)


if __name__ == '__main__':
    process_list = []
    for i in range(5):  # 开启5个子进程执行fun1函数
        p = MyProcess('Python' + str(i))  # 实例化进程对象
        # p.start()
        p.run()
        process_list.append(p)

    for p in process_list:
        p.join()

    print('结束测试')
