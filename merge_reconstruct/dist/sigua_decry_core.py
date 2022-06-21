# coding:utf-8
import os, re, time, shutil  # , sys
from operate_tools import file_Rec, get_file_binary, move_file_dir, make_dirs
from queue import Queue
from Crypto.Cipher import AES

judge_size = 300  # 文件分片依据
stride = 50  # 步幅
if_merge_success_remove = True  # 合成成功是否移除
if_merge_failure_remove = False  # 失败是否移除

log_content = Queue()

def print_video(str, *args, **kwargs):
    """打印信息 如[2230] 处理中"""
    global video_name
    print('['+video_name+']', end='-')
    print(str, *args, **kwargs)
    return '['+video_name+']'


def single_decry(arg_path, file_name, merge_dir, cryptor):
    data = get_file_binary(os.path.join(arg_path, file_name))
    with open(os.path.join(merge_dir, file_name + '.ts'), 'ab') as file:  # 写入解码的文件
        file.write(cryptor.decrypt(data))

def test_time(txt):
    for i in range(30):
        # print(txt + str(i))
        log_content.put(txt + str(i) + '测试解密 local_decry_f')
        time.sleep(2)

def folder_decry(arg_path, mode='general', verbose=False):  # general preserve
    print('执行内部代码', arg_path)
    global video_name, judge_size, stride, if_merge_success_remove, multi_thread_printout
    video_name = arg_path.split("\\")[-1]
    multi_thread_printout = {# "air": "",
                             "slip": "",  # "-/- [-]",
                             "slip_decry": "",  # "[未解密-]",   # 解密 合并

                             "original": arg_path,  # "-:\\...",  #源文件
                             "completed": "",  # "-:\\--_over.ts",   #合成后文件
                             "decry_temp": "",  # temp文件夹删除

                             "decry_finally": "",         # 合并结果
                             "other": "",
                             "flag": "",
                             }

    def multi_thread_print(key="flag", str=""):
        """ 把屏显信息存入 字典, 然后输出字典"""
        global multi_thread_printout
        multi_thread_printout.update({key: str})

        temp = video_name  # 输出:
        for i in multi_thread_printout:
            temp += multi_thread_printout[i]
        if key != "flag" and verbose == True:
            print(temp)
        log_content.put(temp)
        return temp

    dir_path = os.path.abspath(os.path.join(arg_path, os.path.pardir))  # C:\okfun
    success_video = ""

    # 新建文件夹
    success_folder = os.path.join(dir_path, "okfun_success")  # TODO: 自定义okfun_success文件夹
    failed_folder = os.path.join(dir_path, "okfun_failed")
    for folder_name in [success_folder, failed_folder]:
        try:
            os.mkdir(folder_name)
        except FileExistsError:
            pass
        except Exception as E:
            print('尝试新建时源文件归档目录时 出现异常', E)

    # 查找关键两个文件
    key = os.path.join(arg_path, 'key')
    index_m3u8 = os.path.join(arg_path, 'index.m3u8')
    if not(os.path.exists(key) and os.path.exists(index_m3u8)):
        multi_thread_print("other", 'key_index 核心缺失')
        move_file_dir(arg_path, failed_folder)  # 源文件移动到失败文件夹
        return video_name, multi_thread_printout

    m3u8_file = get_file_binary(os.path.join(arg_path, 'index.m3u8')).decode('utf-8')
    key_b = get_file_binary(key)  # .decode('UTF-8')
    # cryptor = AES.new(key_b.encode('utf-8'), AES.MODE_CBC)  #2021.3.11
    cryptor = AES.new(key_b, AES.MODE_CBC)

    # 获取信息合规文件
    file_lst = file_Rec(arg_path, '^[^\.]{6,18}$')  # '^[^\.]{8}$'   '^.{4,}[^.ok][^.m3u8][^.key]$'

    # 通过m3u8文件获取顺序, 正则分析得到顺序
    video_order = re.findall(video_name + '/(.*)\n', m3u8_file)[1:]
    order_cmd_lst = [i + ".ts" for i in video_order[1:]]

    # 查看分片合规
    if len(file_lst) == len(video_order):
        multi_thread_print("slip", f'分片:{len(video_order)}/{len(file_lst)} {"[正常]"}')
    else:
        multi_thread_print("slip", f'分片:{len(video_order)}/{len(file_lst)} {"[异常]"}')
        multi_thread_printout['decry_finally'] = 'Crash'
        move_file_dir(arg_path, failed_folder)
        return video_name, multi_thread_printout

    # 遍历文件夹的合规文件
    multi_thread_print("slip_decry", '解密中:')
    merge_dir_path = arg_path + '_temp'
    merge_dir = make_dirs(merge_dir_path)
    total = len(file_lst)
    num = 0

    try:
        for file_name in file_lst:
            single_decry(arg_path, file_name, merge_dir, cryptor)  # 使用解密
            num += 1
            print(multi_thread_print(), f"{file_name}成功{num}/{total}",  end='\r ')
            # yeild ''
        multi_thread_print("slip_decry", '[解密Over]')
    except Exception as E:
        # raise
        # 移动temp文件夹, 源文件夹,
        multi_thread_printout['slip_decry'] = str(E)
        multi_thread_printout['decry_finally'] = 'Crash'
        move_file_dir(arg_path, failed_folder)
        move_file_dir(merge_dir_path, failed_folder)
        return video_name, multi_thread_printout
    # 判断 是否需要切割
    # judge_size = 300
    # stride = 50  # 步幅
    file_mode = ''
    merge_fail = False
    # 大小文件判断 并合成
    if len(order_cmd_lst) > judge_size:
        file_mode = 'l'
        # 切割整体列表
        sub_merge = []  # 子合成列表
        # stride = 50  # 步幅
        try:
            combine_output = f'步幅:[{stride}]_合并中:'
            for num in range(0, len(order_cmd_lst), stride):
                sub_all_decry_ts = "+".join(order_cmd_lst[num:num+stride])
                os.chdir(merge_dir)
                result_of_sub_merge = os.popen("copy /b {} {}".format(sub_all_decry_ts, "part"+str(num)+".ts")).read() # 存到目录
                sub_merge.append("part"+str(num)+".ts")  # 把子合成加入列表
                if 'copied' in result_of_sub_merge:
                    combine_output += f'~{num+stride}'
                else:
                    combine_output += '[!!!合并未能成功]'
                multi_thread_printout['other'] = combine_output
                multi_thread_printout['decry_finally'] = 'Crash'
        except Exception as E:
            multi_thread_print("slip_decry", '!!!尝试 大合并子合并时出现了意料外的问题:' + str(E))
            multi_thread_printout['decry_finally'] = 'Crash'
            return video_name, multi_thread_printout
        # 子合成 合成最终
        all_sub_ts = "+".join(sub_merge)
        # print_video('子合成顺序:', all_sub_ts)
        os.chdir(merge_dir)
        merge_res = os.popen("@copy /b {} {}".format(all_sub_ts, arg_path + "_over.ts"))

    else:
        file_mode = 's'
        sub_all_decry_ts = "+".join(order_cmd_lst)
        os.chdir(merge_dir)
        merge_res = os.popen("copy /b {} {}".format(sub_all_decry_ts, arg_path + "_over.ts"))  # 存到目录

    # 合并后 的 归档操作
    if 'copied' in merge_res.read():
        success_video = arg_path + "_over.ts"
        multi_thread_print("completed", success_video)
        merge_fail = False
        # 源文件移动到成功文件夹
        move_file_dir(arg_path, success_folder, arg_path=arg_path)
    else:
        multi_thread_print("decry_finally", '!!!合并未能成功' + merge_res.read())
        merge_fail = True
        # 源文件移动到失败文件夹
        move_file_dir(arg_path, failed_folder)
    multi_thread_print("slip_decry", '[合并完成]')

    # 缓存 删存 控制
    # remove_odd_file  (成功移除确认&  成功)  or (失败移除 & 失败)
    rm_condition = (if_merge_success_remove == True and merge_fail == False) or (if_merge_failure_remove == True and merge_fail == True)
    if mode == 'delete' or mode == 'general':
        try:  # 移除 缓存
            for file_name in file_lst:  # 移除解密文件夹的剪辑
                os.remove(os.path.join(merge_dir, file_name + '.ts'))
            if file_mode == 'l':  # 移除大的子剪辑
                for sub_m in sub_merge:
                    try:
                        os.remove(os.path.join(merge_dir, sub_m))
                    except Exception as E:
                        print_video('!!!出现问题移除子合成时:', E)
            os.chdir(dir_path)
            shutil.rmtree(merge_dir)  # 移除临时文件夹
            multi_thread_print("decry_temp", '###已移除缓存')
            # os.removedirs(video_name)  # 移除源文件夹
        except Exception as E:
            multi_thread_print("decry_temp", '!!!尝试移除缓存文件时出现了意料外的问题:' + str(E))
    else:
        multi_thread_print("decry_temp", '###缓存文件保留')

    multi_thread_print("decry_finally", f'Done')
    multi_thread_printout['other'] = ''
    # print_video('■' * 40)
    multi_thread_printout.update({"completed": str(success_video)})  # 补救措施, 上面不知哪里没有给成品赋值

    return video_name, multi_thread_printout

if __name__ == '__main__':
    # ---1. EXE程序拖拽获取
    # cap_res = sys.argv[1:]  # 获取文件路径
    # print('captured:', cap_res)  # 获取文件名
    # for i in cap_res:
    #     decry(i)
    # ---2. 手动输入调试
    # decry(r'D:\python_scripts\merge_m3u8\19651')
    print(folder_decry(r'D:\python_scripts\merge_m3u8\okfun\22043'))
    # print(decry(r'D:\115yun_remote_test\14704'))
    # ----3. 本地使用
    # local_path = 'D:\\okfun'
    # os.chdir(local_path)
    # for dir in os.listdir(local_path):
    #     decry(os.path.join(local_path, dir))
    #     video_name, multi_thread_printout = decry(r'C:\okfun\15380', mode='general')
    #     print(video_name, multi_thread_printout)
    print('\n###执行完毕100s后退出程序,如需再次使用请重复拖拽步骤')
    time.sleep(100)
