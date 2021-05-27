import threading
import queue
import time

# 前台输出状态表
status_1 = ['Loading.', 'Loading..', 'Loading...', '1/5', '2/5', '3/5', '4/5', 'Completed!', 'shutdown']
status_2 = ['-', '/', 'Linking', 'transfing', 'wwww', 'aaa', 'sss', 'Over', ]
output = {"Thread_1": '[loading]',
          "Thread_2": '-',
          }

def Thread_1():
    n = 0
    while n < 9:
        output["Thread_1"] = status_1[n]
        n += 1
        time.sleep(5)

def Thread_2():
    n = 0
    while n < 8:
        output["Thread_2"] = status_2[n]
        n += 1
        time.sleep(1.8)
# 后台两个任务启动
threading.Thread(target=Thread_1, daemon=True).start()
threading.Thread(target=Thread_2, daemon=True).start()


print(f'{"Thread":^10}|{"Status":^10}|{"Thread":^10}|{"Status":^10}')
while output["Thread_1"] != 'shutdown':
    print(f'{"Thread_1":^10}|{output["Thread_1"]:^10}|{"Thread_2":^10}|{output["Thread_2"]:^10}|',end='\r')
    # time.sleep(1)

