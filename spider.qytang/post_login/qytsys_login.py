import requests
import json
import re


# 第一次爬
url = 'https://qytsystem.qytang.com/accounts/login/'
headers = {
    # "Cookie":"csrftoken=Z7PDSdu0sxFR1NttRt7mpoFQ0fBukKccC3V1iGhCzy12wkIkVszfJEl4E9nGOGEt; "
    #          "sessionid=1rz6avj2hkkei9htr5qqewgdjt8rdly9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                                " AppleWebKit/537.36 (KHTML, like Gecko) "
                                "Chrome/83.0.4103.61 Safari/537.36 Edg/"
                                "83.0.478.37"
    }


def get_csrf_token():
    try:
        response = requests.get(url, headers=headers)
        csrf_token = re.findall(r'name="csrfmiddlewaretoken" value="(.*?)"',response.text)[0]
        print('得到csrf_token :', csrf_token)
        return csrf_token
    except:
        print('requests错误！赶紧去排错!!')



def login(data):
    afterURL = "https://qytsystem.qytang.com/net_basic_student/home"        # 想要爬取的登录后的页面
    loginURL = "https://qytsystem.qytang.com/accounts/login/"     # POST发送到的网址
    login = requests.post(loginURL, data=data, headers=headers)                  # 发送登录信息，返回响应信息（包含cookie）
    print('login.text:\t\t',login.text)
    response = requests.get(afterURL, cookies = login.cookies, headers = headers)    # 获得登陆后的响应信息，使用之前的cookie
    return response.text


# print(json.loads(req.text))
# req = requests.get(url)  # 发送请求
# print(req.text)  # 获取请求，得到的是json格式
# print(json.loads(req.text))  # 获取请求，得到的是字典格式
# print(type(req.text))
# print(type(json.loads(req.text)))


if __name__ == '__main__':
    print('')
    csrf_token = get_csrf_token()

    # 第二次爬
    data = {'csrfmiddlewaretoken': csrf_token,
            'username': "nb_mengjq",
            "password": "8Mz.AEdo"}
    req = login(data)  # 发送post请求，第一个参数是URL
    print(req)