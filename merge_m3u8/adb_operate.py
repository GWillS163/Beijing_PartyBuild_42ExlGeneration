# 须在本机提前测试好 adb的连接与否, 需授权密钥连接至本机调试
import os
import time

os.chdir(r'C:\Tools\andriod\platform-tools')

remote_v = '/storage/emulated/0/okfun/v/'

def download_adb(remote, video_num, dst):
    """adb pull /storage/emulated/0/aamydoc/233.mmx C:\okfun\\"""
    os.chdir(r'C:\Tools\andriod\platform-tools')
    # yield os.popen(f'adb pull {remote}{video_num}/ {dst}')
    os.system(f'adb pull {os.path.join(remote,video_num)}/ {dst} > C:\\Users\\admin\\Desktop\\transh.txt')

# download_adb(remote_v, '21978', 'C:\\okfun\\')
# time.sleep(5)
# download_adb(remote_v, '21981', 'C:\\okfun\\')

def upload_adb(localfile, remote):
    os.chdir(r'C:\Tools\andriod\platform-tools')
    """upload_adb('D:\\', 'EB1.mmx', '/storage/emulated/0/aamydoc')"""
    res = os.popen(f'adb push {localfile} {remote}')
    print(res)

def scan_adb(remote):
    os.chdir(r'C:\Tools\andriod\platform-tools')
    lst = os.popen(f'adb shell ls {remote}')
    x = [i.strip('\n') for i in lst]
    return x
# scan_adb('/storage/emulated/0/okfun/v/20999')

# Delete
def delete_abd(remote, video_num):
    os.chdir(r'C:\Tools\andriod\platform-tools')
    return os.popen(f'adb shell rm -r {remote}{video_num}')


# print('-', [i for i in delete_abd(remote_v, '20999')])
#3.删除tmp文件夹及下面所有文件（可行！）#
# Copy
# adb shell rm -r /data/local/tmp/local/tmp
# 删除文件夹：
#
# 如果不为空，则删除不了，报：Directory not empty
#
# Copy
# adb shell rmdir /data/local/tmp/local/tmp
# 如果不为空，则删除不了，报：Directory not empty
#
# 删除文件夹下所有的文件
#
# Copy
# adb shell rm /data/local/tmp/local/tmp/*.*
# 删除文件夹下所有的xml文件
#
# Copy
# adb shell rm /data/local/tmp/*.xml