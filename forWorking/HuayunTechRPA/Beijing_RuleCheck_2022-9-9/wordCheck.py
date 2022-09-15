#  Author : Github: @GWillS163
#  Time: $(Date)
import csv
import os
import re


def wordCheckSimilarity(str1, str2):
    # 1. get the length of the two strings
    len1 = len(str1)
    len2 = len(str2)
    # 2. get the max length of the two strings
    maxLen = max(len1, len2)
    # 3. get the min length of the two strings
    minLen = min(len1, len2)
    # 4. get the similarity of the two strings
    similarity = 1 - (maxLen - minLen) / maxLen
    return similarity


def findFileByRegex(folderPath, filesRegex):
    files = os.listdir(folderPath)
    return [file for file in files if re.match(filesRegex, file)]


def saveResult2csv(outputFileName, resultList):
    with open(outputFileName, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(resultList)


def getFileData(banRuleFilePath):
    """得到文件中的数据"""
    with open(banRuleFilePath, "r", encoding="utf-8") as f:
        banRuleList = f.readlines()
    banRuleList = [rule.strip() for rule in banRuleList]
    return banRuleList


def main(folderPath, filesRegex, banRuleFilePath):
    files = findFileByRegex(folderPath, filesRegex)
    allRuleList = []
    for file in files:
        if "~$" in file:
            continue
        filePath = os.path.join(folderPath, file)
        allRuleList.append(getFileData(filePath))

    banRuleList = getFileData(banRuleFilePath)
    result = []
    # 遍历所有文件的规则
    for rule in allRuleList:
        # 如果规则在禁用规则中，记录下来所有信息
        res = compareRule(rule[2], banRuleList)
        if res:
            result.append(rule)

    saveResult2csv("result.csv", result)


if __name__ == '__main__':
    str1 = "123456"
    str2 = "1234563"
    print(wordCheckSimilarity(str1, str2))