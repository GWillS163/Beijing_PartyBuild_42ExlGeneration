import json
import requests
import time

def drink_chiken_soup():
    """
    通过 api url 返回鸡汤文并打印
    :return:
    """
    soup_url = 'https://data.zhai78.com/openOneGood.php'
    res = requests.get(soup_url)
    res = json.loads(res.text)
    # print(res)
    print(res['txt'])
    return res['txt']


txt_lst =[]
while True:
    result =drink_chiken_soup()
    if result in txt_lst:
        print('==============================发现重复!!!')
    txt_lst.append(result)
    time.sleep(1)
