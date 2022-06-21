import requests
from bs4 import BeautifulSoup
headers = {
    "cookie":" __cfduid=db15419e78b224b618922468dec1f267b1586931747; downloadResolution=Default; _ga=GA1.2.1148830095.1586931750; _gid=GA1.2.1083620007.1586931757; __gads=ID=cd2be79da9cca16d:T=1586931757:S=ALNI_MZTdjyzGuqPBgfle5_1ktnofDmaZg; ai_user=rjqfQ|2020-04-15T06:22:37.370Z; ai_session=XHntx|1586931760585.835|1586931760585.835",
    "user-agent":" Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
}
headers = {
    "cookie":" __cfduid=db15419e78b224b618922468dec1f267b1586931747; downloadResolution=Default; _ga=GA1.2.1148830095.1586931750; _gid=GA1.2.1083620007.1586931757; __gads=ID=cd2be79da9cca16d:T=1586931757:S=ALNI_MZTdjyzGuqPBgfle5_1ktnofDmaZg; ai_user=rjqfQ|2020-04-15T06:22:37.370Z; ai_session=XHntx|1586931760585.835|1586931760585.835",
    "user-agent":" Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
}
def get_detail_link(url,par=None): #喂detaillink ，拉 describe + download。
    page = requests.get(url=url)
    soup = BeautifulSoup(page.text,'html.parser')
    # print("以下是源html" + str(soup))、
    details = soup.select('div.details')[0] #获取 detail信息
    pic_name = soup.select('div.details h1')[0].string

    download = soup.select('div.wallpaperSection')[0] #获取download 信息
    # print(download['href'])
    download_title = download.select('h2')[0].string
    download_des = download.find_all('a')[0].text
    download_link = str(download.select('a')[0]['href']).split('downloadUrl=')[1]
    print(  pic_name,'\n',download_des,'\n',download_title,'\n',download_link)
    return pic_name, download_des, download_title, download_link

# get_detail_link(
# url = "https://wallpaperhub.app/wallpapers/6600"
#       "")

def get_tag_page(tags):
    url = 'https://wallpaperhub.app/wallpapers/?tags=' + str(tags)
    page = requests.get('https://wallpaperhub.app/wallpapers?tags=surface',headers)
    soup = BeautifulSoup(page.text,'html.parser')

    for i in soup.select('div.sc-gZMcBi')[0]:
        href = "https://wallpaperhub.app" + str(i.select('a')[0]['href'])
        h3 = i.select('h3')[0].string
        h4 = i.select('h4')[0].string
        # yield href,h3,h4
        print(href,'\t',h3,'\t',h4)

get_tag_page("office")
#不管爬那哪个页面都是同一个responsed