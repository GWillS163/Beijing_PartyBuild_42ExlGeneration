import requests
import re

def out2file(str):
    """输出文本文件"""
    with open(logfile, 'w+', encoding='utf-8') as f:
        f.write(str)
        f.write('\n')

def url_filter(text):
    """文本筛选到超链接"""
    url_list = re.findall(r"(\"http://[\s\S]*?\")", text)
    return url_list


def access_page(url, key_words):
    print('正在访问:', url)
    """访问单页"""
    headers = {}
    res = requests.get(url, headers=headers)
    body = res.text
    url_list = url_filter(body)
    if key_words in str(body):
        out2file(body)
        print('保存了一个感兴趣页面')
    return url_list

def recursion(url, deepth):  # Flase
    """递归调用访问单页"""
    if deepth <= 0:  # 递归到达指定深度
        return
    recursion(url, deepth-1)
    url_list = access_page(url, key_words='旅行')

def fake_recursion(url, deepth):
    for i in range(deepth):
        url = access_page(url, key_words='理解')
        

def main_exe():
    global logfile, history_url
    deepth = 3
    begining = 'https://www.beijingxxw.net/'
    logfile = './spider.log'

    fetched_url = {1: [],
                   2: [],
                   3: [], }
    history_url = []
    # 主程序
    url_list = access_page(begining, deepth)

    # 副程序



main_exe()