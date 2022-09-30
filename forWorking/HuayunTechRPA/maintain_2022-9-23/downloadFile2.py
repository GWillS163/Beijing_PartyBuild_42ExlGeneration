#  Author : Github: @GWillS163
#  Time: $(Date)

import time
import requests


def getPath(workPath):
    # get current time stamp with yyyyMMddHHmmss
    dtNow = time.strftime("%Y%m%d%H%M%S", time.localtime())
    return workPath+dtNow+".xlsx"


def downloadSave(hrefLink, savePath):
    r = requests.get(hrefLink)
    with open(savePath, "wb") as f:
        f.write(r.content)


def main(workPath, fileLink2):
    savePath = getPath(workPath)
    downloadSave(fileLink2, savePath)
    return savePath


fileLink2 = "https://cdn.educba.com/academy/wp-content/uploads/2020/02/SetAttribute-JavaScript.jpg.webp"
workPath = "D:\\"
savePath = main(workPath, fileLink2)