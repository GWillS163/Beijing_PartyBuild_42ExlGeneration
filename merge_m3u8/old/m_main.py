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
            data_notice[video_num].update({'file_lca': 'local'})
            data_notice[video_num]['ftp_download'] = '-'
            # data_notice[video_num]['file'] += 'local '
            decry_queue.put(video_num)
    print('本地检测到的文件夹:', len(folder_lst), folder_lst)


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
def back_ftp_send():
    while t2_decry.is_alive() or ftp_send_queue.qsize():
        print('send_living-----')
        try:
            video_num_folder, video_com_file_path = ftp_send_queue.get()
            lock.acquire()
            data_notice[video_num_folder].update({'back_ftp_send': 'Sending'})
            lock.release()
            try:
                my_ftp.uploadFile(video_com_file_path, os.path.join(remote_path, video_com_file_path.split('\\')[-1]))  # 上传成品至手机
                lock.acquire()
                data_notice[video_num_folder].update({'back_ftp_send': 'Sended'})
                lock.release()
            except Exception as E:
                lock.acquire()
                data_notice[video_num_folder].update({'back_ftp_send': str(E)})
                lock.release()
            ftp_send_queue.task_done()

        except Exception as E:
            print('ftp 发送出错', E)
            raise
    print('send_dead----- t1_down.is_alive() or t2_decry.is_alive() or ftp_send_queue.qsize()',
          t1_down.is_alive(), t2_decry.is_alive(), ftp_send_queue.qsize())

# Use decry 二级 流水线队列
def back_decry():
    # time.sleep(10)
    n = 1
    while t1_down.is_alive() or decry_queue.qsize():
        print('decry 进入条件: t1_alive , decry:', t1_down.is_alive(), decry_queue.qsize())
        print(f'decry_living-----{n} times')
        video_nu = decry_queue.get()
        # if decry_queue.
        print('decry_get:', video_nu)
        if data_notice[video_nu]['file_lca'] == 'remote' and not 'ftp_download' in data_notice[video_nu].keys():
            decry_queue.put(video_nu)
            decry_queue.task_done()
            lock.acquire()
            data_notice[video_nu].update({'decry_finally': '为避免本地文件与远程文件冲突, 等待远程文件完全覆盖本地时再次解密'})
            lock.release()
            continue
        if video_nu in success_video_lst:
            print('本地远端同时有? 又执行了一次', video_nu)
            continue
        # if data_notice[video_num]['file_lca'] == 'local' or data_notice[video_num]['ftp_download'] == 'Over':
        lock.acquire()
        data_notice[video_nu].update({'decry_finally': 'decrying'})
        lock.release()
        decried_video, decry_printout = decry(os.path.join(local_path, video_nu), mode='general', verbose=True)  # a uto_delete preserve general
        print(decried_video, decry_printout)
        # 应只存部分执行的返回结果
        lock.acquire()
        # data_notice[decried_video].update({"decry_finally": decry_printout['decry_finally']})  # 存入 data_notice
        data_notice[decried_video].update({"completed": decry_printout["completed"]})  # 存入 data_notice
        lock.release()
        decry_queue.task_done()

        if decry_printout['completed']:  # 解密后 成功  存入success lst & queue
            success_video_lst.append(decried_video)  # 放入成功列表
            ftp_send_queue.put((video_nu, decry_printout['completed']))  # 文件地址存入发送 queue
            data_notice[video_nu]['decry_finally'] = 'Success'
            data_notice[video_nu].update({"decry_info": ''})
            # t3_up.start()
        else:
            data_notice[video_nu]['decry_finally'] = 'Failed'
            data_notice[video_nu].update({"decry_info": decry_printout["other"] + decry_printout["slip_decry"]})
        n += 1
    print('decry_dead :t1_down.is_alive() or decry_queue.qsize()', t1_down.is_alive(), decry_queue.qsize())


# 下行 文件
def ftp_download():
    global data_notice
    print('♦♦♦♦♦♦♦♦♦♦♦♦♦♦开启下载♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦')
    playsound("D:\python_scripts\merge_m3u8\source\RA-ready.mp3")
    okfun_video_lst = my_ftp.detect_okfun(start_path)
    print('发现远端目录:', okfun_video_lst)
    for video_num in okfun_video_lst:
        lock.acquire()
        if not video_num in data_notice.keys():
            data_notice.update({video_num: {}})
        data_notice[video_num].update({'file_lca': 'remote'})
        lock.release()
    for video_num in okfun_video_lst:
        data_notice[video_num]['ftp_download'] = 'Starting'
        try:  # 尝试下载一个目录
            # 下载视频分片
            down_step = my_ftp.DownLoadFileTree_okfun(start_path, video_num, local_path, verbose=False)  # 下载到本地
            file_lst = my_ftp.ftp_client.nlst(os.path.join(start_path, video_num))
            for file in file_lst:
                rate_precent = next(down_step)
                # print(rate_precent)
                lock.acquire()
                # if data_notice[video_num]['decry_finally'] == 'Success':
                #     data_notice[video_num]['ftp_download'] = rate_precent[0:7]
                #     lock.release()
                #     break
                data_notice[video_num]['ftp_download'] = rate_precent
                lock.release()

            # print('下载完成：', video_num)
            lock.acquire()  # 公共单元写数据
            data_notice[video_num]['ftp_download'] = 'Over'
            decry_queue.put(video_num)
            lock.release()
            # t2_decry.start()
        except Exception as E:  # 下载出问题就跳过
            data_notice[video_num]['ftp_download'] = str(E)

    # # 上传和下载使用同一个线程:
    # print('='*40, '开始上传')
    # while ftp_send_queue.qsize():
    #     print('send_living-----')
    #     try:
    #         video_num_folder, video_com_file_path = ftp_send_queue.get()
    #         lock.acquire()
    #         data_notice[video_num_folder].update({'back_ftp_send': 'Sending'})
    #         lock.release()
    #         try:
    #             my_ftp.uploadFile(video_com_file_path,
    #                               os.path.join(remote_path, video_com_file_path.split('\\')[-1]))  # 上传成品至手机
    #             lock.acquire()
    #             data_notice[video_num_folder].update({'back_ftp_send': 'Sended'})
    #             lock.release()
    #         except Exception as E:
    #             lock.acquire()
    #             data_notice[video_num_folder].update({'back_ftp_send': str(E)})
    #             lock.release()
    #         ftp_send_queue.task_done()
    #
    #     except Exception as E:
    #         print('ftp 发送出错', E)
    #         raise
    # print('send_dead----- t1_down.is_alive() or t2_decry.is_alive() or ftp_send_queue.qsize()',
    #       t1_down.is_alive(), t2_decry.is_alive(), ftp_send_queue.qsize())
    # print('发送结束')

# 后续 删除处理
def remove_all_oringa(remote, success_video, directory):
    playsound("D:\python_scripts\merge_m3u8\source\MC-hurt.mp3")
    print('移除远程/ 本地success. 目录 / 本地成品 :')

    success_file_lst = file_Rec(local_path, '[\s\S]*_over.ts')
    success_num_lst = [i.strip('_over.ts') for i in success_file_lst]

    if remote:
        print('清空 远程目录中成功的:', remote_path)
        my_ftp.ftp_client.cwd(start_path)
        # success_video_lst = os.listdir(os.path.join(local_path, "okfun_success"))  # 检测本地成功文件
        print('移除远程列表:', success_num_lst)
        for succ_dir in success_num_lst:
            if data_notice[succ_dir]['file_lca'] == 'remote':
                try:
                    my_ftp.ftp_client.rmd(succ_dir)  # 移除远程
                    data_notice[succ_dir].update({'remote': 'Deleted'})
                except Exception as E:
                    try:
                        data_notice[succ_dir].update({'remote': 'Empty:' + str(E)})
                    except KeyError:
                        print('发现了上次遗留的文件哦:')
    if success_video:
        print('移除 所有成品ts')
        os.chdir(local_path)
        for video_com_file, success_num in zip(success_file_lst, success_num_lst):
            try:
                os.remove(video_com_file)  # 移除成品
                data_notice[success_num].update({'completed_del': 'Com_Deleted'})
            except Exception as E:
                data_notice[success_num].update({'completed_del': 'Com_cannt_Deleted' + str(E)})

    if directory:
        print('移除文件夹')
        try:  # 移除 success failed directory
            shutil.rmtree(os.path.join(local_path, "okfun_success"))
            os.removedirs(os.path.join(local_path, "okfun_failed"))
        except OSError:
            pass
    print('传输完成')
    playsound("D:\python_scripts\merge_m3u8\source\MC-hurt.mp3")


def print_notice_all():
    while over_flag == 0:
        # while ftp_download_status == 0 or decry_queue.qsize() != 0 or ftp_send_queue.qsize() != 0:  # ftp_send_queue.qsize() == 0 and success_video_lst != 0:

        print_out = f""
        for video_name in data_notice:
            print_out += f"{video_name:^6} |"  # 列
            for key in data_notice[video_name]:  # 行
                print_out += f"{data_notice[video_name][key]:^10}|"

            print_out += f"\n"
        print(f'{"vdonum":^6} |{"file_lca":^10}|{"ftp_down":^10}|{"decry_fin":^10}|{"com_location":^25}|{"ftp_send":^10}|{"remove":^10}|{"Com_file_del":^10}')
        print(print_out)
        print('■' * 40)
        print(#'ftp_download_status', ftp_download_status,
            't1_down:', t1_down.is_alive(),
            '| decry:', decry_queue.qsize(),
            '  t2_decry', t2_decry.is_alive(),
            '| ftp:', ftp_send_queue.qsize(),
            '  t3_up', t3_up.is_alive(),
            "  success_video_lst", success_video_lst)
        time.sleep(3)


def upload_local_detect():
    """跳过前面几步 仅为了发送成品文件"""
    from sigua_decry_core import file_Rec
    success_lst = file_Rec(local_path, '[\s\S]*.ts')
    print('执行本地检测 成功文件 目录 :', success_lst)
    for success_ts in success_lst:
        video_nu = success_ts.strip('_over.ts')
        success_path = os.path.join(local_path, success_ts)
        data_notice.update({video_nu: {"completed": success_path}})
        ftp_send_queue.put((video_nu, success_path))  # 文件地址存入发送 queue


if __name__ == '__main__':
    local_path = 'C:\\okfun\\'
    start_path = "/okfun/v/"
    remote_path = "/okfun/"  # '/AAmydoc/.native/robot/'
    ip_list = ['192.168.3.101', '192.168.1.124', '192.168.3.107', '192.168.3.102', '192.168.1.13', ]
    port = 6666
    username = 'root'
    password = 'admin'
    data_notice = {}
    over_flag = 0
    host_ip, my_ftp = ftp_link(ip_list)

    # 主线程输出, 最后才关闭
    t0_print = threading.Thread(target=print_notice_all, daemon=True)  # 开启 print_out
    t1_down = threading.Thread(target=ftp_download, daemon=True)  # 开启 后台 下载

    # file_lst = file_Rec('C:\\okfun', "^[0-9]{4,6}$")
    # for video_num_file in file_lst:
    #     print(video_num_file)
    #     decry_queue.put(video_num_file)
    t2_decry = threading.Thread(target=back_decry, daemon=True)  # 开启 后台解密
    # file_lst = file_Rec('C:\\okfun', "^[0-9]{4,6}_over.ts$")
    # for video_num_file in file_lst:
    #     print(video_num_file)
    #     ftp_send_queue.put(video_num_file.strip('_over.ts'), "C:\\okfun\\" + video_num_file)
    t3_up = threading.Thread(target=back_ftp_send, daemon=True)  # 开启 后台发送

    local_detect_fold()
    t0_print.start()
    t1_down.start()
    t2_decry.start()

    t1_down.join()
    print('下载结束 状态t1_down.is_alive() or decry_queue.qsize()', t1_down.is_alive(), decry_queue.qsize())
    t3_up.start()

    t2_decry.join()
    print('解密结束')
    t3_up.join()
    ftp_send_queue.join()  # 前后台 完成后 取消阻塞
    decry_queue.join()
    # 完成 后检测文件发送完成后进行删除
    remove_all_oringa(remote=1, success_video=1, directory=1)

    over_flag = 1
    t0_print.join()


    print(f'{60}s waiting ---')
    time.sleep(60)


"""无音录屏测试:  从远端下载源文件 / 解密/ 回传 / 善后"""
