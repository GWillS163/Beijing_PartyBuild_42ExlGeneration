#  Author : Github: @GWillS163
#  Time: $(Date)
import csv
import os
import re
import time
from typing import List, Any

import xlwings as xw


def createFolder(savePath):
    # get current time stamp with yyyyMMddHHmmss
    dtNow = time.strftime("Output_%Y%m%d_%H%M%S", time.localtime())
    savePath = savePath + dtNow + "\\"
    if not os.path.exists(savePath):
        os.makedirs(savePath)
    return savePath

def findFileByRegex(folderPath, filesRegex):
    files = os.listdir(folderPath)
    return [file for file in files if re.match(filesRegex, file)]


def saveResult2csv(outputFileName, methodSuffix, rulePh, resultList):
    if not all(resultList):  # 如果没有则不输出文件
        return
    prefix = ""
    if "使用中" in rulePh:
        prefix = "使用中"
    elif "部门" in rulePh:
        prefix = "部门级"
    elif "公司" in rulePh:
        prefix = "公司级"
    fileName = f"{prefix}检查结果_{methodSuffix}_" + time.strftime("%Y%m%d_%H%M%S", time.localtime()) + ".csv"
    savefilePath = os.path.join(outputFileName, fileName)

    with open(savefilePath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows([["可能包含的已禁止规则：", "原文"]])
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


def findUnPermitRule(runningRuleList, permitRuleListCore):
    """返回permitRuleList中不包含的runningRule规则
    Return the runningRule rules that do not contain the permitRuleList"""
    return [rule for rule in runningRuleList if rule not in permitRuleListCore]


def getBaseRuleList(app, baseRuleFilePath: str, columnLetter: str) -> list:
    """得到基准（现行/废止）规则文件中的数据
    Get the data in the banned rule file"""
    colNum = getColNum(columnLetter)
    return [data[colNum]
            for data in getXlsData(app, baseRuleFilePath)]


def findBannedRule(runningRule: str, banRuleList: list) -> List[str]:
    """被方法2和4使用，返回 runningRule 中包含的 banRuleList 中的规则
    Used by method 2 and 4, return the rules in banRuleList contained in runningRule"""
    # 若有一个规则在禁止规则中，记录返回
    return [banRule for banRule in banRuleList if banRule in runningRule]


def getRunningRule(runningRule: str) -> List[str]:
    """根据正则表达式查找规则
    Find rules by regular expressions"""
    return re.findall(r"《(.*?)》", runningRule)


def isRunningRuleLtVersion(runningRuleV, versionV):
    """判断运行规则的版本号是否小于规则的版本号, 2022-9-26已废弃
    Determine whether the version number of the running rule is less than the version number of the rule"""
    runningRuleVersion = re.findall(r"V(\d{1,3}).(\d{1,3})?.?(\d{1,3})?.?(\d{1,3})?", runningRuleV)
    # get "3.4.2.3" in Version
    version = re.findall(r"(\d{1,3}).(\d{1,3})?.?(\d{1,3})?.?(\d{1,3})?", versionV)
    if not runningRuleVersion or not version:
        return True
    runningRuleVersion = runningRuleVersion[0]
    version = version[0]
    for i in range(len(runningRuleVersion)):
        runR = runningRuleVersion[i]
        verR = version[i]
        if not runR:
            break
        if not verR:
            return False
        # 若运行规则版本号小于规则版本号，返回True
        if int(runR) < int(verR):
            return True
        elif int(runR) == int(verR):
            continue
        else:
            return False


def getXlsColData(app, rulePh, ruleCol):
    """得到规则文件中的规则列数据 - 已废弃
    Get the rule column data in the rule file"""
    colLtr = getColNum(ruleCol)
    return [row[colLtr] for row in getXlsData(app, rulePh)]


def getBannedRuleCore(bannedRule: str) -> str:
    """得到禁止规则的核心部分
    Remove non-coreCode fields from running rules"""
    bannedRuleVersion = re.findall(r"（.*?）", bannedRule)
    if bannedRuleVersion:
        bannedRule = bannedRule.replace(bannedRuleVersion[0], "")
    return bannedRule \
        .replace("中国移动", "") \
        .replace("北京公司", "") \
        .replace("北京有限公司", "") \
        .replace("中国移动通信集团", "") \
        .replace("《", "") \
        .replace("》", "")


def getBannedRuleCoreSimply(bannedRule: str) -> str:
    """简单处理得到禁止规则的核心部分
    Remove non-coreCode fields from running rules"""
    return bannedRule \
        .replace("《", "") \
        .replace("》", "")


def compareMethod1(runningRuleStr, permitRuleList):
    """运行中关键词不更改，比较运行中规则
    # Compare running rule and banned rule"""
    runningRuleList = getRunningRule(runningRuleStr)
    permitRuleListCore = [getBannedRuleCoreSimply(rule) for rule in permitRuleList]
    return findUnPermitRule(runningRuleList, permitRuleListCore)


def compareMethod2(runningRuleStr, bannedRuleList):
    """以核心关键词组合为基准，返回运行中规则中包含的禁止规则
    Compare all rules in a file with coreCode keywords and return hits"""
    baseRuleListCore = [getBannedRuleCore(rule) for rule in bannedRuleList]
    return findBannedRule(runningRuleStr, baseRuleListCore)


def compareMethod3(runningRuleStr, permitRuleList):
    """以核心关键词组合为基准，返回运行中规则中不包含的规则
    Compare all rules in a file with coreCode keywords and return hits"""
    runningRuleList = getRunningRule(runningRuleStr)
    permitRuleListCore = [getBannedRuleCore(rule) for rule in permitRuleList]
    return findUnPermitRule(runningRuleList, permitRuleListCore)


def compareMethod4(runningRuleStr, permitRuleList):
    """比较一个文件中的所有规则 返回不符合的规则
    Compare all rules in a file and return hits"""
    permitRuleListCore = [getBannedRuleCoreSimply(rule) for rule in permitRuleList]
    return findBannedRule(runningRuleStr, permitRuleListCore)


def getFirstCol(involvedBannedRule, method):
    """得到第一列的数据
    Get the first column data"""
    if method == 1 or method == 4:
        bannedRuleFormat = '》,\n《'.join(involvedBannedRule)
        return [f"《{bannedRuleFormat}》"]
    elif method == 2 or method == 3:
        return ["..." + '...,\n...'.join(involvedBannedRule) + "..."]
    else:
        raise Exception("method error, 生成第一列文本时method出错")


def compareMethodMain(runningRuleData, ruleCol, baseRuleList, method=4):
    """比较模块核心
    Compare module coreCode"""
    result = []
    colLtr = getColNum(ruleCol)
    for runningRuleRow in runningRuleData:
        if not runningRuleRow:
            continue
        if not runningRuleRow[colLtr]:
            continue
        if method == 1:  # 规则全名 vs 使用中的规则
            involvedBannedRule = compareMethod1(runningRuleRow[colLtr], baseRuleList)
        elif method == 2:  # 规则核心 vs 废止中的规则
            involvedBannedRule = compareMethod2(runningRuleRow[colLtr], baseRuleList)
        elif method == 3:  # 规则核心 vs 使用中的规则
            involvedBannedRule = compareMethod3(runningRuleRow[colLtr], baseRuleList)
        elif method == 4:  # 规则全名 vs 废止中的规则
            involvedBannedRule = compareMethod4(runningRuleRow[colLtr], baseRuleList)
        else:
            raise Exception("method error, 比较模块核心时method输入出错")
        # 9-22 取消更新
        # if involvedBannedRule:
        #     lowVersion = isRunningRuleLtVersion(runningRuleStr, runningRuleStr[0])
        #     if not lowVersion:
        #         continue
        if not involvedBannedRule:
            continue
        firstCol = getFirstCol(involvedBannedRule, method)
        result.append(firstCol + runningRuleRow)
    return result


def main(savePath, bannedFilePh, bannedCol, permitUsingFilePh, permitCol,
         compUsingFilePh, compCol, sectUsingFilePh, sectCol):
    runningRuleList = [(compUsingFilePh, compCol),
                       (sectUsingFilePh, sectCol)]
    app = xw.App(visible=True, add_book=False)

    banRuleList = getBaseRuleList(app, bannedFilePh, bannedCol)
    permitRuleList = getBaseRuleList(app, permitUsingFilePh, permitCol)

    # 对所有文件的运行中规则进行遍历
    method1 = []  # 现有不变 匹配 使用中文件
    method2 = []  # 去掉前缀 匹配 废止文件
    method3 = []  # 去掉前缀 匹配 使用中文件
    method4 = []  # 现有不变 匹配 废止文件
    for rulePh, ruleCol in runningRuleList:
        if not rulePh or not ruleCol:
            continue
        runningRuleData = getXlsData(app, rulePh)

        result1 = compareMethodMain(runningRuleData, ruleCol, permitRuleList, method=1)
        result2 = compareMethodMain(runningRuleData, ruleCol, banRuleList, method=2)
        result3 = compareMethodMain(runningRuleData, ruleCol, permitRuleList, method=3)
        result4 = compareMethodMain(runningRuleData, ruleCol, banRuleList, method=4)  # 现有规则不变 匹配 废止文件
        method1.extend(result1)
        method2.extend(result2)
        method3.extend(result3)
        method4.extend(result4)
        saveResult2csv(savePath, "1规则全名+不在使用中", rulePh, result1)
        saveResult2csv(savePath, "2规则核心+在已废止中", rulePh, result2)
        saveResult2csv(savePath, "3规则核心+不在使用中", rulePh, result3)
        saveResult2csv(savePath, "4规则全名+在已废止中", rulePh, result4)
    app.quit()
    return method1, method2, method3, method4


stt = time.time()
# savePath = createFolder(savePath)
#
# method1, method2, method3, method4 = main(savePath, bannedFilePath, bannedColName,
#                                           permitUsingFilePath, permitColName,
#                                           compUsingFilePath, compColName, sectUsingFilePath, sectColName)
end = time.time() - stt
# print(method1, method2, method3, method4)
print("Done!", round(end, 3), "s")
