from Interactive_mongodb import My_mongoDB
from url_download_file import multithread_down_file
import time
import threading
from scrab_img_at_cl import get_web_link, find_url
# from pprint import pprint
import os
os.chdir('.')

global username_title
global username


def auth_welcome():
    while 1:
        try:
            with open('./db_user_pass.ini', 'r', encoding='utf-8') as f:
                x = f.readlines()[0]
            # print('读取到配置:', x)
            username = x.split(':')[0]
            if 'CL' in username:
                username_title = 'CL_user'
            elif 'admin' in username == 'admin':
                username_title = 'ADMIN'
            else:
                username_title = 'User'
            break
        except Exception as E:
            print('提示:新建db_user_pass.ini', '输入monogo DB的账户密码: 形如admin:Cisco')
            print(f'读取配置文件的错误!')
            acc_pass = input('输入monogo DB的账户密码: 形如admin:Cisco:')
            with open('./db_user_pass.ini', 'w', encoding='utf-8') as f:
                f.write(acc_pass)
            input('###回车重试以认证\n\n')

    print(f'{"*" * 50}')
    print(f'\t{"欢迎使用社区图贴下载解析器":50}')
    print(f'{username:^50}')
    print(f'{"*" * 50}')
    return username, username_title, x

def db_link(username, username_title, x):
    # 后台1. 链接数据库 admin 可选择, 其他用户固定表单
    # 数据库collection 名称根据username不同, admin可管理所有
    print('.', end='')
    db = My_mongoDB(f'mongodb+srv://{x}@qyt-cluster.catxh.azure.mongodb.net/QYT-cluster',
                         'private_spider_data', username_title)
    # 查询数据
    find_links_lst = db.query_data()
    print('\r!', end='')
    return find_links_lst, db


def data_local_store():
    #  整理collect数据库数据, 仅ADMIN 可存盘到本地
    stt = time.time()
    if username_title == 'ADMIN':
        # print('写入整理中...')
        f = open('data_base.txt', 'a+', encoding='utf-8')
        f.write(f'{"=" * 20}{time.strftime("%Y-%m-%d %H:%M", time.localtime())}{"=" * 20}\n')
        for i in find_links_lst:
            try:
                f.write(str('title:' + i['title']))
                f.write('\n')
                f.write(str('url:' + i['url']))
                # print('\t添加:', i['title'], 'over')
            except Exception as E:
                print('\t出现问题:', i['title'])
            f.write('\n\n')
        f.write('\n')
        # print('整理后的列表lst_data:', result)
        f.close()
        print('本地整理完毕: used_time', time.time() - stt)
    return find_links_lst


def front_uesr_input():
    global history_mode
    # 获取合法输入, 分析到 输入链接
    try:
        print('###输入你要分析的图贴链接, 查看历史请输入q 回车')
        while True:
            # TODO: 给用户选择 , 继续喂入图片?还是查看历史
            input_links = input(f'[{username_title}]{username}>')
            if input_links:
                if input_links == 'quit' or input_links == 'exit' or input_links == 'q':
                    raise IOError
                find_links_lst = find_url(input_links)
                if not find_links_lst:
                    print('###输入你要分析的图贴链接, 查看历史请输入q 回车')
                    continue
                break

        # 传入URL链接 这里下载
        print(f'找到链接, 共{len(find_links_lst)}')
        for i in find_links_lst:
            print(i)
        if find_links_lst:
            print('###开始执行解析下载###')
            for find_link in find_links_lst:
                print('\t正在解析...' + find_link[-18:])
                try:
                    (link_url, link_title, body, link_img_lst, unoutput) = get_web_link(find_link, verbose=False)
                except Exception as E:
                    print('尝试解析时出现了问题:', E)
                    continue
                print('标题:', link_title)
                print('链接:', link_url)
                print(f'检测到图片链接:{len(link_img_lst)}个')

                # 入数据库部分
                data = {'title': link_title,
                        'url': link_url,
                        # 'html': html,
                        'output_lst': link_img_lst,
                        'un_output_lst': unoutput,
                        }
                # 插入数据库
                try:
                    db.mongo_insert(data)
                    print('记录ed')
                except Exception as E:
                    result = '记录出现问题' + str(E)
                    print(result)
                    pass
                return link_img_lst
    except IOError:
        print('进入历史功能')
        history_mode = True


def back_link_db():
    global find_links_lst, db, database_status, history_mode
    print('历史加载中 ')
    try:
        find_links_lst, db = db_link(username, username_title, x)
        print('历史已加载')
        database_status = True
    except Exception as E:
        print('历史功能不可用:', E)
        database_status = False

def judge_db_status():
    """判断DB 状态 返回True 或进行重试
        判断Collect 返回True或重试
    """
    if database_status:
        if db.db_coll:
            return True
        else:
            print('Collection请选择')
            while True:
                user_input = input('DataBase未连接是否重试[y/n]')
                if user_input == 'y' or 'Y':
                    db.admin_choice_collect()
                    break
                elif user_input == 'n' or 'N':
                    break
                else:
                    continue
    else:
        while True:
            user_input = input('DataBase未连接是否重试[y/n]')
            if user_input == 'y' or 'Y':
                back_link_db()
                return True
            elif user_input == 'n' or 'N':
                return False
            else:
                continue


def history(find_links_lst):
    # print('\n已选择查看历史')
    if not database_status:
        print('历史功能暂不可用!')
        return

    # 读取数据库进行下载
    # if username_title == 'ADMIN':
    #     db.rename_and_show(username_title)  # ADMIN可以rename
    # if input('是否刷新历史记录:'):

    print(f'{"=" * 30}')
    print(f"{'No':3}|{'Length':^7}|{'Title':<80}")
    n = 1
    for i in find_links_lst[:]:
        print(f"{n:3}|{len(i['output_lst']):^7}|{i['title']:<80}|{i['create_time']:>40}")
        n += 1
    print(f'{"=" * 30}')

    # collection页 获取下载参数 输入
    while True:
        try:
            print('Ctrl C /输入q 中断返回上一级菜单')
            print('###全部回车即代表默认值: 从开头到结尾, 下载到./imgDownload文件夹下')
            choice = input('选择开始的条目序号:')
            choice_end = input('选择结束的条目序号:')
            path = input('输入存储文件夹名:')
            if choice == 'q' or choice_end == 'q' or path == 'q':
                break
            if choice == choice_end == '':
                print(f'{"=" * 10}{"使用默认值!!!":25}{"=" * 10}')
                print(f'{"=" * 10}{"全部下载到./imgDownload文件夹下":25}{"=" * 10}')
                clip_result = find_links_lst[:]
            else:
                choice = int(choice) - 1
                choice_end = int(choice_end)
                clip_result = find_links_lst[choice:choice_end]
            if path == '':
                path = 'imgDownload'
            else:
                pass

            # 对Collect 选择 进行下载
            all_need_down_lst = []
            for i in clip_result:
                all_need_down_lst += i['output_lst']  # 逐一处理每一个数据库选择的output_lst
            return list(set(all_need_down_lst)), path
            # for i in all_need_down_lst:
            #     print(i)
            # if all_need_down_lst:
            #     multithread_down_file(all_need_down_lst, 5, path)
            # break
        except KeyboardInterrupt:
            # print('中断, 返回上一菜单')
            break
        except Exception as E:
            print('你输入的有问题,重来:', E)
            continue

if __name__ == '__main__':
    global link_img_lst, history_mode, path
    try:
        # 首页欢迎
        username, username_title, x = auth_welcome()
        back_link_db()
        while True:
            history_mode = False
            # try:
            # # 新建多线程
            # threads = []
            # lock = threading.Lock()
            # task1 = threading.Thread(target=front_uesr_input, args=())
            # threads.append(task1)
            # task2 = threading.Thread(target=back_link_db, args=())
            # threads.append(task2)
            # for task in threads:
            #     task.start()
            # for task in threads:
            #     task.join()
            link_img_lst = front_uesr_input()   # 输入写入数据库
            if history_mode:
                if input('是否重新加载 历史记录[y确认/回车跳过]:'):
                    back_link_db()
                if judge_db_status():
                    if database_status:  # 数据库后台连接
                        find_links_lst = data_local_store()  # 本地存储
                        link_img_lst, path = history(find_links_lst)
                else:
                    print('历史未能加载')

            if not link_img_lst:
                print('!!!可供下载的链接为空!\n\n\n\n')
                continue
            print('####开始下载 下载列表#####')
            try:
                print('下载到:', path)
            except:
                path = "imgDownload"
            # 展示link_lst
            for i in link_img_lst:
                print(i)
            # 使用link_lst
            if link_img_lst:
                multithread_down_file(link_img_lst, 5, path)

    except Exception as E:
        print('出现:', E)
        raise
    input('############################程序异常############################')
