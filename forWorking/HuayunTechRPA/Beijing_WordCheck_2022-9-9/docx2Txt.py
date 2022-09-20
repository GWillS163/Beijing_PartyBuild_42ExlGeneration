#  Author : Github: @GWillS163
#  Time: $(Date)

# import a module to read docx files
import os
import re


def findFileByRegex(folderPath, filesRegex):
    """根据正则表达式查找文件"""
    files = os.listdir(folderPath)
    return [file for file in files if re.match(filesRegex, file)]


filesPath = "D:\work\北京9.8 - 批量文件关键词检查"
# find all docx or .doc files
filesRegex = r".*\.(docx|doc)"

res = findFileByRegex(filesPath, filesRegex)
print(res)
