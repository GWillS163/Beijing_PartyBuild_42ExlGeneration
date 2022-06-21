import logging
from sigua_decry_core import *
from old.ftp_operate import MyFtp
import threading, queue
import time
from playsound import playsound

success_video_lst = []
folder_lst = []
ftp_send_queue = queue.Queue()
decry_queue = queue.Queue()
lock = threading.Lock()


def local_detect_fold():
    """备用本地检测 ['C:\\okfun\\3832', 'C:\\okfun\\4542', ]"""
    print('♦♦♦♦♦♦♦♦♦♦♦♦♦♦本地检测♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦')
    for video_num in os.listdir(local_path):
        video_num_dir = os.path.join(local_path, video_num)
        if os.path.isdir(video_num_dir) and re.match('^[0-9]+$', video_num):  # 是 数字名的目录 , 若BUG请留意正则
            folder_lst.append(video_num)

            data_notice[video_num] = {}
            data_notice[video_num].update({'file_lca': 'local'})  # 存入data
            data_notice[video_num]['ftp_download'] = '-'
            decry_queue.put(video_num)
    print('本地检测到的文件夹:', len(folder_lst), folder_lst)

def remote_detect_fold():
    global data_notice
    # print('♦♦♦♦♦♦♦♦♦♦♦♦♦♦开启下载♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦')
    # playsound("D:\python_scripts\merge_m3u8\source\RA-ready.mp3")
    okfun_video_lst = my_ftp.detect_okfun(start_path)
    print('发现远端目录:', okfun_video_lst)
    for video_num in okfun_video_lst:
        # lock.acquire()
        data_notice.update({video_num: {}})
        data_notice[video_num].update({'file_lca': 'remote'}) # 存入data
        # lock.release()


# FTP 传输
def ftp_link(ip_list):
    while True:
        for ip in ip_list:
            my_ftp = MyFtp(ip, port)
            print('连接:', ip, end='')
            # while True:
            if my_ftp.ftp_login(username, password) == 1000:
                logging.warning('login success , now waiting queue task')
                print('ftp链接成功')
                return ip, my_ftp
            else:
                pass


# 后台发送  三级 流水线队列
def ftp_upload(video_num, com_file_path, remote_path):
    lock.acquire()
    data_notice[video_num].update({'back_ftp_send': 'Sending'})
    lock.release()
    try:
        my_ftp.uploadFile(com_file_path, os.path.join(remote_path, video_num))  # 上传成品至手机
        lock.acquire()
        data_notice[video_num].update({'back_ftp_send': 'Sended'})
        lock.release()
    except Exception as E:
        lock.acquire()
        data_notice[video_num].update({'back_ftp_send': str(E)})
        lock.release()
    ftp_send_queue.task_done()



# Use decry 二级 流水线队列
def back_decry(video_num):
    print('back_decry living~', video_num)
    if video_num in success_video_lst:
        print('为什么又执行了一次', video_num)
        return
    lock.acquire()
    data_notice[video_num].update({'decry_finally': 'processing'})
    lock.release()
    decryed_video, decry_printout = decry(os.path.join(local_path, video_num),
                                          mode='general')  # a uto_delete preserve general
    # 应只存部分执行的返回结果
    lock.acquire()
    data_notice[decryed_video].update({"decry_finally": decry_printout["decry_finally"]})  # 存入 data_notice
    data_notice[decryed_video].update({"completed": decry_printout["completed"]})  # 存入 data_notice
    decry_queue.task_done()

    if decry_printout['completed']:  # 解密后 成功  存入success lst & queue
        success_video_lst.append(decryed_video)  # 放入成功列表
        data_notice[video_num]['decry_finally'] = 'Success'
        return decry_printout['completed']
    else:
        data_notice[video_num]['decry_finally'] = 'Failed'
        return
# 下行 文件
def ftp_download(video_num):
    global data_notice
    # lock.acquire()
    data_notice.update({video_num: {}})
    data_notice[video_num].update({'file_lca': 'remote'})
    # lock.release()

    data_notice[video_num]['ftp_download'] = 'Starting'
    try:
        down_step = my_ftp.DownLoadFileTree_okfun(start_path, video_num, local_path, verbose=False)  # 下载到本地
        file_lst = my_ftp.ftp_client.nlst(os.path.join(start_path, video_num))
        for file in file_lst:
            rate_precent = next(down_step)
            lock.acquire()
            data_notice[video_num]['ftp_download'] = rate_precent
            lock.release()

        lock.acquire()  # 公共单元写数据
        data_notice[video_num]['ftp_download'] = 'Over'
        decry_queue.put(video_num)
        lock.release()
        return video_num
    except Exception as E:  # 下载出问题就跳过
        data_notice[video_num]['ftp_download'] = str(E)
        return

# 后续 删除处理
def remove_all_oringa():
    playsound("D:\python_scripts\merge_m3u8\source\MC-hurt.mp3")
    # input('移除远程 确认:>>continue:')
    print('移除远程/ 本地success. 目录 / 本地成品 ')
    print('清空 远程目录:', start_path)
    my_ftp.ftp_client.cwd(remote_path)
    print('移除', success_video_lst)
    for succ_dir in success_video_lst:
        my_ftp.ftp_client.rmd(succ_dir)
    # my_ftp.ftp_client.cwd("..")
    # my_ftp.ftp_client.rmd(start_path)
    # my_ftp.ftp_client.mkd(start_path)
    for video in data_notice:
        vdo_completed_path = data_notice[video]['completed']
        if vdo_completed_path != "":
            try:
                print('正在移除:', vdo_completed_path)
                os.remove(vdo_completed_path)
                data_notice[video]['completed_del'] = "deleted"
            except FileNotFoundError:
                data_notice[video]['completed_del'] = "empty"
                pass

    # print('正在移除success目录')
    try:
        shutil.rmtree(os.path.join(local_path, "okfun_success"))
        os.removedirs(os.path.join(local_path, "okfun_failed"))
    except OSError:
        pass
    print('传输完成')
    playsound("D:\python_scripts\merge_m3u8\source\MC-hurt.mp3")


def print_notice_all():
    print_out = f""
    print(data_notice)
    for video_name in data_notice:
        print_out += f"{video_name:^6} |"  # 列
        for key in data_notice[video_name]:  # 行
            print_out += f"{data_notice[video_name][key]:^10}|"

        print_out += f"\n"
    print(f'{"vdonum":^6} |{"file_lca":^10}|{"ftp_down":^10}|{"decry_fin":^10}|{"com_location":^25}|{"ftp_send":^10}|{"remove":^10}')
    print(print_out)
    print('■' * 40)

def pure(video_num):
    # 获取列表
    local_file_lst = local_detect_fold()
    okfun_video_lst = remote_detect_fold()
    print_notice_all()  # 展示所有文件
    ip, my_ftp = ftp_link(ip_list)

    # 分发 线程


    if data_notice[video_num]['file_lca'] != 'local':
        # 下载
        video_num = ftp_download(video_num)
    # 解密
    com_file_path = back_decry(os.path.join(local_path, video_num))
    # 上传
    if com_file_path:
        ftp_upload(video_num, com_file_path, remote_path)

if __name__ == '__main__':
    local_path = 'C:\\okfun\\'
    start_path = "/okfun/v/"
    remote_path = "/okfun/"  # '/AAmydoc/.native/robot/'
    ip_list = ['192.168.1.124', '192.168.3.107', '192.168.3.102', '192.168.1.13', ]
    port = 6666
    username = 'root'
    password = 'admin'
    data_notice = {}

    # multi_front_printout = f"{'video_num'}"
    host_ip, my_ftp = ftp_link(ip_list)

    local_detect_fold()
    t1 = threading.Thread(target=ftp_download, daemon=True)  # 开启 后台 下载
    t1.start()
    # time.sleep(10)
    # t1.join()
    # t2 = threading.Thread(target=back_decry, daemon=True)  # 开启 后台解密
    # t3 = threading.Thread(target=back_ftp_send, daemon=True)  # 开启 后台发送
    # t2.start()
    # t3.start()
    # t2.join()
    # t3.join()
    while ftp_send_queue.qsize() == 0 and success_video_lst != 0:
        print('decry_queue.qsize():', decry_queue.qsize())
        print('ftp_send_queue.qsize():', ftp_send_queue.qsize())
        print("success_video_lst", success_video_lst)
        print_notice_all()
        time.sleep(1)
    print(f'len(success_video_lst):{len(success_video_lst)}  len(data_notice){len(data_notice)}')
    print("success_video_lst", success_video_lst)
    print("data_notice", data_notice)
    print_notice_all()

    ftp_send_queue.join()  # 前后台 完成后 取消阻塞
    decry_queue.join()  #
    input('回车结束')
    print('*main FTP正在发送:')
    time.sleep(5)

    # 完成 后检测文件发送完成后进行删除
    remove_all_oringa()
    print('\n执行报告:')
    print_notice_all()
    # print(f'{"文件名":^5}|{"本地状态":^7}|{"分片数":^18}|{"解密状态":^5}|{"发送状态":5}|{"本地缓存":^6}|{"完成状态":^8}')
    # for i in data_notice:
    #     print(f"{i:^5}{data_notice[i]['air']:^7} {data_notice[i]['slip']:^18} {data_notice[i]['slip_decry']:^5} "
    #           f"{data_notice[i]['original']:^5} {data_notice[i]['completed']:^5} {data_notice[i]['decry_com']:^5} "
    #           f"{data_notice[i]['temporary']:^5} {data_notice[i]['completed_del']:^5} {data_notice[i]['decry_temp']:^5} "
    #           f"{data_notice[i]['finally']:^5} ")

    print(f'{60}s waiting ---')
    time.sleep(60)

"""
"completed_del": "",  # 成品删除   #

文件名   | 本地状态  |   分片数    |                解密状态                      | 发送状态  | 本地缓存         | 完成状态
[16118]  [ 下载成功]     17[正常]  [解密Over]C:\okfun\\16118_over.ts               [发送成功] [本地缓存-删除]      ■■
[5277]    [ 下载成功]     合规文件0                   ----                             --         --              ■■
"""
