#参考官方文档 https://ai.baidu.com/ai-doc/ANTIPORN/jk42xep4e
import requests
import time
import string
""" 你的 APPID AK SK """
APP_ID = '19891414'
API_KEY = 'usNMOs7sdzwep3QOgY4xoFV2'
SECRET_KEY = 'gw5vs1lKOLRGE6MstE8X8zbmxsXVBWIg'


tm = time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
#读取图片
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

#编码图片


def image_encap():



    headers = {
        'host': 'aip.baidubce.com',
        'x-bce-date': '{}T{}Z'.format('2020-5-15', '13:54:02'),
        'authorization': 'bce-auth-v1/46bd9968a6194b4bbdf0341f2286ccce/2015-03-24T13:02:00Z/1800/host;x-bce-date/994014d96b0eb26578e039fa053a4f9003425da4bfedf33f4790882fb4c54903',
        'content-type': 'application/x-www-form-urlencoded',
    }

    data = {
        # 'image':'/9j/4AAQSkZJRgABAQAASABIAAD/4QBYRXhpZgAATU0AKgAAAAgAAgESAAMAAAABAAYAAIdp',
        'imgUrl': 'https://ai-solution-admin.cdn.bcebos.com/audit%2Fdemo%2Fcensoring-demo.jpg'
    }
    print('-<<[发送中]>>--',end='')
    #res = requests.post(api_url, headers=headers,json=data)
#    print(res.json())
    #print('\t\t' + str(res.json()['status']))




def get_token():
    # 先获取token，保质期30day
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(API_KEY, SECRET_KEY)
    response = requests.get(host)
    if response:
        token = response.json()#['refresh_token']
        print(token)
        return

#get_token()
def method_token():
    # 使用token +url post
    api_url = 'https://aip.baidubce.com/rest/2.0/solution/v1/img_censor/v2/user_defined?access_token=' + str(token)
    headers = {
        'Content-Type':'application/x-www-form-urlencoded'
    }
    data = {
            #'image':'/9j/4AAQSkZJRgABAQAASABIAAD/4QBYRXhpZgAATU0AKgAAAAgAAgESAAMAAAABAAYAAIdp',
            'imgUrl':'https://ai-solution-admin.cdn.bcebos.com/audit%2Fdemo%2Fcensoring-demo.jpg'
        }
    print('-<<[发送中]>>--',end='')
    res = requests.post(api_url, headers=headers,json=data)
    print(res.json())
    print('\t\t' + str(res.json()))

if __name__ == '__main__':
    token = '24.d51dc05f98fbc3fa4e908fde9f6b7302.2592000.1592128960.282335-19891414'
    method_token()