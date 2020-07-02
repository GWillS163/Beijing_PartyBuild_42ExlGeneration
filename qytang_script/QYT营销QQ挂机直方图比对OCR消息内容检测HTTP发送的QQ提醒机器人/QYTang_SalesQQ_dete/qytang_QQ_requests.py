import requests

'''-----------------------------------------------------'''  # 发送提醒
def message_API():
    data = {
        'change': True,
    }
    url = 'https://qytsystem.qytang.com/sales_qq_monitor/'
    print('-<<[发送提示]>>--',end='')
    res = requests.post(url, json=data)
    print('\t\t' + str(res.json()['status']))

'''-----------------------------------------------------'''  # 发送内容
def send_text(text):
    data = {
        'context': text
    }
    url = 'https://qytsystem.qytang.com/sales_qq_monitor/'
    print('-<<[发送text]>>--', end='')
    #res = requests.post(url, json=data)
    #status = str(res.json()['status'])
    status = text
    print('\t\t' + status)
    n = 0
    if n < 3:
        if status == 'False':
            print('-<<[重试text]>>--', end='')
            #res = requests.post(url, json=data)
            #status = str(res.json()['status'])
            print(str(n) + '\t\t' + status)
            n = n+1
            print('已尝试3次，不发了')
        else:
            print('不重发')
if __name__ == '__main__':
    send_text('False')