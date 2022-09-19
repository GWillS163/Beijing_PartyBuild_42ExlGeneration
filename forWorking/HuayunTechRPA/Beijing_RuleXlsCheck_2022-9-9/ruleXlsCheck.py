#  Author : Github: @GWillS163
#  Time: $(Date)
import csv
import os
import re
import time
from typing import List, Any

import xlrd


def findFileByRegex(folderPath, filesRegex):
    files = os.listdir(folderPath)
    return [file for file in files if re.match(filesRegex, file)]


def saveResult2csv(outputFileName, resultList):
    with open(outputFileName, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(resultList)


def getXlsData(banRuleFilePath):
    """得到Xls文件中的数据
    Get the data in the Xls file"""
    workbook = xlrd.open_workbook(banRuleFilePath)
    sheet = workbook.sheet_by_index(0)
    return [sheet.row_values(i) for i in range(1, sheet.nrows)]


def getColNum(colLtr):
    """转换列字母为数字
    Convert Excel column letter to number."""
    num = 0
    for c in colLtr:
        if c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            num = num * 26 + (ord(c) - ord("A"))  # + 1
    return num


def getBannedRuleList(bannedRuleFilePath: str, columnLetter: str) -> list:
    """得到禁止规则文件中的数据
    Get the data in the banned rule file"""
    colNum = getColNum(columnLetter)
    return [data[colNum]
            for data in getXlsData(bannedRuleFilePath)]


def findBannedRule(runningRule: str, banRuleList: list) -> List[str]:
    """比较运行规则和禁止规则
    Compare running rule and banned rule"""
    containBannedRule = []
    for banRule in banRuleList:
        banRule = banRule \
            .replace("《", "").replace("》", "") \
            .replace("(", "（").replace(")", "）")
        # get version that wrap with "《" and "》" in banRule
        banRuleVersion = re.findall(r"（.*?）", banRule)
        # 若有一个规则在禁止规则中，返回True
        if banRule in runningRule:
            containBannedRule.append(banRule)
    return containBannedRule


def compareFileRule(fileData, ruleCol, banRuleList):
    """比较一个文件中的所有规则 返回不符合的规则"""
    result = []
    ruleNum = getColNum(ruleCol)
    for fileRow in fileData:
        res = findBannedRule(fileRow[ruleNum], banRuleList)
        if res:
            bannedRuleFormat = '》,\n《'.join(res)
            result.append([f"《{bannedRuleFormat}》"] + fileRow)
    return result


def main(bannedFilePh, bannedCol, sectUsingFilePh1, sect1Col,
         compUsingFilePh, compCol, sectUsingFilePh, sectCol):
    # files = findFileByRegex(folderPath, filesRegex)
    # allRuleList = []
    # for file in files:
    #     if "~$" in file:
    #         continue
    #     filePath = os.path.join(folderPath, file)
    #     allRuleList.append(getXlsData(filePath))
    runningRuleList = [(sectUsingFilePh1, sect1Col),
                       (compUsingFilePh, compCol),
                       (sectUsingFilePh, sectCol)]
    banRuleList = getBannedRuleList(bannedFilePh, bannedCol)
    result = [["包含的已禁止规则：", "原文"]]
    # 对所有文件的运行中规则进行遍历
    for rulePh, ruleCol in runningRuleList:
        fileData = getXlsData(rulePh)
        # 如果规则在禁用规则中，记录下来所有信息
        result += compareFileRule(fileData, ruleCol, banRuleList)
    # fileName with current timestamp
    fileName = "result_" + str(int(time.time())) + ".csv"
    saveResult2csv(fileName, result)


if __name__ == '__main__':
    bannedFilePath = r"D:\work\北京9.8 - 批量文件关键词检查\制度核查\公司级制度汇编-已废止.xls"
    bannedColName = "E"
    sectUsingFilePath1 = r"D:\work\北京9.8 - 批量文件关键词检查\制度核查\公司级制度汇编-使用中.xls"
    sect1ColName = "C"
    compUsingFilePath = r"D:\work\北京9.8 - 批量文件关键词检查\制度核查\公司级-控措施清单-20220909.xls"
    compColName = "D"
    sectUsingFilePath = r"D:\work\北京9.8 - 批量文件关键词检查\制度核查\部门级-防控措施清单-20220909.xlsx"
    sectColName = "C"
    main(bannedFilePath, bannedColName, sectUsingFilePath1, sect1ColName,
         compUsingFilePath, compColName, sectUsingFilePath, sectColName)
    print("Done!")