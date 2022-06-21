# 调用所有函数进行整合, 并对UI.py 提供函数
# 使用多线程执行操作
import threading
import time
from operate_tools import *
from queue import Queue
from decry_core import decry_obj

t0_notic_q = Queue()
t1_downs_q = Queue()
t2_decry_q = Queue()
t3_sends_q = Queue()
t4_delete_q = Queue()
main_decry_info = Queue()
lock = threading.Lock()
data_notice = {}  # 所有文件信息数据

def __t1_down():
    """下载线程 """
    print('t1开始执行下载线程:')
    while t1_downs_q.qsize():
        [file_num, local_temp_folder, remote_source_path, remote_storage_path, adb_tool, temp_file, is_delete_other_file, strip] = t1_downs_q.get()  # 源文件Num, 路径
        # print_notice(file_num, '下载状态', '下载中')
        data_notice[file_num].update({'下载状态': '下载中'})
        # 进行下载
        res = download_adb_folder(os.path.join(remote_source_path, file_num), local_temp_folder, adb_tool, temp_file)
        print(file_num, res)
        data_notice[file_num].update({'下载状态': '下载完成'})
        # lock.acquire()
        t1_downs_q.task_done()
        t2_decry_q.put([file_num, local_temp_folder, remote_source_path, remote_storage_path, adb_tool, temp_file, is_delete_other_file, strip])
        # lock.release()
    print('t1下载线程关闭:')


def __t2_decry():
    """解密线程"""
    while t1_down.is_alive() or t2_decry_q.qsize():
        # lock.acquire()
        [file_num, local_temp_folder, remote_source_path, remote_storage_path, adb_tool, temp_file, is_delete_other_file, strip] = t2_decry_q.get()
        # lock.release()
        # 解密处理
        # print_notice(file_num, '解密状态', '处理中')
        data_notice[file_num].update({'解密状态': 'decrying'})

        # for i in range(3):
        #     time.sleep(1)
        file = decry_obj(os.path.join(local_temp_folder, file_num), is_delete_other_file, strip)
        file.main_decry()
        t2_decry_q.task_done()
        if file.all_in_one['最终情况'] == '[合成完毕,请打开目录检查]':
            # print_notice(file_num, '解密状态', 'decry完成')
            data_notice[file_num].update({'解密状态': 'decry完成'})

            # lock.acquire()
            t3_sends_q.put([file_num, local_temp_folder, remote_source_path, remote_storage_path, adb_tool, temp_file, is_delete_other_file])
            # lock.release()
        else:
            data_notice[file_num].update({'解密状态': file.all_in_one['最终情况']})
    print('t2结束')

def __t3_send():
    """发送线程"""
    while t2_decry.is_alive() or t3_sends_q.qsize():
        # lock.acquire()
        [file_num, local_temp_folder, remote_source_path, remote_storage_path, adb_tool, temp_file, is_delete_other_file] = t3_sends_q.get()
        # lock.release()
        data_notice[file_num].update({'发送状态': '发送中'})
        # for i in range(3):
        #     time.sleep(1)
        upload_adb(os.path.join(local_temp_folder, file_num + '_over.ts'), remote_storage_path, adb_tool)
        data_notice[file_num].update({'发送状态': '完成'})
        print(f'{file_num}发送完成')
        # lock.acquire()
        t3_sends_q.task_done()
        t4_delete_q.put([file_num, local_temp_folder, remote_source_path, remote_storage_path, adb_tool, temp_file, is_delete_other_file] )
        # lock.release()
    print('t3结束')

def __t4_delete():
    while t3_send.is_alive() or t4_delete_q.qsize():
        [file_num, local_temp_folder, remote_source_path, remote_storage_path, adb_tool, temp_file, is_delete_other_file] = t4_delete_q.get()
        if not is_delete_other_file:
            data_notice[file_num].update({'远程删除': 'False无需删除'})
            return
        rm_dele = remote_delete(remote_source_path, file_num, adb_tool).close()
        data_notice[file_num].update({'远程删除': '远程删除完毕'})
        print(f'{file_num}远程删除完成')
        try:
            os.remove(os.path.join(local_temp_folder, file_num + '_over.ts'))
            data_notice[file_num].update({'本地删除': '本地删除完毕'})
            print(f'{file_num}本地删除完成')
        except Exception as E:
            data_notice[file_num].update({'本地删除': f'本地删除出错{E}'})
        t4_delete_q.task_done()
    print('t4 删除结束')

def print_thread_status():
    """输出线程状态信息"""
    #
    #         current_print.put(
    #             f'{"vdonum":^6} |{"file_lca":^10}|{"adb_down":^10}|{"decry_fin":^10}|{"local_temp_location":^25}|{"ftp_send":^10}|{"remove":^10}|{"Com_file_del":^10}')
    #         current_print.put(print_out)
    #         # print(f'{"vdonum":^6} |{"file_lca":^10}|{"adb_down":^10}|{"decry_fin":^10}|{"local_temp_location":^25}|{"ftp_send":^10}|{"remove":^10}|{"Com_file_del":^10}')
    #
    # print(t0_notic_q.qsize(), t1_down.is_alive(), t2_decry.is_alive(),)

def print_notice(file_num, str, info):
    """输出文件处理信息"""
    # lock.acquire()
    if file_num not in data_notice.keys():
        data_notice.update({file_num: {}})
    data_notice[file_num].update({str: info})
    # t0_notic_q.put(data_notice)
    # lock.release()
    # playsound()

def print_out_thod(data):
    print_out = f""
    # lock.acquire()
    for video_name in data:
        print_out += f"{video_name:^6} |"  # 列
        for i in data[video_name].keys():
            print_out += f" {data[video_name] [i]} | "
        print_out += f"\n"
    return print_out

def __print_in():
    while t1_downs_q.qsize() or t3_send.is_alive():
        print_out = print_out_thod(data_notice)
        # lock.release()
        time.sleep(3)
        main_decry_info.put(print_out)
        # print(print_out)

def __self_print_listen():
    """ 监听本来对外的队列"""
    while main_decry_info.qsize() or t3_sends_q:
        print(main_decry_info.get())

def self_print_listen():
    t = threading.Thread(target=__self_print_listen)
    t.start()

def main_multi_thread(local_temp_folder, remote_source_path, remote_storage_path, adb_tool, temp_file, is_delete_other_file, strip):
    local_v_lst = []
    remote_vlst = []
    for i in local_fold_detect(local_temp_folder):
        print_notice(i, '文件类型', '本地文件')
        local_v_lst.append(i)
    for i in remote_fold_detect(remote_source_path, adb_tool):
        print_notice(i, '文件类型', '远程文件')
        remote_vlst.append(i)
        t1_downs_q.put([i, local_temp_folder, remote_source_path, remote_storage_path, adb_tool, temp_file, is_delete_other_file, strip])
    for i in local_v_lst:  # 若只存于本地则开始解密
        if i not in remote_vlst:
            t2_decry_q.put([i, local_temp_folder, remote_source_path, remote_storage_path, adb_tool, temp_file,
                            is_delete_other_file, strip])

    # for i in range(1, 5): # 自行测试的代码
    #     # print_notice(i, '文件类型', '远程文件')
    #     data_notice[i] = {}
    #     t1_downs_q.put([i, local_temp_folder, remote_source_path, remote_storage_path, adb_tool, temp_file, is_delete_other_file])
    print('文件查找完毕', data_notice)
    # self_print_listen()
    t0_print.start()
    t1_down.start()
    t2_decry.start()
    t3_send.start()
    t4_dele.start()

os.chdir('.')
t0_print = threading.Thread(target=__print_in)
t1_down = threading.Thread(target=__t1_down)
t2_decry = threading.Thread(target=__t2_decry)
t3_send = threading.Thread(target=__t3_send)
t4_dele = threading.Thread(target=__t4_delete)

if __name__ == '__main__':
    main_multi_thread('C:\\okfun\\', '/storage/emulated/0/okfun/v/', '/storage/emulated/0/okfun/', 'C:/Tools/andriod/platform-tools/', '.\\temp.txt', False)
