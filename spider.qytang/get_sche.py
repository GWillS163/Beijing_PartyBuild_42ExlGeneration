import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://qytsystem.qytang.com/accounts/login/?next=/teachers/sec_ccie_clear_rack"

header1 = {
    "Cookie":"Hm_lvt_24b7d5cc1b26f24f256b6869b069278e=1584086880",
    "_qddaz":"QD.262ikh.fvqj7o.k7agwjs0",
    "UM_distinctid":"1709b51fe8896-0883a495068352-71415a3b-14043d-1709b51fe89264",
    "pgv_pvi":"9560422400",
    "__cfduid":"d00d0f55318f8f217e8e81ec9c89c76401584601948",
    "sessionid":"xldds6jpsmvahrt0lxvsvptakf23zh7b",

    }
data ={"csrfmiddlewaretoken":"oj944sonFQE8ZByCnDGOTIIkBwX04byhivUmNSPzXzHEUdBmNQeF7hNhQv7iPiBJ&username=mengjq&password=7Vr.K0s5"
}
token = ''
print("获取首页csrfmiddlewaretoken:")
#获取首页的html，找到验证用的csrfmiddlewaretoken值
try:
    response = requests.get(url,headers=header1)
    token = re.findall(r'name="csrfmiddlewaretoken" value="(.*?)"',response.text)[0]
    print(token)
except:
    print('requests错误！查看报错信息')

header2 = {
    # "username":"mengjq",
    # "password":"7Vr.K0s5",
    'referer':'https://qytsystem.qytang.com/accounts/login/',
    "Hm_lvt_24b7d5cc1b26f24f256b6869b069278e":"1584086880",
    "csrftoken":"eF12MZZBwLWpZ7gR5TlsaewbOZuwjL2B8RMkvpqNOuZVUJjBv6TjoNB83YEO4S53",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
# "_qddaz":"QD.262ikh.fvqj7o.k7agwjs0",
    # "UM_distinctid":"1709b51fe8896-0883a495068352-71415a3b-14043d-1709b51fe89264",
    # "pgv_pvi":"9560422400",
    # "__cfduid":"d00d0f55318f8f217e8e81ec9c89c76401584601948",
    'csrfmiddlewaretoken':token,
    'Content-Type':'csrfmiddlewaretoken=16NZtOkRQLl9iGzYHrn4ZtBf2sbB2l1TViyhceL38uoFdiCI7EVVd2GchrlTNs4l'

}

data = {'Data':"csrfmiddlewaretoken=16NZtOkRQLl9iGzYHrn4ZtBf2sbB2l1TViyhceL38uoFdiCI7EVVd2GchrlTNs4l&username=mengjq&password=7Vr.K0s5"}
#print(header2)
response2 = requests.post(url1,data=data,headers=header2)
print(response2.text)