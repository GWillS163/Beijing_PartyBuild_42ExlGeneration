# 本模块用来下载文件,及多线程下载
import sys
from scrab_img_at_cl import find_url

sys.path.append("..")
import requests
import threading
import time
import queue
import os
# 给http://xxx.xxx.com/xxx/#IUhufhd.jpg 的链接和本地路径将下载

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}


def down_file_to_path(url, filepath):
    """
    传入下载链接, 和本地保存路径
    :param url:   如 'https://img9.51tietu.net/pic/2019-091221/ikunjtrp4hpikunjtrp4hp.jpg'
    :param filepath: 如 './'
    :return:
    """
    print('正在下载:', url, end='/')
    try:
        os.mkdir(filepath)
        print('文件夹  已新建')
    except FileExistsError:
        # print('文件夹  已存在')
        pass

    file_name = url.split('/')[-1]
    path_name = filepath + '/' + file_name
    # print('得到file_name:', file_name, '文件名:', path_name)

    if os.path.exists(path_name):
        print('将下载的文件', file_name, '已存在, pass', end='')
        return
    try:
        for i in range(5):
            url = url.replace(r'i/?i=', '')
            try:
                r = requests.get(url, headers=headers)
            except ConnectionError:
                print(f"|{file_name:>38} | {'网络连接错误':^5}|原链接:{url:<80} ")
                return
            except KeyError:
                print(f"|{file_name:>38} | {'还是包含假图 暂时跳过':^5}|原链接:{url:<80} ")
                return
            except Exception as E:
                print(f"|{file_name:>38} | {str(E):^5}|原链接:{url:<80}")
                return
            # print('##检查 包含查看大图?', end='\n')
            if '点击查看大图' in r.text:
                # print('###包含 点击查看大图')
                with open('./error_img_link.txt', "a+") as f:
                    f.write(url)
                    f.write('\n')
                raise KeyError
            else:
                # print('##尝试写入?', end='\n')
                with open(path_name, "wb") as f:
                    f.write(r.content)
                try:
                    print(f"|{file_name:>20} | {'OK':^5}|原链接:{url:<80} ")
                except:
                    print('ok', file_name)
    except Exception as E:
        print('下载文件出现了非 request错误!', E)
        raise


def size_format(size):
    if size < 1000:
        return '%i' % size + 'size'
    elif 1000 <= size < 1000000:
        return '%.1f' % float(size/1000) + 'KB'
    elif 1000000 <= size < 1000000000:
        return '%.1f' % float(size/1000000) + 'MB'
    elif 1000000000 <= size < 1000000000000:
        return '%.1f' % float(size/1000000000) + 'GB'
    elif 1000000000000 <= size:
        return '%.1f' % float(size/1000000000000) + 'TB'


def download_queue(file_path):
    global lock,task, bad_queue
    while not task_queue.empty():   # 线程内检测当queue 有东西时
        lock.acquire()
        # print('\t\t[Lock]', end='')
        # print(end=" Get:")

        current_task_num = task_queue.qsize()  # 查看que 大小
        down_task_lnk = task_queue.get(timeout=30)  # 拿出来一个任务
        #print(down_task_lnk, end='←当前任务\n')  # 当前任务

        lock.release()
        # print('[UnLock]')
        # print('excess.', current_task_num, end='')  # TODO:启用这条就会显示剩余

        # print('模拟执行', down_task_lnk)
        # down_file_to_path(down_task_lnk, file_path)

        # 执行下载
        url = down_task_lnk.replace(r'i/?i=', '')
        file_name = url.split('/')[-1][-30:].strip('%')
        path_name = file_path + '/' + file_name
        try:
            try:
                print(threading.currentThread().getName(), end=" ")
            except Exception as E:
                print('?thread?', E)
            # 查重
            if os.path.exists(path_name):
                size = os.path.getsize(path_name)
                print(f"{current_task_num}|{file_name:>20}|{'ExistsPass':^10}|{size_format(size):8}|链接:{url:<60} ")
                continue
            # 请求
            try:
                r = requests.get(url, headers=headers, timeout=5)
            except Exception as E:
                print(f"{current_task_num}|{file_name:>20} | {'req Err':^10}|链接:{url:<60}|{str(E):^10}|")
                bad_queue.put(url)
                continue

            # 保存文件
            # retry = 0
            # while retry < 3:
            try:
                if not os.path.exists(file_path):
                    os.mkdir(file_path)
                    print('文件夹  已新建')
                with open(path_name, "wb") as f:
                    f.write(r.content)
            except Exception as E:
                print('保存文件时出现了问题', E)

            # 输出 执行效果
            try:
                print(f"{current_task_num}|{file_name:>20} | {'OK':^10}|原链接:{url:<60} ")
            except:
                print('ok', file_name)
        except Exception as E:
            print(f'{current_task_num}|执行 请求/保存/输出时 出现了未知问题:{E} |源链接{down_task_lnk}')
            raise
    try:
        print(f'{threading.currentThread().getName()}线程执行完毕')
    except Exception as E:
        print(f'未知线程执行完毕', E)
    #
    # while not bad_queue.empty():
    #     bad_task = bad_queue.get()


def multithread_down_file(link_lst, stride, file_path):
    """
    多线程下载, 下载链接是同一个站点的可能会被限速,多线程可能帮不上忙
    :param link_lst:  下载列表如['https://img9.51tietu.net/pic/2019-091221/ai24umljpzpai24umljpzp.png', 'https://img9.51tietu.net/pic/2019-091221/ikunjtrp4hpikunjtrp4hp.jpg']
    :param stride:    多线程数, 如 5
    :param file_path: 下载路径, 如'./'
    :return:
    """
    mstt_tme = time.time()
    global task_queue, lock, task, bad_queue
    task_queue = queue.Queue()
    bad_queue = queue.Queue()
    for i in link_lst:  # 把列表转化未queue对象存入
        task_queue.put(i)
    all_task_num = len(link_lst)
    print(f'{"#"*40}list共{all_task_num}/任务队列共{task_queue.qsize()}准备执行{"#"*40}')

    # 新建多线程
    threads = []
    lock = threading.Lock()
    for i in range(stride):  # 步幅5 五个线程 从队列取东西
        task = threading.Thread(target=download_queue, args=(file_path, ))
        threads.append(task)
        task.start()
        # time.sleep(0.2)  # 几个多线程错开
    for task in threads:
        task.join()

    print(f'{"#"*40}{all_task_num}个 执行完毕 耗时{round(time.time() - mstt_tme,2)}s {"#"*40}')


if __name__ == '__main__':
    # file_download_lst = ['https://img9.51tietu.net/pic/2019-091221/ai24umljpzpai24umljpzp.png', 'https://img9.51tietu.net/pic/2019-091221/ikunjtrp4hpikunjtrp4hp.jpg', 'https://img9.51tietu.net/pic/2019-091404/nj4rv1hoon3nj4rv1hoon3280x180.jpg', 'https://img9.51tietu.net/pic/2019-091320/jyi22oj0nfrjyi22oj0nfr280x180.jpg', 'https://img9.51tietu.net/pic/2019-091403/j5csvvgou4tj5csvvgou4t280x180.png', 'https://img9.51tietu.net/pic/2019-091221/xxkmhho1xjixxkmhho1xji.png', 'https://img9.51tietu.net/pic/2019-091221/a0cx2dy54i4a0cx2dy54i4.png', 'https://img9.51tietu.net/pic/2019-091319/kakimwxklbmkakimwxklbm280x180.jpg', 'https://img9.51tietu.net/pic/2019-091222/kz4rg24cpupkz4rg24cpup280x180.jpg', 'https://img9.51tietu.net/pic/2019-091221/jbdc1dmj0v2jbdc1dmj0v2.png', 'https://img9.51tietu.net/pic/2019-091319/kew3olldl1mkew3olldl1m280x180.jpg', 'https://img9.51tietu.net/pic/2019-091221/erogsolanflerogsolanfl.png', 'https://img9.51tietu.net/pic/2019-091221/itxdms5trheitxdms5trhe.jpg', 'https://img9.51tietu.net/pic/2019-091323/b1fofvnk5ccb1fofvnk5cc280x180.png', 'https://img9.51tietu.net/pic/2019-091401/q100zwoikmfq100zwoikmf280x180.jpg', 'https://img9.51tietu.net/pic/2019-091401/oiycdzkzinsoiycdzkzins280x180.jpg', 'https://img9.51tietu.net/pic/2019-091221/iaahkfeabz1iaahkfeabz1.png', 'https://img9.51tietu.net/pic/2019-091221/m0frvoiz4uvm0frvoiz4uv.png', 'https://img9.51tietu.net/pic/2019-091221/vo2kivcw50dvo2kivcw50d.png', 'https://img9.51tietu.net/pic/2019-091401/tgrbae1q2l3tgrbae1q2l3280x180.jpg', 'https://img9.51tietu.net/pic/2019-091402/tdhwjpe1nrctdhwjpe1nrc280x180.jpg', 'https://img9.51tietu.net/pic/2019-091221/zqhdsflioyxzqhdsflioyx.png', 'https://img9.51tietu.net/pic/2019-091221/vtxvx5sejuyvtxvx5sejuy.png', 'https://img9.51tietu.net/pic/2019-091221/m0mruqsut4jm0mruqsut4j.png', 'https://img9.51tietu.net/pic/2019-091316/fxpjjeltetifxpjjelteti280x180.jpg', 'https://img9.51tietu.net/pic/2019-091221/1p4h1pukas51p4h1pukas5.jpg', 'https://img9.51tietu.net/pic/2019-091221/dekr5sc0xsudekr5sc0xsu.png']

    # 获取用户输入:
    # in_text = input('输入你的链接,我会解析里面的url')
    in_text = """http://i1.hdslb.com/bfs/archive/49efcfa26496927fe8425ba7e12f0b3159c995bd.jpg
http://i1.hdslb.com/bfs/archive/62f2984a338910941e71a6be49c61dcb1a873bdb.jpg
http://i2.hdslb.com/bfs/archive/22fc947e7460e692f699f763fb5d104aee5dd8db.jpg
http://i0.hdslb.com/bfs/archive/7ef797021d323a17868b1f3d85d085bad7daf641.jpg
http://i1.hdslb.com/bfs/archive/b88912ecea4eddc084df7578441251107222c27d.jpg
http://i0.hdslb.com/bfs/archive/d304c6dd6470c3dcd6b4f63ed3211f53764a4d4b.jpg
http://i1.hdslb.com/bfs/archive/8266e299b842df2682fd04b3e1f8c0f36a15e363.jpg
http://i2.hdslb.com/bfs/archive/acc8d6e241f26e01f5e02236f70b62a5950b9e7e.jpg
http://i1.hdslb.com/bfs/archive/9c73acf0f6d353393a4eee4a48735f70e9621d8a.jpg
http://i0.hdslb.com/bfs/archive/acff32f4b1a239937e94884eb4685c2de487460a.jpg
http://i2.hdslb.com/bfs/archive/9f38aed9422d0d0653ab8d13f90ca5897f8b4a65.jpg
http://i0.hdslb.com/bfs/archive/cb8d4cebdaa70a6add2d77da824d3dd06ba46a5e.jpg
http://i1.hdslb.com/bfs/archive/3a47a2ecfce4e9441fe32490336c31e8d03e0890.jpg
http://i1.hdslb.com/bfs/archive/3960441cf24846dd9bf621563307d1cf5a39797e.jpg
http://i0.hdslb.com/bfs/archive/f05721718f06e80b22fa76359a62b681be505438.jpg
http://i0.hdslb.com/bfs/archive/237abd005b1e1b9c0e7d876495c573f840156ed1.jpg
http://i0.hdslb.com/bfs/archive/bf80f5705dc2964e6d602c114aa26e52aa560761.jpg
http://i2.hdslb.com/bfs/archive/de8f97d91bf4cc03200a2524457e51f6bc604413.jpg
http://i2.hdslb.com/bfs/archive/2af854f5dc7f1a80fc938740247d24db02cdb760.jpg
http://i1.hdslb.com/bfs/archive/73395b1251ae112e79049702540ef8dbe1c7a57f.jpg
http://i1.hdslb.com/bfs/archive/1d37e53f32054d99fddca2a6c8bebc313fcc6490.jpg
http://i2.hdslb.com/bfs/archive/c9a7cd69580959b78b2008682f37104f1e05c7f9.jpg
http://i1.hdslb.com/bfs/archive/55c34a3a07261ba89e811b5a1b4c1cff43f8ceb0.jpg
http://i1.hdslb.com/bfs/archive/35ec1c233ad6736139b8e6b3dac39d5bdb26a8a7.jpg
http://i2.hdslb.com/bfs/archive/67b0c8f98a82895856906e237f1cefd34e086ab7.jpg
"""
    file_download_lst = find_url(in_text)
    file_download_lst = list(set(file_download_lst))
    print('解析到你的url', )
    for i in file_download_lst:
        print(i)

    # 多线程下载
    multithread_down_file(file_download_lst, 8, './mult5555i')

    #
    # # 单线程下载
    # stt_tme = time.time()
    # for i in file_download_lst:
    #     down_file(i, './single')
    # print('single_thread used time:', time.time()-stt_tme)