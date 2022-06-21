# encoding=utf-8
import time
# 报错装饰器! 未封装完成

# 定义装饰器
def error_log_candy(func):
    def wrapper(*args, **kargs):
        while True:
            try:
                print('正在测试环境下运行，请关注报错提醒及报错文件')
                f = func(*args, **kargs)
                break
            except Exception as e:
                print('出现异常,将报错信息给我(error_log.txt):\n\t', e)
                #print('20s后重试')
                current_time = time.strftime("%Y-%m-%d_%H:%M:%S\t", time.localtime())
                with open('error_log.txt', 'w+') as f:
                    f.write(current_time)
                    f.write(str(e))
                    f.write('\n-------------\n\n\n')
                # time.sleep(20)
            print('exit after20s')
            time.sleep(20)
            break

        print('\n\n测试 任务结束无报错100s后退出')
        time.sleep(100)
        return f

    return wrapper

# 定义装饰器
def write2file(func):
    def wrapper(*args, **kargs):
        f_result = func(*args, **kargs)
        print('write_in', f_result)
        with open('error_log.txt', 'w+') as f:
            f.write(f_result)
        return f_result

    return wrapper




# @write2file
# def prin(n):
#     print('ha' * n)
#     return 'h' * n
#
# prin(3)
