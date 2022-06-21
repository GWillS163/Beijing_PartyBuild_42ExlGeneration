from edit_docx import edit_docx
import os, re, time
import zipfile
# 定位到文件

# 通过正则 查找当前目录下 文件
def file_Rec(file_rule):
    file_lst = []
    for i in os.listdir():
        if re.match(file_rule, i):
            if not re.match('~', i): # 不匹配含 ~ 的正在打开的文件
                # print('\t\t┣' + i)  # 打印文件名
                file_lst.append(i)
    return file_lst
    # os.unlink(i)  # 移除文件

# 解压文件， 返回解压后路径
def unzip_resource(zip_path):
    file_name = os.path.basename(zip_path)
    file_dir = os.path.dirname(zip_path)
    if os.path.splitext(zip_path)[1] == '.zip':
        file_zip = zipfile.ZipFile(zip_path, 'r')
        for resource_file in file_zip.namelist():
            file_zip.extract(resource_file, file_dir + '/' + file_name.replace('.zip', ''))
    file_path = zip_path.replace('.zip', '')
    resource_path = file_path + '\\'
    return resource_path
ESA = [1]
WSA = [1, 2]
ACS = [1, 2]
FirePower = [1, 2, 3, 4]
ISE = [1, 2, 3, 4, 5]
Secure = [1, 2, 3, 4, 5]
CCNA_SEC = [1, 2, 3, 4, 5]
VPN = [1, 2, 3, 4, 5, 6, 7, 8]
Firewall_ASA = [1, 2, 3, 4, 5, 6, 7, 8]
CCIELAB = []

def main():
    global err_lst
    path = 'C:\\Users\\admin\\Downloads\\'
    os.chdir(path)
    print('进入目录：', path)

    print('■■■■■[找到以下名为no_check.*.zip的文件]■■■■\t\t')
    for i in file_Rec('no_check_.*.zip'):  # 返回目录的no_check file_lst
        print(i)

        direct = unzip_resource(path + i)
        os.chdir(direct)  # 进入解压目录
        print('  进入目录：' + direct)
        time.sleep(2)

        print('\t┳■■■■■找到以下名为.*.docx的文件]■■■■■')
        for file in file_Rec('.*.docx'):  # 遍历文件
            print('\t┣' + file, end='\t')  # 打印文件名
            try:
                edit_docx(file, 'A')
            except Exception as exc:
                print('\n出现异常，报错信息为\t', exc)
                err_lst.append(file)
                pass


err_lst = []
if  __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
    print('批阅完毕，出现{}个错误'.format(len(err_lst)), '\n分别是')
    for i in err_lst:
        print(i)
    time.sleep(20)

