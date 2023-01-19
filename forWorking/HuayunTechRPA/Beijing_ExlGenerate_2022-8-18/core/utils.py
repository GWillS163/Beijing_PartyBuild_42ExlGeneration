#  Author : Github: @GWillS163

import csv
# import datetime
# import os.path
import re
import time


def getColLtr(colNum: int) -> str:
    """0 -> A, 1 -> B, 2 -> C, ..., 26->AA, ..., 311 -> KZ
    :param colNum: the Column number of the Column Letter of Excel mappings
    :return the letter of Excel column
    """
    if colNum < 26:
        return chr(colNum + 65)
    else:
        return getColLtr(colNum // 26 - 1) + getColLtr(colNum % 26)


def getColNum(colLtr: str) -> int:
    """A -> 0, B -> 1, C -> 2, ..., AA->26, ..., KZ -> 311
    :param colLtr: the Column Letter of Excel
    :return the sequence number of Excel column
    """
    if len(colLtr) == 1:
        return ord(colLtr) - 65
    else:
        return (ord(colLtr[0]) - 64) * 26 + getColNum(colLtr[1:])


def getTltColRange(titleScope, offsite: int = 0):
    """titleScope : A1:B2, in other words is ColA to Col B
    return iterable Range
    :param titleScope:
    :param offsite: 偏移是为了在放置sht2值时，包含最后一列(默认不包含下界)
    """
    titleStart, titleEnd = titleScope.split(":")
    # get the letter of titleStart by regex
    titleStartLetter = re.findall(r"[A-Z]+", titleStart)[0]
    titleEndLetter = re.findall(r"[A-Z]+", titleEnd)[0]
    # convert to number
    titleStartLetterNum = getColNum(titleStartLetter)
    titleEndLetterNum = getColNum(titleEndLetter)
    titleEndLetterNum += offsite
    return range(titleStartLetterNum, titleEndLetterNum)


def getLineData(allOrgCode):
    """
    获取所有的线数据
    :param allOrgCode:
    :return: {线条: [部门, 部门, ...]}
    """
    lineData = {}
    for lv2 in allOrgCode:
        for lv3 in allOrgCode[lv2]:
            line = allOrgCode[lv2][lv3]["line"]  # 取出每个3级部门的线条
            if line not in lineData:
                lineData.update({line: []})
            lineData[line].append(lv3)
    # for orgName, orgInfo in allOrgCode.items():
    #     if orgInfo["line"] not in lineData:
    #         lineData.update({orgInfo["line"]: [orgName]})
    #         continue
    #     lineData[orgInfo["line"]] += [orgName]
    return lineData


def getAllOrgInfo(orgSht):
    """返回所有的部门代码"""
    lastRow = orgSht.used_range.last_cell.row
    lastCol = orgSht.used_range.last_cell.column
    values = orgSht.range(f"A2:{getColLtr(lastCol)}{lastRow}").value
    allOrgInfo = {}
    for row in values:
        if row[4] not in allOrgInfo:
            allOrgInfo.update({row[4]: {}})  # 上级部门
        allOrgInfo[row[4]] \
            .update({row[0]: {
            "departCode": row[1],
            "level": row[2],
            "line": row[3],
            "staffNum": row[5] if row[5] else 0,  # 人数为空的话则为0
        }})
    print("所有部门代码：", allOrgInfo)
    return allOrgInfo


def countDepartStaffNum(sht1PeopleData: dict, sht1PartyData: dict):
    """
    统计部门人数, 逻辑错误， 这个是参与人数
    :param sht1PeopleData:
    :param sht1PartyData:
    :return:
    """
    departStaffNum = {}

    def addDepartStaffNum(data):
        for lv2 in data:
            if lv2 not in departStaffNum:
                departStaffNum.update({lv2: {}})
            for lv3 in data[lv2]:
                if lv3 not in departStaffNum[lv2]:
                    departStaffNum[lv2].update({lv3: 0})
                departStaffNum[lv2][lv3] += len(data[lv2][lv3])

    addDepartStaffNum(sht1PeopleData)
    addDepartStaffNum(sht1PartyData)

    return departStaffNum


def getSht0DeleteCopiedRowScp(sht2_lv2Score, keywords: list) -> list:
    """
    获得每个单元中间需要删除的区间, keywords开始到结束的区间行
    :param keywords:  关键词列表
    :param sht2_lv2Score:
    :return:
    """
    unitLst = sht2_lv2Score.used_range.value
    rows = 1
    for entireRow in unitLst:
        unit = entireRow[0]
        if unit in keywords:
            break
        rows += 1
    lastRow = sht2_lv2Score.used_range.last_cell.row
    sht0LastValidRow = rows
    return [f"A{lastRow + 1}:A{sht0LastValidRow}  ", sht0LastValidRow]  # f"A32:A52"


def saveDebugLogIfTrue(debugScoreLst, pathPre, debug, debugPath):
    """
    保存debug文件
    save debug file
    :param debug:
    :param debugPath:
    :param debugScoreLst:
    :param pathPre:
    :return:
    """
    saveDebugFile(["name", "questTitle", "quesType", "answer", "rule", "score"],
                  debugScoreLst, debug, debugPath, pathPre)
    # if debug:
    #     print(f"正在保存Debug文件, {debugPath}")
    #     with open(f"{debugPath + pathPre}_{time.strftime('%Y%m%d%H%M%S')}.csv", "w", newline="") as f:
    #         writer = csv.writer(f)
    #         writer.writerows([["name", "questTitle", "quesType", "answer", "rule", "score"]])
    #         writer.writerows(debugScoreLst)


def saveDebugFile(titleLst: list, dataLst, debug, debugPath, pathPre):
    """
    保存debug文件
    save debug file
    :param debug:
    :param debugPath:
    :param titleLst:
    :param dataLst:
    :param pathPre:
    :return:
    """
    if not debug:
        return
    print(f"正在保存Debug文件, {debugPath}")
    with open(f"{debugPath + pathPre}_{time.strftime('%Y%m%d%H%M%S')}.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows([titleLst])
        writer.writerows(dataLst)


def chineseBracket(s: str) -> str:
    """
    将英文括号转换为中文括号
    :param s:
    :return:
    """
    if not s:
        return s
    return s.replace("(", "（").replace(")", "）")


class Stuff:
    def __init__(self, name, lv2Depart, lv2Code, lv3Depart, lv3Code, ID, answerLst=None):
        self.name = name
        self.lv2Depart = chineseBracket(lv2Depart)
        self.lv2Code = lv2Code
        self.lv3Depart = chineseBracket(lv3Depart)
        self.lv3Code = lv3Code
        self.ID = ID
        self.answerLst = answerLst
        self.scoreLst = [None for _ in range(len(answerLst))]

    def __str__(self):
        return f"{self.name} {self.lv2Depart} {self.lv2Code} {self.lv3Depart} {self.lv3Code} {self.ID} {self.answerLst}"

    def __repr__(self):
        return f"{self.name}, answers:{len(self.answerLst)}"  # lv2:{self.lv2Depart[:10]}, lv3:{self.lv3Depart[:10]},


def printAni(strs):
    """
    打印动画
    :param strs:
    :return:
    """
    while True:
        for c in "-\\|/":
            print(f"\r \033[1;36m{c}\033[0m {strs}", end="")
            yield