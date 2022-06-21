import threading
import time
import queue
import pymysql
import mysql
# 数据库连接池
from DBUtils.PooledDB import PooledDB
from client_sender import Interactive
import requests
# from gwills_tools.scrab_img_at_cl import get_web_link, find_url
# from gwills_tools.insert_my_mongodb import insert_to_database
from pprint import pprint

# 2020年8月27日, 19点28分
# 使用 queue 队列技术
# 本代码 已经修改- 主要有两个线程,一个监听listen,另一个后台不断检测并执行任务队列,
# listen到数据后不会处理,会扔给queue_lst并继续listen
# queue 会不断检测queue_lst,然后一点点按顺序处理
# 你可以自己修改.
# 本仓库主要用来备份自己的代码, 非必要不会做过多的 封装.
pool = PooledDB(
        creator=pymysql,  # 使用链接数据库的模块
        maxconnections=0,  # 连接池允许的最大连接数，0和None表示不限制连接数
        mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
        maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
        maxshared=3,
        # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
        blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
        maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
        host='127.0.0.1',
        port=3306,
        user='root',
        password='qweasd159753',
        database='excel',
        charset='utf8'
    )
def block_listen():  # 前台不断接收 值,返回给列表,后不间断监听
    global queue_lst
    while 1:
        result = s.listen()
        if result:
            # queue_lst = [result] + queue_lst
            q.put(result)
            print('已添加到消息处理队列--:')
            # if 'fromQQ' in result.keys():
            #     s.group_msg('爸爸你交给我的事情我记下了,还有'+str(q.qsize())+'个没给您发完', result['fromGroup'])


my_qq = 532268865
# 这里是检测是否与机器人相关, 未完成
def detect_about_me(result):
    if 'fromQQ' in result.keys():
        res_type = result.get('res_type')
        res_msg = result.get('msg')
        if res_type == 1:  # 如果type 为1 进行私发回复
            from_qq = int(result.get('fromQQ'))
            message = result.get('msg')
            from_group = result.get('fromGroup')
            print('提取about me 的消息:', res_msg)
            return True, res_msg
        if res_type == 2:
            if f"[@{my_qq}]" in res_msg:
                print('提取about me 的消息:', res_msg)
                return True, res_msg
            else:
                return None
        if res_type == 3:
            print('事件消息', res_msg)

# def back_queue():   # 后台消息处理队列  不断检测输入内容, 并执行相应程序
#     while 1:
#         queue_arg = q.get()
#         if queue_arg:
#             # 检测是否与bot 相关的消息
#             # if detect_about_me(queue_arg):
#             for i in range(1, 6):
#                 notice = "..." * i
#                 states = "操作中: "
#                 if i == 5:
#                     notice = '!!!' * i
#                     states = "操作成功"
#                 notice = f'{i:>2}/5|{queue_arg["msg"][:5]:<6}|{states}{notice:15}| 队列剩余:{q.qsize() * "#":<10}'
#                 print(notice)
#                 s.private_msg(notice, from_qq=532268865)
#                 time.sleep(0.9)
#             print('====本条数据处理完毕=====')

def back_queue():   # 后台消息处理队列  不断检测输入内容, 并执行相应程序
    while 1:
        queue_arg = q.get()
        if "fromQQ" in queue_arg.keys():
            print(pprint(queue_arg))
            msg=queue_arg["msg"]
            # 设置 搜索资料的指令
            if msg[0:1]=='搜':
                msg=msg.split()
                # 分割后 根据list长度选择调用那个数据库搜索函数
                legth=len(msg)
                if legth==2:
                    result = mysql.Search1(msg[1])
                    jud_i=result[0]
                    num=result[1]
                    r_all=result[2]
                    judgement(jud_i,queue_arg,r_all,num)
                elif legth==3:
                    result = mysql.Search2(msg[1],msg[2])
                    jud_i = result[0]
                    num = result[1]
                    r_all = result[2]
                    judgement(jud_i, queue_arg, r_all, num)
                elif legth==4:
                    result = mysql.Search3(msg[1], msg[2],msg[3])
                    jud_i = result[0]
                    num = result[1]
                    r_all = result[2]
                    judgement(jud_i, queue_arg, r_all, num)
                else:
                    continue
            elif msg == "毒鸡汤":
                msg = chick_soup()
                s.group_msg(msg, queue_arg["fromGroup"])
            elif msg == '卖家秀':
                msg = seller_show()
                s.send_group_pic_text(msg, queue_arg["fromGroup"],0)
            else:
                continue
        print('====本条数据处理完毕=====')

def multi_process():
    while True:
        global s, threads, queue_lst, q
        threads = []
        queue_lst = []
        q = queue.Queue()
        try:
            print('尝试建立连接')
            # s = Interactive("127.0.0.1", 8404, 430139105)
            s = Interactive("172.16.66.170", 8404, 2154024779)
            print('###进入监听发送模式,Ctrl+C退出:')
            front_func = threading.Thread(target=block_listen)  # 前台函数
            back_func = threading.Thread(target=back_queue)  # 后台任务处理队列
            threads.append(front_func)
            threads.append(back_func)
            back_func.start()
            front_func.start()
            for i in threads:
                i.join()
        except ConnectionResetError:
            print('连接中断!3s retry')
            time.sleep(3)
            break
        print('='*20)
#
# # 判断数据库中是否存在词条
# # jud_i表示数据库查询个数除10 向上取整
# # r_all表示数据库的搜索结果
# # num 数据库查询条数
# def judgement(jud_i,queue_arg,r_all,num):
#     if jud_i == 0:
#         str = '资料库条没有你的搜索字段，请尝试更换'
#         s.group_msg(str, queue_arg["fromGroup"])
#     elif jud_i==1:
#         str=''
#         for i in range(0, num):
#             str=str+r_all[i][0]+'\n'+r_all[i][1]+'\n'
#         s.group_msg(str, queue_arg["fromGroup"])
#     else:
#         for i in range(0,jud_i):
#             if i==0:
#                 str = ''
#                 for j in range(0, 10):
#                     str = str + r_all[j][0] + '\n' + r_all[j][1] + '\n'
#                 s.group_msg(str, queue_arg["fromGroup"])
#                 continue
#             elif i==jud_i-1:
#                 str = ''
#                 limit=num-(jud_i-1)*10
#                 for j in range(0,limit):
#                     str = str + r_all[i * 10+j:i * 10 + j+1][0][0] + '\n' + r_all[i * 10+j:i * 10 + j+1][0][1] + '\n'
#                 time.sleep(1)
#                 # s.send_group_temporary_msg(str, queue_arg["fromGroup"], queue_arg["fromQQ"])
#                 s.private_msg(str, queue_arg["fromQQ"])
#                 continue
#             else:
#                 if num >50:
#                     s.private_msg('您的词条较多，请增加关键词！！', queue_arg["fromQQ"])
#                     break
#                 str = ''
#                 for j in range(0, 10):
#                     str = str + r_all[i*10+j:i*10+j+1][0][0] + '\n' + r_all[i*10+j:i*10+j+1][0][1] + '\n'
#                 time.sleep(0.5)
#                 # s.send_group_temporary_msg(str, queue_arg["fromGroup"], queue_arg["fromQQ"])
#                 s.private_msg(str,queue_arg["fromQQ"])
#                 continue

# 毒鸡汤
def chick_soup():
    url = 'http://api.lkblog.net/ws/api.php'
    r = requests.get(url)
    dic=r.json()
    msg=dic["data"]
    return msg
# 卖家秀
def seller_show():
    netpic='https://api.66mz8.com/api/rand.tbimg.php?format=png'
    msg="[netpic:"+netpic+"]"
    return msg
if __name__ == '__main__':

    # 多线程监听程序, multi_process 调度内调度前台和后台程序.
    multi_process()


