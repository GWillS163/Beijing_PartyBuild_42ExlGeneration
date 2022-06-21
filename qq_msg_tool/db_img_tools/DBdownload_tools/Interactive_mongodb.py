# coding=utf-8
from pymongo import *
import time

data_lst = [{'img': 'http://i2.hdslb.com/bfs/archive/e0784716f4553c198484eed7381f6187319c4a8c.jpg',
             'tit': 'FlexConnect.第50期教主技术进化论-亁颐堂现任明教教主秦柯CCIE#13778',
             'lnk': 'http://www.bilibili.com/video/BV1Jb411K7TD',
             'tme': '02:00:36', 'dat': '2019-4-12'},]


class My_mongoDB:
    def __init__(self, url_link, db_name, username_title):
        # self.username = 'admin'
        # self.passwod = 'Cisc0123'
        self.url_link = url_link
        self.db_name = db_name
        self.db = db_name
        # self.collect = collect_name
        client = MongoClient(url_link)#.format(self.username, self.passwod))
        self.db_obj = client[db_name]  # 选择或进入数据库
        # self.db_obj.create_collection('QQ_bot')  # 其实不写，下一句也会自动创建
        self.collect_lst = self.db_obj.collection_names()
        self.rename_and_show(username_title)

        # 不同用户选择数据库, admin 可选择, 其他用户固定表单
        if username_title == 'ADMIN':
            self.admin_choice_collect()
        elif username_title == 'CL_user':
            self.db_coll = self.db_obj['CL_user']
        else:
            self.db_coll = self.db_obj['User']

    def admin_choice_collect(self):
        try:
            while True:
                try:
                    input_collect_name = input('###输入要使用的序号>>>')
                    if not input_collect_name:  # 不合法则重试
                        # print('输入为空!重试!!')
                        continue
                    input_collect_name = int(input_collect_name)
                    break  # 合法输入则跳出循环
                except Exception as E:
                    print('你输入的啥玩意儿没int成功', E)
            self.db_coll = self.db_obj[self.collect_lst[input_collect_name]]  # 连接第N号位的
        except Exception as E:
            print('##出现错误,使用默认ADMIN')
            print(E)
            self.db_coll = self.db_obj['ADMIN']  # 选择数据库内的合集

    def insert_mydata_to(self, data):
        data.update({'create_time': time.strftime("%Y-%m-%d %H:%m", time.localtime())})
        self.db_coll.insert(data)

    def query_data(self):
        find_links_lst = []
        for i in self.db_coll.find():
            find_links_lst.append(i)  # yield对象改成lst对象,便于后面裁剪
        return find_links_lst

    def show_collect(self):
        print(f'{"=" * 30}')
        print(f'{"No":2}|{"Collect_name":^22}|{"Count":^5}')
        for n, i in zip(range(len(self.collect_lst)), self.collect_lst):
            # print('n, i 值', n, i)
            print(f'{n:2}|{i:<22}|{self.db_name[i].count()}')  # print合集名称
        print(f'{"=" * 30}')

    def rename_and_show(self, username_title):
        if username_title == 'ADMIN':
            while True:
                lst = self.collect_lst
                print(f'{"="*30}')
                print(f'{"No":2}|{"Collect_name":^22}|{"Count":^5}')
                for n, i in zip(range(len(lst)), lst):
                    print(f'{n:2}|{i:<22}|{self.db_obj[i].count()}')  # print合集名称
                print(f'{"="*30}')
                # 重命名
                input_No = input('是否输入重命名的序号, 空回车跳过')
                try:
                    if input_No:
                        input_No = int(input_No)
                        input_new_name = input('输入要命名的名称')
                        self.db_obj[lst[input_No]].rename(input_new_name)
                        continue
                    break
                except Exception as E:
                    print('这啥玩意儿重命名没成功:', E)
                # print(f"{'=' * 20}进行下载数据库{'=' * 20}")
                break

    def mongo_insert(self, data):
        data.update({'create_time': time.strftime("%Y-%m-%d %H:%m", time.localtime())})
        # 插入前进行比对 url ,title, output_lst
        # data = {'title': link_title,
        #         'url': link_url,
        #         # 'html': html,
        #         'output_lst': link_img_lst,
        #         'un_output_lst': unoutput,
        #         }
        if not data in self.query_data():
            self.db_coll.insert(data)
        else:
            print('似乎之前有做过')


if __name__ == '__main__':
    acc_pass = input('输入monogo DB的账户密码: 形如admin:Cisco')
    db = My_mongoDB(f'mongodb+srv://{acc_pass}@qyt-cluster.catxh.azure.mongodb.net/QYT-cluster',
                            'private_spider_data', 'QQ_bot')
    # TODO:后台队列执行漂亮打印 例如
    # 线程1: ## 读取文件名
    # 线程2: ## 读取文件名  ## 检查  ## 尝试写入
    # 线程3: ## 读取文件名  ## 检查
    # 线程4: ## 读取文件名  ## 检查  ## 尝试写入  ## 写入成功

    # TODO: 打印线程剩余:
    # # 插入数据
    # for da in data_lst:
    #     db.insert_mydata_to(da)

    # 查询数据
    result = db.query_data()
    for i in result:
        print(i)
