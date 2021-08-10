# 操作工具库
# 设计理念是 没有print输出, try, 只简单的返回值 便于复用
# 参数路径等可调用
import os
import re
import shutil
# from config_parser import cfg_adb_tool_location, cfg_temp_file

def file_re(paths, re_str):
    """通过正则筛选某个目录下的文件"""
    file_lst = []
    for i in os.listdir(paths):
        if re.match(re_str, i):
            file_lst.append(i)
    return file_lst

def get_file_binary(paths):
    with open(paths, 'rb') as file:
        data = file.read()
    return data

def local_fold_detect(local_temp_path):
    """本地检测文件夹"""
    local_video_lst = []
    for video_num in file_re(local_temp_path, '^\d+$'):
        local_video_lst.append(video_num)
    return local_video_lst


# print(' '.join(local_fold_detect("C:\\okfun\\")))
def delete_local_temp(local_dir):
    shutil.rmtree(local_dir)
    os.mkdir(local_dir, mode=True)
    return '本地文件删除完毕'

# adb tool
def remote_fold_detect(remote, cfg_adb_tool_location):
    os.chdir(cfg_adb_tool_location)
    lst = os.popen(f'adb shell ls {remote}')
    x = [i.strip('\n') for i in lst]
    return x

def remote_delete(remote, video_num, cfg_adb_tool_location):
    os.chdir(cfg_adb_tool_location)
    return os.popen(f'adb shell rm -r {remote}{video_num}')

def upload_adb(localfile, remote, cfg_adb_tool_location):
    """push <文件> 至 <远端>"""
    os.chdir(cfg_adb_tool_location)
    """upload_adb('D:\\', 'EB1.mmx', '/storage/emulated/0/aamydoc')"""
    res = os.popen(f'adb push {localfile} {remote}')
    res.close()
    return '文件上传完毕'

def download_adb_folder(remote_video_path, dst, cfg_adb_tool_location, cfg_temp_file):
    """adb pull /storage/emulated/0/aamydoc/233.mmx C:\okfun\\"""
    os.chdir(cfg_adb_tool_location)
    os.system(f'adb pull {remote_video_path}/ {dst} > {cfg_temp_file}')  # > {cfg_temp_file}
    return '下载完成'

