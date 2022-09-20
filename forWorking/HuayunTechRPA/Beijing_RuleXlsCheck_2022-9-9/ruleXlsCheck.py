#  Author : Github: @GWillS163
#  Time: $(Date)
import csv
import os
import re
import time
from typing import List, Any

import xlwings as xw


def findFileByRegex(folderPath, filesRegex):
    files = os.listdir(folderPath)
    return [file for file in files if re.match(filesRegex, file)]


def saveResult2csv(outputFileName, resultList):
    with open(outputFileName, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(resultList)


def getXlsData(app, banRuleFilePath):
    """得到Xls文件中的数据
    Get the data in the Xls file"""
    # workbook = xlwings.Book(banRuleFilePath)
    workbook = app.books.open(banRuleFilePath)
    sheet = workbook.sheets[0]
    # get the last row number
    # lastRow = sheet.range("A1").end("down").row
    # # get the last column number
    # lastCol = sheet.range("A1").end("right").column
    # # get the data in the range
    # data = sheet.range((1, 1), (lastRow, lastCol)).value
    # get all data zone in the sheet
    data = sheet.used_range.value
    workbook.close()
    return data

    # workbook = xlrd.open_workbook(banRuleFilePath)
    # sheet = workbook.sheet_by_index(0)
    # return [sheet.row_values(i) for i in range(1, sheet.nrows)]


def getColNum(colLtr):
    """转换列字母为数字
    Convert Excel column letter to number."""
    num = 0
    for c in colLtr:
        if c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            num = num * 26 + (ord(c) - ord("A"))  # + 1
    return num


def getBannedRuleList(app, bannedRuleFilePath: str, columnLetter: str) -> list:
    """得到禁止规则文件中的数据
    Get the data in the banned rule file"""
    colNum = getColNum(columnLetter)
    return [data[colNum]
            for data in getXlsData(app, bannedRuleFilePath)]


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
        if not fileRow:
            continue
        if not fileRow[ruleNum]:
            continue
        res = findBannedRule(fileRow[ruleNum], banRuleList)
        if res:
            bannedRuleFormat = '》,\n《'.join(res)
            result.append([f"《{bannedRuleFormat}》"] + fileRow)
    return result


def main(savePath, bannedFilePh, bannedCol, sectUsingFilePh1, sect1Col,
         compUsingFilePh, compCol, sectUsingFilePh, sectCol, *args, **kwargs):
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
    app = xw.App(visible=True, add_book=False)
    banRuleList = getBannedRuleList(app, bannedFilePh, bannedCol)
    result = [["包含的已禁止规则：", "原文"]]
    # 对所有文件的运行中规则进行遍历
    for rulePh, ruleCol in runningRuleList:
        if not rulePh or not ruleCol:
            continue
        fileData = getXlsData(app, rulePh)
        # 如果规则在禁用规则中，记录下来所有信息
        result += compareFileRule(fileData, ruleCol, banRuleList)
    app.quit()
    # fileName with current timestamp format "YYYYMMDDHHMMSS"
    fileName = "result_" + time.strftime("%Y%m%d_%H%M%S", time.localtime()) + ".csv"
    savefilePath = os.path.join(savePath, fileName)
    saveResult2csv(savefilePath, result)
    return result


# result = main(savefilePath, bannedFilePath, bannedColName, sectUsingFilePath1, sect1ColName,
#      compUsingFilePath, compColName, sectUsingFilePath, sectColName)
# print("Done!")
