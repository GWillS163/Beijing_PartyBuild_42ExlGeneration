import os
import re
import requests
from Crypto.Cipher import AES

def get_file_binary(path):
    """输入路径返回文件二进制文件内容"""
    with open(path, 'rb') as file:
        data = file.read()
    return data


def get_key(m3u8_url):
    return key.encode()
    pass

def signle_decry(file_name, merge_dir, cryptor):
    """本地读取文件解密"""
    data = get_file_binary(file_name)
    with open(os.path.join(merge_dir, file_name + '.ts'), 'ab') as file:  # 写入解码的文件
        file.write(cryptor.decrypt(data))


def web_signle_decry(key_url, ts_name, merge_dir, cryptor):
    """给网络下载的ts 解密"""
    # key_url = 'https://sgjk3.com/api/video/4802/key?sign=184485166d97d3267729133345c70cd3&t=1616031900'
    res_content = requests.get(key_url).content
    with open(os.path.join(merge_dir, ts_name), 'ab') as file:  # 写入解码的文件
        file.write(cryptor.decrypt(res_content))

# signle_decry('D:\python_scripts\merge_m3u8\web_down\j6df0XMh2995000.ts', './/', cryptor)
"""-------------"""

headers = """GET /api/video/4802/key?sign=184485166d97d3267729133345c70cd3&t=1616031900 HTTP/1.1
Host: sgjk3.com
Connection: keep-alive
User-Agent: Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Mobile Safari/537.36 Edg/89.0.774.54
Accept: */*
Origin: https://www.sg149.xyz
Sec-Fetch-Site: cross-site
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://www.sg149.xyz/
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
"""


def web_get_ts_lst(m3u8_url):
    """获得列表 m3u8_url to ['j6df0XMh2995000.ts', 'j6df0XMh2995001.ts', 'j6df0XMh2995002.ts',]"""
    res = requests.get(m3u8_url).text
    if '401' in res:
        print(m3u8_url, 'm3u8返回401 ')
        raise BaseException
    # return re.findall('\n(.*?\.ts)\n', res)
    ts_lst = re.findall('\n(.*?\.ts)\n', res)

    file_line = res.split("\n")
    key = ''
    for index, line in enumerate(file_line):  # 第二层
        if "#EXT-X-KEY" in line:  # find找解密Key
            method_pos = line.find("METHOD")
            comma_pos = line.find(",")
            method = line[method_pos:comma_pos].split('=')[1]
            print("Decode Method：", method)

            uri_pos = line.find("URI")
            quotation_mark_pos = line.rfind('"')
            key_path = line[uri_pos:quotation_mark_pos].split('"')[1]

            # key_url = res.rsplit("/", 1)[0] + "/" + key_path  # 拼出key解密密钥URL
            res = requests.get(key_path)
            key = res.content
    return ts_lst, key.decode('utf-8')

def down_ts_decry(ts_url, ts_lst, dst, cryptor):
    """下载列表里的所有视频"""
    stor_ts_lst = []
    for ts_name in ts_lst:
        if 'http' in ts_name:
            url = ts_name
            ts_name = ts_name.split('/')[-1]
        else:
            url = ts_url + ts_name
        print('下载', ts_name)
        web_signle_decry(url, ts_name, dst, cryptor)
        stor_ts_lst.append(os.path.join(dst, ts_name))
    return stor_ts_lst

def merge_all(ts_lst, arg_path, file_name):
    """给定列表, """
    judge_size = 50
    stride = 50
    if len(ts_lst) > judge_size:
        sub_merge = []  # 子合成列表
        for num in range(0, len(ts_lst), stride):
            sub_all_decry_ts = "+".join(ts_lst[num:num + stride])
            # os.chdir(merge_dir)
            result_of_sub_merge = os.popen(
                "copy /b {} {}".format(sub_all_decry_ts, "part" + str(num) + ".ts")).read()  # 存到目录
            sub_merge.append("part" + str(num) + ".ts")  # 把子合成加入列表
            if 'copied' in result_of_sub_merge:
                print('合并成功',num)
            else:
                print('!!!合并未能成功',num)

        # 子合成 合成最终
        all_sub_ts = "+".join(sub_merge)
        print('子合成顺序:', all_sub_ts)
        # os.chdir(merge_dir)
        merge_res = os.popen("@copy /b {} {}".format(all_sub_ts, file_name + "_over.ts"))
        for i in sub_merge:
            os.remove(i)
    else:
        sub_all_decry_ts = "+".join(ts_lst)
        os.chdir('.')
        merge_res = os.popen("copy /b {} {}".format(sub_all_decry_ts, arg_path + "_over.ts"))  # 存到目录
    return merge_res

def main_download_decry_merge(m3u8_url, arg_path, file_name, key):
    ts_half_url = m3u8_url.split('?')[0].split('/')[-1]
    ts_lst, key = web_get_ts_lst(m3u8_url)  # m3u8获得列表
    print(key, ts_lst)
    # if not key:
    #     key = get_key(m3u8_url)  # key
    cryptor = AES.new(key.encode(), AES.MODE_CBC)

    stor_ts_lst = down_ts_decry(ts_half_url, ts_lst, arg_path, cryptor)  # 下载列表并解密
    merge_all(ts_lst, arg_path, file_name)  # 合并并删除
    for ts in stor_ts_lst:
        print('移除:', ts)
        os.remove(ts)

if __name__ == '__main__':
    m3u8_url = 'https://cdn.jinbobz.com/videos/202010/hls/b57f3b84-f852-48a3-921f-3efc52a7f8af/index.m3u8?id=4802&sign=6c3472412131aac5724c0573f38031e5&t=1616031900'
    # key = 'df538e25a9c989b8' 

    # m3u8_url = 'https://sgjk3.com/api/video/6595/m3u8?sign=e2d42f8ce240beba32ee66c79aaceed1&t=1616057100'
    # key = '4f4289a1dcca9bbf'
    key= ''

    m3u8_url = 'https://sgjk3.com/api/video/7216/m3u8?sign=44046b7e11989af6483f21dfa04f7982&t=1616058000' # 测试成功

    # 注意有时 m3u8禁止访问
    main_download_decry_merge(m3u8_url, '.', 'file_name.ts', key)
