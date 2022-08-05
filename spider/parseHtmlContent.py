# create a function that can requests the url and return the html content
import requests
from bs4 import BeautifulSoup
import re
from pprint import pprint
import csv


if __name__ == '__main__':
    url = input('http:')
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    # print(soup.text)

    dl_lst = soup.select('dl > dl')
    # print(dl_lst)
    n = 0
    for box_n in dl_lst:
        print('n = ', n)
        box = box_n.select('dl > dd p')
        box_link = box_n.select('dl > dd p > a')
        data = {
            "header": box_n.select('dl > dd p')[0].text,
            "describe": box_n.select('dl > dd p')[1].text,
            "Benefit": box_n.select('dl > dd p')[3].text,
            "entrance": re.findall("[\s\S]*href=\"(.*?)\"", str(box_link[0]))[0],
            "support": re.findall("[\s\S]*href=\"(.*?)\"", str(box_link[1]))[0]
        }
        # write data to csv file
        with open('integration.csv', 'a', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=data.keys())
            writer.writerow(data)
        pprint(data)
        n += 1
    # pprint(dl_lst[0].select('dl > dd p'))
