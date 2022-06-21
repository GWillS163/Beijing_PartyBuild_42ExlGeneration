import logging
import os
import shutil
from playsound import playsound
from old.ftp_operate import MyFtp
from sigua_decry_core import decry, file_Rec


# 后续 删除处理
def remove_all_oringa(remote, success_video, directory):
    playsound("D:\python_scripts\merge_m3u8\source\MC-hurt.mp3")
    print('移除远程/ 本地success. 目录 / 本地成品 :')

    if remote:
        print('清空 远程目录:', src)
        my_ftp.ftp_client.cwd(src)
        success_video_lst = os.listdir(os.path.join(local_path, "okfun_success")) # 检测本地成功文件
        print('移除', success_video_lst)
        for succ_dir in success_video_lst:
            my_ftp.ftp_client.rmd(succ_dir)  # 移除远程

    if success_video:
        print('移除 成品ts')
        os.chdir(local_path)
        success_lst = file_Rec(local_path, '[\s\S]*.ts')
        print('success_ready:', success_lst)
        for success_video in success_lst:
            os.remove(success_video)  # 移除成品

    if directory:
        print('移除文件夹')
        try:  # 移除 success failed directory
            shutil.rmtree(os.path.join(local_path, "okfun_success"))
            os.removedirs(os.path.join(local_path, "okfun_failed"))
        except OSError:
            pass
    print('传输完成')
    playsound("D:\python_scripts\merge_m3u8\source\MC-hurt.mp3")

def download():  # 下载
    remote_all_dir = my_ftp.ftp_client.nlst(src)
    print(my_ftp.ftp_client.nlst(src))
    n = 1
    for video_num_dir in remote_all_dir:  # 文件夹
        print('下载中:', video_num_dir)
        down_gene = my_ftp.DownLoadFileTree_okfun(src, video_num_dir, bck )
        for i in my_ftp.ftp_client.nlst(src + video_num_dir):
            print(n, "/", len(remote_all_dir), next(down_gene), '-', video_num_dir, end='\r')  # 下载目录树
        n += 1
    print('=====下载完成=======')

def decry_():
    file_lst = file_Rec(local_path, "^[0-9]{4,6}$")
    print(f'{"num":^5}|{"分片":^20}|{"slip_decry":^9}|{"original":^19}|{"completed":^25}|{"decry_fin":^8}')
    success_lst = []
    for dir in file_lst:
        video_name, data = decry(os.path.join(local_path, dir), mode='general')
        success_lst += video_name if data['completed'] == 'Done' else ''
        print(f'{video_name:^5}|{data["slip"]:^20}|{data["slip_decry"]:^9}'
              f'|{data["original"]:^19}|{data["completed"]:^25}|{data["decry_finally"]:^8}')
    print('=======解密完成=======')

def upload():
    from sigua_decry_core import file_Rec
    success_lst = file_Rec(local_path, '[\s\S]*.ts')
    print('success_ready:', success_lst)
    for success_video in success_lst:
        # for success_video in success_lst:
        src, dst = os.path.join(local_path, success_video.split('\\')[-1]), os.path.join(bck, success_video)
        print(src, dst)
        my_ftp.uploadFile(src, dst)  # 上传成品至手机

if __name__ == '__main__':
    # 要连接的主机ip    # 用户名# 密码
    host_ip = '192.168.3.104'
    # host_ip = '192.168.1.124'
    username, password = 'root', 'admin'
    my_ftp = MyFtp(host_ip, 6666)
    src, bck, local_path = '/okfun/v/', '/okfun/', 'C:\\okfun\\'

    # 如果登录成功则执行命令，然后退出
    while True:
        if my_ftp.ftp_login(username, password) != 1000:
            continue
        logging.warning('login success , now will execute some command')

        download()  # 下载
        decry_()  # 解密
        upload()  # 上传
        # remove_all_oringa(remote=0, success_video=0, directory=0)  # 删除

        my_ftp.ftp_logout()
        break
    print('single over')
