import base64
import json
from pprint import pprint
from urllib import parse

import requests
import time

# 2020年8月28日, 10点10分
# 注意,本代码通过httpapi与 QQ_bot 进行交互.
# !!!!!!!! 功能不完整!!!!!!!!!!!


send_qwx_url = 'http://172.16.66.170:4000/send?t=1&tos=23&content={}'
# send_msg_url
# send_pic_url

# 群消息
def group_msg(text, togroup, image=''):
    url = host_port + '/sendgroupmsg'
    data = {
            'fromqq': selfqq,  # 2154024779,
            'togroup': togroup,  # 1106878273,
            'text': text + image if image else text,
            'fromtype': 2 if image else '',
            'path': image if image else '',
            'url': image if image else '',
    }

    try:
        s = requests.post(url, data)
        s = requests.get(host_port + '/send?t=1&tos=23&content={}'.format(text))
    except Exception as E:
        s = False
        print(E)
    time.sleep(1)
    return s

# 饲料消息
def private_msg(text, toqq):
    url = host_port + '/sendprivatemsg'
    data = {
            'fromqq': selfqq,  # 2154024779,
            'toqq': toqq,  # 1106878273,
            'text': text,
    }
    try:
        s = requests.post(url, data)
        # s = requests.get(host_port + '/send?t=1&tos=23&content={}'.format(text))
    except Exception as E:
        s = False
        print(E)
    time.sleep(1)
    return s

def group_temporary(text, toqq, togroup):
    """
    :param text:
    :param 给哪个 QQ:
    :param 你们在哪个组?:
    :return:
    """
    url = host_port + '/sendgrouptempmsg'
    data = {
            'fromqq': selfqq,  # 2154024779,
            'togroup': togroup,
            'toqq': toqq,  # 1106878273,
            'text': text,
    }
    try:
        s = requests.post(url, data)
    except Exception as E:
        s = False
        print(E)
    time.sleep(1)
    return s

# 发送私聊 发送图片
def send_pm_pic(toqq, pic='',  fromtype=0,img_url='', path='', flashpic=''):
    """

    :param toqq: 指定好友QQ
    :param fromtype: 选填 指定图片来源类型(0:pic参数,1:本地文件,2:网络文件 默认为0)
    :param flashpic: 选填 指定是否闪照(true,false)
    :param pic:  [fromtype=0时]指定数据(请使用BASE64+URL编码:url_encode(base64_encode(src)))
    :param path: [fromtype=1时]指定文件路径(请使用绝对路径,存在特殊字符请使用URL编码)
    :param url:  [fromtype=2时]指定文件url(存在特殊字符请使用URL编码)
    :return:
    """
    url = host_port + '/sendprivatepic'
    data = {
        'fromqq': selfqq,
        'toqq': toqq,
        'fromtype': fromtype if fromtype else 0,
        # 'pic': pic #if fromtype == 0 else '',
        'path': path if fromtype == 1 else '',
        # 'url': img_url if fromtype == 2 else '',
        # 'flashpic': flashpic if flashpic else False,
    }
    pprint(data)
    try:
        s = requests.post(url, data)
    except Exception as E:
        s = False
        print(E)
    time.sleep(1)


# 获得缓冲区
def get_buffer():
    """新建一个session"""
    url = host_port + '/allocsession'
    try:
        s = requests.post(url, '')
        current_session = json.loads(s.text)['session_id']
        return current_session
    except Exception as E:
        print(E)

# 删除会话
def del_buffer(sessid):
    """删除一个<指定session>"""
    url = host_port + '/removesession'
    data = {
        'sessid': sessid,
    }
    try:
        s = requests.post(url, data)
        print(s.text)
    except Exception as E:
        print(E)

# 清空事件缓冲区
def resetevent(sessid):
    """ 应该是 清空信道内内容"""
    url = host_port + '/resetevent'
    data = {
        'sessid': sessid,
    }
    try:
        s = requests.post(url, data)
        print(s.text)
    except Exception as E:
        print(E)


def getevent(sessid):
    """获取<指定session> 里的事件
       离线后的不同session 消息相同"""
    url = host_port + '/getevent'
    data = {
        'sessid': sessid,
    }
    try:
        s = requests.post(url, data)
        # print(s.text)
    except Exception as E:
        print(E)
    try:
        result = json.loads(s.text)
        pprint(result)
    except Exception as E:
        print('json.loads出错!', E)


def geteventv2(sessid):
    """获取session 里的事件v2-支持直接解析json"""
    url = host_port + '/geteventv2'
    data = {
        'sessid': sessid,
    }
    try:
        s = requests.post(url, data)
        result = json.loads(s.text)
        try:
            msg = result['events']
            if msg:
                pprint(msg)
                print('='*20, end='\n\n')
        except Exception as E:
            print('#geteventv2 获取失败:', E)
            print('#geteventv2 状态码:', result['status'])
    except Exception as E:
        print(E)


# def get_event2(toqq, text):
#     url = host_port + '/sendprivatemsg'
#     data = {
#             'fromqq': selfqq,  # 2154024779,
#             'toqq': toqq, # 1106878273,
#             'text': text,
#     }
#     try:
#         s = requests.post(url, data)
#         # s = requests.get(host_port + '/send?t=1&tos=23&content={}'.format(text))
#     except Exception as E:
#         s = False
#         print(E)
#     time.sleep(1)
#     return s

def auto_accept():
    url = host_port + '/setfriendaddrequest'

    HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'fromqq': selfqq,  # 2154024779,
        'qq': '782659451',
        'seq': '',
        'op': 1,
    }
    try:
        s = requests.post(url, data)
        # s = requests.get(host_port + '/send?t=1&tos=23&content={}'.format(text))
    except Exception as E:
        s = False
        print(E)
    time.sleep(1)
    return s

if __name__ == '__main__':
    # global fromqq, togroup, selfqq, host_port
    toqq = 1274667113   # 发送至哪个QQ
    # toqq = 2097897464   # 发送至哪个QQ
    # togroup = 1106878273  # 发送至哪个群
    togroup = 630424368  # 发送至哪个群

    # host = '172.16.66.170'
    host = '137.78.5.44'
    port = 10429
    selfqq = 2934289319
    # selfqq = 2154024779
    host_port = 'http://' + host + ':' + str(port)

    print(f'{"="*20}尝试无状态下发送!{"="*20}')
    # print('尝试图片')
    # pic = "%2f9j%2f4AAQSkZJRgABAQEAYABgAAD%2f4QAiRXhpZgAATU0AKgAAAAgAAQESAAMAAAABAAEAAAAAAAD%2f2wBDAAIBAQIBAQICAgICAgICAwUDAwMDAwYEBAMFBwYHBwcGBwcICQsJCAgKCAcHCg0KCgsMDAwMBwkODw0MDgsMDAz%2f2wBDAQICAgMDAwYDAwYMCAcIDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz%2fwAARCABaAjgDASIAAhEBAxEB%2f8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL%2f8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4%2bTl5ufo6erx8vP09fb3%2bPn6%2f8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL%2f8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3%2bPn6%2f9oADAMBAAIRAxEAPwD668G6rJpWs2szFfMjbD57MDg%2fqDX0hDqa6%2fo0Nwqr5kh3Eg%2fe4%2fLr%2btfM1%2fbtFfzMqttYpJnHAyoXA%2f74z%2fwL3r2f4M63%2faHh0wszExcjn1I96%2feswiq9OGKguiv81t95%2bJYGEqFWphJfZbXrZ2T%2ba1OilG5t3%2bTQG%2fDj9almhOQ2Dt9e2ajztP4cCvPjsejykscrBl%2fA%2fpVqI7hz6VR8zaR0q5YsGDYb5lXdyevtWdTRXKjK5T1STbKx%2fT1rLl1pvtEmH2ySllJODwevb6flWr4gg%2bRtuTxketco%2fF23OeeD2qZS5YcxlUutjYST5sqdxx8pzjNX7OKNrlVVvlJILnnI74H9OelZlmq55%2fi547VoW9wLaVWH3lOfpXh1cyqc1omUYzkdZpmjtPCY8FvKIx9Mf559q6v4dRf2drEbcrtIABHXmuN0fVF8nYMNvOST06f5%2fSt%2b3vMus2JMk7to9Mjp%2bVY1JVKtNxl1PRw9CUZqZ7N4m0tda0PnOduQAK8e1fT10q8kVVb5c8MenevZPA97%2faPhiBjzgFT61wXxP8OyW2tvKq%2fLNyMA%2fwCFfP5RXdOtKhLY%2brzTL416ca%2fWyucrpn7yP5n2liOMf1qp4i0uMQyAMwXaTzWrY6cS%2b5shs1qahpLXFn5iq2FyTkfKa%2bg%2bsezqJnj%2fAFNcp47fRlMj7w7msXUhya63XNOaC7mBBbLfl0rC1fTcJu%2bbnsvavpo1FKmefKKg7JHOSuWft9c1E54%2bXmrt1blTkY61XliPFcntbGikJaHZJ07d61FnIC4FZscR3Cr0f3BRGtqTIJpSaRZ2PHHv7Uki4P40kGRJznHetZVLxOfm1LO1cfe%2bhxUezDbe3XFTQqSP71OWMqynbn6D%2fP8Ak1y%2b3urHoRlzQOO%2bImlgxRTc7t20%2flmuO8nbXpnjLT2udCPy%2fNG27p1%2fzmvPZI8DvmvUwGKvDl7HzeMjyzKfk4NPWFcbs%2frU%2flZFOMO013%2b2uee5Gl4Zu%2fKnWPIw1d3on7yIqf4fu4rze3LJIp9OeK9B8P3G9Y2z16461wTrcsz0MFU6G1FbZx%2bf0qSOHr71OkeRUnlZxjd%2fWtJVDPFaMytRtN0bflWKYcD0xXWXVvuiP071hXVt5U38IHSvNzK7gproVga19Gch4ysCEjuI87o%2bf5f41d0lvOijf6GtbUdN%2b1WTrxz0Pb1%2fpWZ4WtmS3aHjdGxB9uTRg%2berRVt07G%2bIkrl2JABtx90469qsWi7jzVmxsfNuFX1Hf2rUg0zy2H9a5amWVJNps5a2KVNK6MuWx3r8u6qsmjb1z8wPWupZVWLjsKzryUKprvwOBVPd3D6%2fOcPdR4%2f8VfDqwHcN2Mhhx27155MFR8HtXtXxLtPtWk7h8zQvnH%2bzzXiGoxNHqDRnpng1%2br5DWdSjyvofjnEtOrTxL6JjJZQF%2fCqTzskvTj1q0yMx%2fDFRT2rFP1r6CNkfLPm3bN%2fRr77TZJ0yvBxWvaHcPxrmvDMoiutrfxdq6a0XGP6V5eKjyyaR9FgcRzRTL0MY4%2fwqSS2Vl%2b9T4R8oFS%2bWxFeW56no1JcyuZRi8icN%2bFblv%2fpNp%2bGaoXdtg9%2buat6E%2bEI%2bnWprtShc9nJ8VdqLLunthdufumrg6fhWfnyr1WOPm4JrQXivO6H1cnZqXcrSLtkbtzmm1ZuYzt3VX71DBx6hsDoao3MO01oKMMM1Dew7h%2fhWlKWtjlrRurmc4468fSmYw1SMuOOaaRn0rricJ1ngK93xSQHH%2fPQevoa6IjIrg%2fDV8LPUIpG%2b6Dg%2fQ9a7wda%2bEz%2fD%2bzxHOtpfmtz9R4VxntcJ7KW8H%2bD1X6kdNIqRgTTe9eGfRjGXbSVIRkVH1rMBrjIptSE4prjBoAj25NNYc8U8jdimsuKhoCJ%2btFOZc0UgOEkjaeeGPbmOUFT8vfaSDn2xj%2fgX0rqvgtqzWOuPau20SIQFz15H%2bFcubz7KizfN%2b5IdhjkqPvAe5XIHuav6XP8A2R4shl3fxDkc19VkdR1aEsO9mnb1Tv8Ar%2bB8RxBR9hjniFs1Fv8AL9D2wzsyD%2b7npnjP0qrJKI3xnP8Ak0tjcedAsi8bgCPbgUzazD%2bZNc0Y2epzVKzeonmsKtWkhXldzc4qubbbI3H3ePrVmC32kNxj39KU7NGcKzuTXw3jP3hjAPrXF30b21w2eNrY%2fDNduz7lk24XAyM9%2fwDIrE1iyy27%2bFjgjNYxs4tM9CNpWZn2dw7GtC3jklPOeR0qHTbRVxwRtrUjby0Zdobfg554xn%2fEfrXiVqcYyPSoxjYu6duQqqjkckA53dK6Gxndh8zN8o4H49PasHTIivY5HIrUhkYwhGxwT%2f8Aqqo2eiN3Ky0PbPgnqX23wxIrNuaOU%2fgCBitnxfoqanaq7Rh2jb9PSvOfgl4gGl6u1q3ScgcAYGR659q9ckTzodv94V8RmdN0MY2uup9bl8lXwii%2fQ8mbTvIu2XHyK3NWL2aRrFlU7FwTtH%2bfrWx4k0Bra%2baRcfMMYyc%2fyqFNPkeLbxjjGO1elHERklM8%2bdNq8Ty3xPYbLnJXryea53VrVShKr8ucfT1r0rxR4fZrdj8vy9iTk1w%2bpaeVkKt69q%2bqwOIU4WPm8XTamcTd23704U7c%2blVZYOeRit%2fUrHbJk%2fxZHvj%2fADis5rTduI4C9u9Z1KlnY54vuZ4ix%2f8ArqxDEyBdylVbvUqW4A71NDEM4%2fAe1Z%2b2KK00WPurUap%2b8G38RWkyZXb%2fAHe56VA0I78hq3Va6scsnYW2i2Mfl%2bUmphFubqVUn8qbCMdMVOVx%2bPSvOqVeWZ1YafQqahbC4tZEK7gwI5rzPVLH7NeOu3pnj0NeqBijH26Vw%2fjXTfK1Dcfuvya2wOL5avL3PPzKHVHMBDS7DmrBtee2KclsZK%2bihUctj5%2bcktyvEmF9fWuu8K3Ra2HP3W4rAh085%2bvFdB4btvJQqcdc1VXA1pq9rGmHxKjI7WwP2iFW6etWkX5enIqloc29FVq2UgDR5yM%2fWoleGjOzEWkrlSSHenSsjULVAw3Lnn8q6QwYXqvT1rF1i32x%2blOi1J8sjbJ6EZ1eVleKyjkhAwu36VzcsX9k%2bKJo1%2fdxyAED1Pf%2fAD7V0GmXeUZfrwax%2fGttgx3Sgbozn8v%2fAK1ehhVCFR0tro6cywcqFbXYvCVoyrrwQc5xWhc3yhPlbHGc1k2si3VmjLzuAPNPXdsA4yDzn0rz82ryw9L2sVs7P5ixOFjWoKS3j%2bTL633mDvVeeI5qCJhu%2bXPHpV9U82IYzxXLleZe20lucdGCguU5%2fWNNS7hZZE%2bV8qff0rw%2fxzogsNXYLHs5I6%2fl%2blfQ11ZeajKcA9R%2bVeW%2fFzw9mfztvzTLnqeo4NfeZDjOStyPZnwXGOF5qftF0PMxCvFDQA9qtQwfJTmiwv8AKvtvaH5VKoULdfs1yGXgrzXW2Z8yFH7sBmudktf4vl%2bma2%2fDkga3Mf8Ad5Fc%2bL96PMdGAxPLPlN20Xfz7dKuRpVWyHy%2fh0rQRPlrwqktT6KNa6sV7q23iobUfZpsY25%2fWtIQb4%2feqUsTK43YHPNRGV1ZlYLE%2bzrWJrtd0O9f4auWUnnQK27tVaL97Afpin6VJhiv904P41yy3P0qjNVKHMvUuyxmRKpuvNaQQEccD3qpLFhj9T0rNs1pS5okQ5FMuE3x%2fSpQnIoePC04SsxVI3Rl3C%2bXyahb516Yq1cw81VePY1dsWeXKNmPtJFWUZHQ9K9B0m8%2b3abDIzbmZQG%2bo4NedouHyMY712Hga58y1kh%2fusJB75GP6V4nEGH58P7Rbxf%2fAAD6rhPFcmK9k9pK3zWq%2fX7zcoIyKVgc0ma%2bGP0kjIwaRh8tPkptAiMjFB5pzim1ADSmR%2f8AWpm3HU1KeRUbLikAxx97txRSsu5qKmwHAIfkH0%2fPinwj91a%2bsZEf125AP44zUMZ4H0pyFtzhf4sSfQjg%2fwDsv5V6uQ4j2eJSfX%2fhvybZ4vE%2bG9phlUXS6%2bTt%2bqSPavDMhl0WBh94KMe3StBI8vHu%2fwCWgJ%2bv%2bf61h%2fD27W58PQ7c%2fu%2bua6azOVX%2b8tdmKvGpJeZ8bRkpRVx8Vhk925A%2fCp5rTZEp%2fEVbtRhgvy7W%2fSrLxboX4464x06V5kqzudipow5Tn5VX5VGCc%2frVO7TzSR904xWhcQ8nsev41Vul3RNwvsR3rqps2w8uhlxRFWDZ%2fh44q9AyBJN3YY%2bnv%2bFZouPs92cqCNjqOOASpUH8M5%2boFWrW7ZF%2bXjcOQffP%2bNeTjlyu56lGWhq2reXK2wY%2bUg%2b4I5q7azbh0yeoGawXucLtVVyvI46%2b306Vp2NwCfvL1zweBzXmxrWeh0nQ6DeGw1iCRVwy4YgnP419D6Re%2fwBoabBN3kQE185212yRLGqIyZLLvHqBn%2bQr2f4Oax%2faXhwx%2fwAVu2OOmDn39q8vPafPTjVXQ9nIcRy1XSfU6PUrAXKbskMveoLXRlijx26j2rSor5hVJJWPppYeDlzM5nX%2fAA2s9vJtLfMCK8r8XaGtvIzcna354r3l13rXMeOPDi31ozKAGHXHUj8q9jK8ydKfLLY8HNstvH2kD531awDSOfvbTux%2bn%2bFYs8B7r685ruPF%2bimwnk%2fi2nBI5%2fpXL3AzuX2wCa%2boxFRO0l1Pj1eLsZxgVW%2bX3wfWk2%2fvM9attEGxjA6mojExP4%2fyrm9oVzDEQMOPTp6VEwGSf4v51M0bb8Y%2bvFNa3cnaRt%2box1rro06k9EjlqzS3IUPz%2fQZxVmJyYyM9wAMf565pken88t%2bR6GtOysVHy8eg%2fGitltWer0OWOOhCWhm%2bW2Vxzz%2bVZ3i7Q%2ft1luJ%2f1fP%2bea6rydp4qG%2bVXtmDEcjvXThsshTmqk3exjjMVKpH3UeW%2fwBkKpHzGpFtlWtPWAsF46857bazJrrYrcV9pSr4enHdI%2bbkm3qHl4NaGjMpkAz97gVjS3ZccduTUtjOY7hW46iuTEZzQSstTSkmpHa6I2y6xnO79a6m0Hy888VyOjXAmjSTuf0rsNL%2fAHkC9N2MV5%2bJqKcVOOzPSqT90eF7HpWfrFn5kOeyjNbcdvu69jUdxZeYu3jpiuSNazuTgMV7KspHCmP7Pdtt6tzRe263VnJGx%2bZRnHpWlrVmUuTx909qqkFCrc9e1aZjinRVPFL7L19GffZjTWIwymtzC8Nv5UUsWMeS2wfTt%2fStGaHavHTBzVG6t%2f7N8Q7gv7ub0H%2bfWtqFAVNelmFNYijKC2ktP69TwcDUTXJL0M2JBBMoB45GK0rIGRv0zVSSHHNW9NkVJFDDr6dq%2fN8txjo1rPucdSLi7Mmlh%2bUf7RrkfiLpP2zSZHyf3J3j%2bv6V3kkHmov1z71mavYb24%2b7g5%2fGv0rB4rlmpxPnc8oqrQce585XVkttfSL%2fAA54qMxha6j4iaC2mau3tz%2bBJI7VgvCdtfpWHxCqU4zXU%2fAsZF06soPoyl5Ksan0p%2fst4v8AdzUog2noetMNvzuraUrqxwKs4yUkdLZ8H5eB3Falsm9f881l2b%2faIlZeOADmtiyX93%2bFeHWZ9Rh8RdEqR9j2qG%2btqvQQljx%2btPubbcn0%2fSuNVLMqpU5ZKSMq3GFX6VHt8rUf9%2fj%2fAAq08Jik46Gob5CE8wY%2fd8iqm76o%2fSOG8YqtHl7GpbtviVsdahvIiGz60abMsiYHf5h%2bNWriLdDn24rGWjsepRl7Ot7N9dDNPB9acBjrQy4bpigLQj0JRKd%2bmDnPWqUqdhWndxfLkfrVGRDuP17V2U5XR5leNmVc7SK2vCN99l1ONv4XIjP4%2fwD16yWj46c1LaP5Tn8qVamqlNwl1Q8HWlSqxqR3TT%2b49GbHemdqj0q6N7psMjfeYYP1HB%2flU%2bOK%2fNa1Nwm4Po7H7NRqqrTVRbNJ%2ffqMpj8GpCuKQqM8CsjQjprLzmnMNpoxQBGaRhuFPYYptZgRsMfXtRTnXmipdwPN1b5B9KsWG1rpUbpICmf7vcfmQBVRH%2b79BT0lZG3cZBDfkcj%2bVFGSjUTf9efyKx1GVXDzpw3a09ei%2bb0PSPg7fmW0mt5G5U9M8ivQLb5epG76V5L8Pr%2f7N4ohf5VS6Cn5z93NeuRxef8AN8qKcD26f%2fWr6THS52qr%2b0rv12f43PymnUSk4rbp6PVGhby7m6fN7cVaMhxwflbrWfCcuTkenHeri5aPk968ecdbnX7Yz9QXEh%2fxqq4byzhdwx6dK0r1fNbnp61R8rzVYfp6V0U5aF4er75zOpOYZXOTx60yz1jKfw%2b1T%2bKLXyw3Jx0z71g2E373bXPmFNOPMj2qUjo0u9%2fp16itHR5S8nyjzMe3pyf5Vi2itInQ9eorW0m3aKdvmC7eM%2fmK%2bRlUs7HdF9TsNIK3Q%2ffNsVYmKbV6kL8oP1IAz7133wW1z7FqclsXVY5QBgjHP1rzXT59ibWG7%2bEbT1roPD2o%2fY9SjlPHlkMAeM9uv%2belaSXtqUqb6l0K3sayqLoz6AFFVdH1JdT06GZSp8xATg55wKmnuFgQszAADPJr5FxadmfoEakXHnWxITis3X5IxbsGkVW6cmsvxB49i01SF8tvfeK4LxN8QTeFtqxjB7nrXpYPLa1WSdrI%2bezXOqNOm4R1M3xxFGbiRdwwTjI71w2oWJR%2flXj1xity71r7VIeV%2bbJqrcN543N9RX2kcHeCjM%2bE%2buqbvEw1syT0P5YoNsIyfrxk1oyDJx71FNb7u9d1HB0Y7q5EnNq6KLRqMtjmqzy%2fPzz9atyR4HPSqc%2f8vavTpxitEefU5pJpscHVB1A7mpE1JYhuVxVe4jzbMfesqTKSj6GvJzjHSw8PcW5jh6Kk7Nm%2fLq%2fA2EHvmqdxqLSD%2bErzx61Xt2yn%2bFO2A%2bvTnPavzrFZ9iJ3Tl%2bZ7tPD0%2fZ7HOeJ1ZLlX6ZH%2bNYjrlu9dZ4msPMtFZePLHGa5N5NvHqO3b617GX5pKrTXMzwcVh1GWg3ysHjqetOVNvzD19KI3DHjIPHXvQsmRuxt55rueIv1OLlaZ03hW63R7c13XhybeRXmnhmcxXPQ9cV6H4en8u4j77q97L8R7bDuD3R0S2sdNFDlj8v%2fwBeka33DO36VZtl%2bUfSpfKJPfp6Vj7SzPJnU5ZHKa7pwZz8p%2bbPesV7fbHyPunnnoP84rtNXsPNhbGa5m5tsXBWuySWIw8qL6r8T9JyTFLEYf2b7HN%2bJrQvYxzx5aSE9varmnSCeGNjt5Xk%2bpqyYC6SQ%2f3uRx6ZrK8P5ikkhb70eQCeM4PH%2bfatMrxkq%2bBjf4oaP5f1%2bJ4sk6OIcS9f2vljjpUNt8sgb9a0riATW3uo6is0J5cgXPTvXwefU%2fq%2bM5o7S95fr%2bOp04mzamupu22JYx%2fe7VBfW25jw3I9elLpD7yob1xV%2b7tt6luw6V9fk2OVWin1R87jqd4OJ5J8VtCWe6SUq21k25B6sMkV579n%2bXG057ivc%2fG2h%2f2np00Yba23eCB6dq8f1S0aK%2fOd3z8nIxg1%2bm5Li%2belydj8I4qw3ssQ5rZmSUOfu96DDuXgVcaDLfQ0qW%2bfrXue0PjpVCfQJQSY29Mit21GMVztoht51cfwnp610tquQrduua8%2fFaO56%2bXYrTlZpW6ALxUqwbx39%2fem23KZ%2fSrkMHP1ryJzsetKpeJmXNptH3T0qjdQ5jb0YdK3prfcueelZ81thWXn16VrTqXVj6LhXMPZ11CWzM%2fSXMMKlvvK%2b1h%2fsnpW4sPmQsNucViwL5d%2b0fa4G3Poa29KbdDH%2fe6EfTipqy0ufoOZ3g1VW6MqeMrIeKjrQ1GDy5T79vSqZBLYFVGSaPZpyU4Ka66kcse6Gs2ZcPxkfjWuwxHt%2fGs%2b6j5rooy6HFiY9SkBg8%2fzpUC7%2bKfIvzVG65P1rpONKzOz8H3n2nTmi3AtC3A74P8A9fNatcn4Svfsl%2fH93bKNhJPTJH9a64x5b0%2btfDZzh%2fZ4hy6S1%2fz%2fAMz9R4dxXtsGoveOny6f5fIjOWpvSpGXFNcV48ke6MIzTKkIzTXGDUgMZc0wjBqSmuaTAaeaKD1oqAPMBwq%2fSnhs1EjfLj2p2flrnOw19KvCkdrJ%2fFbzFfwOCM%2fr%2bVe3aLeC%2fwBOhk4Py44P%2bfSvCdFkEiXEOP3kihl%2f4D1%2fnXr3wxk%2b0eGo2k3dcZ9enH619FRq%2b1wa5t4v89b%2fAH3PynPKH1bHNR2f%2fAaXyTt8jqrVd2c%2fw9DV%2bOInpuPYVVsl%2bX5sda39PhWCINjcy9Aex9TXmYipynLT1RRew%2fdfMpVm5%2blZdzB9nHzKynGMGusuLuIsAu7av3i%2bPQ8fyrk9ZuDOzcbWU9uOajC1JSdmVKSpyTuYmtWSzQnt7A5zWFbaSsd621G%2bZehPeugupcoV555NV44VaVsfKQeDXpVaPPTse3h611dFnS7FYVVTuVvQjp0%2f%2bvWnb26l%2bSV2A44zUemW%2fwAmP7zcGtBroRo27OMcAdBXzcsovPVneqztoWLKD7NEAfkZhnk5xVtrlYsKGUBSMAn1%2fwA%2frXO3usLG2FaQAjseD%2btU5Nb3rtGTxn%2fPNejRyuMVoebXxzTseu%2bC%2fiW2hWXkgwMi84Lc0vif4vM8LbRb%2fMP73SvGjrrQ7fQ8j156Y5qC%2b1NnZl3NnkHn2qFw9RdX2kkaf21iHS9nc6XW%2fH8l0z5ERyfX9ax38QtN2XjjiuflZ2k59ep7daSEOjL8ykE84PTBr36eBpQjaJ4eIxFSfxM6XT783EhZtvX161uWr%2bbHnPY5NcnpUmJAvNdPpW5oiqnLZ4rixkOVaBltZc3KypdXmGbotOt5DKcGm6tbeXOx5G7oD2qO3VlkXJ%2blfF080qwxPLN9T6mNNct0PnjweAetVJ4A3Y4rUkhZowOvv2qrPbtgfn9a%2byp1bq6PCrq0ij5f7srzt9RWPqUPkyn6%2bnvXQIuT61n67bFtpGOv515me0%2faYZyXTU5aMuWrYq6aFdv1q75OQ3q3WqFj8rf7vBrUjBcZ7V%2bMY6o4VT3qMuhT1GyF1Zsv%2bzjg1wd1b7J5OPmB%2fOvRireW2AOK4%2fxJpxhumY7drHtXZk%2bO99wPPxkVujEk3htp%2b7kk1FHDyGI59KsMuDQ4yeOlfTe3ueaTabJsvd3bjk9677w5OHlVvl3d%2ba8%2bt%2flkX2Ndj4buNlwg5%2bYcV6uTY7kr8j2lp95M43hddD03TH86Be%2fQcGrohwoxWX4Xm8yID%2bdbsaZ6%2fdr2sR7srHh4hNSKVxb%2bYpU5xiuY1Wy8m4zhvlNdqY8k%2fT8qxdcsSWY9mrTC1rSsfScM4xwq8jOLvYzBdq67uu7msq8thp%2bu%2bZkgSjnPc%2f5JrpNRsiYN3Xae341i%2bJovO0iOVfvQsCSfbJ4%2borHK5eyzGthHtNcyPezmg4yVaJctzkbf7wx0rOvICrFcZ%2bvFXNOu1khVhubaRUutW4iZZvlaNsE1wcRYGdSnGfWLt8n%2fAJMqjQlWhyrfoN0qNnk%2fD8q2JJFEEfI%2bXoM1iXGqpZ2w5%2b7121jXPi1RIeZOP8%2bte9k%2bRyoU9G7nz%2bd82EhzVUbOsyxRs3zgdx3zXk%2fjjTo4tRkaM7lV8g%2bxH%2f166nVNeEjZBkx0%2fwA81gX5%2b0hs%2fMzcZr7XLKMqL5j8D4lxixMnFHM%2bXkd%2femmLnvV77NtJVsblJ5FDW%2f09q%2bi9ofn852KLRY%2fOtzSJTJbhT1Tj61ntBiP%2bH3q3o7eXdD0bisqz5olYTE8lT1NzTj8w%2fLrWnEuR9Ko2kW3uOtatup2KeOmOa8StLU%2bohWGGDP8ACenWqdzZAc%2fNz19q2IotgINQ3NmSG%2b7zWEatmXhcQ6NdSRyOq25hlVhndGwYZ9q0NJlzMy8fNiQfQ807V7U7M%2fLnpmqlvMBFDNzi3cxMO%2bO1d3xR9T9wp1FisHGa7fiaetW3CuM9OlZZXatdJLH9p0rPGVHWufli%2b8GyO9ZUZXVuxrkmI9ph%2bR7xdv8AIjXk1VvYtsnrVxVyQP8A9VR3sWVrppysz0asboyHHzdKjkG339andCD9KbIvy16ETy5KzH2Upznp9a7yzn%2b12ccnH7xQxx64%2fwAa89iyrCux8Gz79MaMt80b55PY%2fwCT%2bdeBn1Hmoqp2f5n1fCeK5cQ6T%2b0vxX9M025prLuqVvvd6jxxXyEj9AGMu2kK7qcwzTazAa4wBTSM056aRigCNhhqKc3PrRUSA8pU4C%2fSnBqjX7y%2fQfyqRfvfhXMd3UtaTOLbUIXLbV3BWP8Asng%2fpXtHw5haw0VoGy2JWwCf5flXh79Pwr3XRf8AkEr%2fALn9TXq4Ft03Hp%2fVv1%2b8%2bC40pKLjV62%2fJ%2f5P8Pu2F1loW24Vty5xjp%2f%2bqpX8XTh2I%2bUHjAJrHm6%2f59abJ%2frB9K7fq8Hq0fCQqzezNZtfuJ1P7xsM2SAajnuZJZW%2bbd7%2fAI9ap2n3v8%2b9Wk%2b8P89zU%2bzjHZGcnJvVkUkfzfN35pLe3Uj1ZT6dasXPUf7tRSdfyqrux9tkuHjOPvF20kJCqG2%2fj0ptzcnGN27IPGOtSQ%2f6qT%2fP8VUl%2fwBXH9BWEdXc%2bshg6aWxT1V2AJONyjkD%2bHr6VlGdopvvkbfRq17%2fAP48n%2bi%2fyNU9N6t%2fuP8A%2bgmu%2bnK0L2Pk81oxhU90gAZwvzbmUcDp2%2f8ArVIImY4%2bbOBlscmhes%2f%2b%2bP51Iv8ArF%2blaSlZnjpkbWwY5Vi3ByPfNEUa5%2b7tx2x%2btSSdf%2bAig9R%2bFHM7HHW3LVmgB68%2bwxXRaA5X8Mc1z9t97%2fgP%2bFbui9Vrz8X8Jy4eo411Ys67bbwrZ7dazFbYf93ge9ber%2f8AHr%2bVYM%2f%2bub%2fPavy7OrwxTkj7zDy5qaZqWZMgC%2bw69qjuEyPp0NO0%2fwD49fwFOuuhr7PJ60quHjKW54uYWjPQz0AD7fbtUOsWyvaEr1HTFWZ%2fvfh%2f7NTJ%2fwDj2%2f4Ca9CrHnoSi%2bzR49Sb5lJHNwNsk2%2bp9eta1k%2b9cZPv71iy%2fwDH5J%2fvH%2bda2lfeP1r8Fz33Z6H0FGTdmWcYfA59s1ieILATbs10E3%2bq%2fGszWujfSvLy7ESjXVisUjiLiDy3II71FsxV3Uv%2bPv8AE%2f0qu3UfSvuIVGeTYZGu3p%2f%2bqui0G4ZVjbHK45rArW8P%2fc%2f4F%2fhW9GtJTUl3Do0eoeE7r96vOfpXXRhQtcJ4S%2b%2fH9BXb2v8AqRX3uL1Sn5Hh4qNncm2cen9aparbq8f0qy33xVW4%2b6fxrnpqzudmTw%2ffqRzt%2fYg7l7NkgetczfBZLKWLb8vXn8q7LUei1xd9%2fr5P9013UaaeLpVuuqP1mODhXwclPojL8L6huVoG6ocA%2buP%2fAK1bmo5u9FmUfejXcuBzx1rk9G%2f5Dsn1H9a7DSerf7p%2fka93M8PCSa7o8zKZWpRqdUcTNqUkyYJOSDkHtWLeTMJt24ith%2f4v9%2f8ApWbqn%2bsr3MvlzU4y7o83xKwkHhOZEIBlT9TUMlvg45FXLf7lR3H3q7oy1sj%2bR8x0kzJ1Gz8qbcPutVfyv%2frVpat%2fx6R%2f7xqq33F%2blddOb5bnyuJ0m7Fcw9vamxBopRjtVtvvL%2bNRf8tPxq1K%2bhwyqNM3LKTzIlb862NObzF6YHvWJo3%2bo%2fGtrSvu%2flXkYjsfS4etJ00y%2bkRbFOntwVoH%2brb8Kmk6V5zk7nTUm7JmHq1mpLDHDc%2fjXPWyYvJrduFuAdvswz%2fSus1T7v4%2f0rlbn%2fkJw%2f8AXcfzr0cPJuJ%2bxcF4idXCOEuhv%2bF7r%2b0NNCt%2fEuMe%2fQ1m6hB5E7Jzwcc1a8F%2f8fL%2fAPXWT%2f0I07xF%2fwAfsn4Uo6VnFHq5XL2eY1aMdmr%2fADTMsLhqJIt8TU7vQPvfga6Ln0sloY80eJKiKbmqze%2f65qjX7v4V3Qk7XPNnFEJh2%2b9bvhG58q%2bWP%2bGUbCP5VjP0rR0T%2fj7h%2bv8AUVhjIqdJwlszqwNR0q8akN1qdcyYH9aZjnFSP0pn8f4V%2bfn62xrLio2GKlfpUbdBSewhvWmtxTqR%2fu1ADD1ooPWilYD%2f2Q%3d%3d"
    # # send_pm_pic(toqq, fromtype=2, img_url='http%3a%2f%2ftiebapic.baidu.com%2fforum%2fw%253D580%253B%2fsign%3dbf4b3d23c61373f0f53f6f9794344afb%2fb21c8701a18b87d649770e47100828381f30fdb5.jpg')
    # after_base = base64.b64encode(b'img_ad.jpg')
    # base_url_encode = parse.quote(after_base)
    # send_pm_pic(1274667113, fromtype=1, path=base_url_encode)
    while 1:
        soup_msg = requests.get('https://api.muxiaoguo.cn/api/tiangourj')
        soup_msg = json.loads(soup_msg.text)['data']['comment']
        print(soup_msg)
        for sp in soup_msg.split('，'):
            print(sp)
            time.sleep(len(sp) * 0.3)
            group_msg(sp, togroup)
        group_msg('[@2097897464]小姐姐, 你理理我啊', togroup)
        print('小姐姐, 你理理我啊')

    # group_msg('http发送群聊!', togroup)
    time.sleep(1)
    # private_msg('http发送私聊test', toqq)
    # time.sleep(1)
    # group_temporary('群临时消息test', toqq, togroup)

    # print(f'{"="*20}处理离线模式下的session内容 可能会有json.loads问题{"="*20}')
    # for i in range(100): # TODO:如何获取旧session序列号?
    #     print(i, end=' ')
    #     getevent(i)
        # geteventv2(i)

    input(f'{"="*20}回车清除session{"="*20}')
    for i in range(100):
        del_buffer(i)
        resetevent(i)

    current_session = input(f'{"="*20}回车建立session{"="*20}')
    if not current_session:
        current_session = get_buffer()
        print('###已建立新session:', current_session)
    else:
        print('###使用已有session:', current_session)

    while 1:
        # get_buffer()
        input('###回车开始监听session内 消息>')
        geteventv2(current_session)

    # while True:
    #     requests.get(get, )
    # auto_accept()
