import os
import re
import csv
import time
import datetime
import xlwings as xw
from typing import Any
from typing import List
from typing import Dict
from typing import Union
from typing import Optional
# Github: GWillS163
# User: 駿清清 
# Date: 17/10/2022 
# Time: 17:38

surveyExlPh1013 = r"..\Input\2022-9-27\党建表格输入配置表_2022-10-18.xlsx"
surveyExlPh1111 = r"\Input\2022-11-11\党建表格输入配置表_2022-11-10.xlsx"
surveyExlPh1116 = r"D:\Project\python_scripts\forWorking\HuayunTechRPA\Beijing_ExlGenerate_2022-8-18\Input\2022-11-16\党建表格输入配置表_2022-11-16_样式更改.xlsx"
peopleAnsExlPh0926 = r"..\Input\2022-9-27\220926党建工作成效调研测试问卷--群众.xlsx"
peopleAnsExlPh1103 = r"..\Input\2022-11-3\edited\221101党建工作成效调研测试问卷--群众.xlsx"
peopleAnsExlPh1116 = r"D:\Project\python_scripts\forWorking\HuayunTechRPA\Beijing_ExlGenerate_2022-8-18\Input\2022-11-16\2022年度党建工作成效调研问卷-群众.xlsx"
partyAnsExlPh0926 = r"..\Input\2022-9-27\220926党建工作成效调研测试问卷--党员.xlsx"
partyAnsExlPh1103 = r"..\Input\2022-11-3\edited\221101党建工作成效调研测试问卷--党员.xlsx"
partyAnsExlPh1116 = r"D:\Project\python_scripts\forWorking\HuayunTechRPA\Beijing_ExlGenerate_2022-8-18\Input\2022-11-16\2022年度党建工作成效调研问卷-党员.xlsx"
peopleAnsExlPh1128 = r"D:\work\考核RPA_Exl\Input\2022-11-28_正式\2022年度党建工作成效调研问卷-群众 .xlsx"
partyAnsExlPh1128 = r"D:\work\考核RPA_Exl\Input\2022-11-28_正式\2022年度党建工作成效调研问卷-党员 .xlsx"

# partyAnsExlPh = partyAnsExlPh0926
# peopleAnsExlPh = peopleAnsExlPh0926
# partyAnsExlPh = partyAnsExlPh1103
# peopleAnsExlPh = peopleAnsExlPh1103
# peopleAnsExlPh = peopleAnsExlPh1116
# partyAnsExlPh = partyAnsExlPh1116
peopleAnsExlPh = peopleAnsExlPh1128
partyAnsExlPh = partyAnsExlPh1128
# surveyExlPh = surveyExlPh1111
# surveyExlPh = surveyExlPh1111
surveyExlPh = surveyExlPh1116
isGenDepartments = False

savePath = r"D:\work\考核RPA_Exl\Output"
fileYear = ""
fileName = "PartyBuild"
# surveyTestShtName = "测试问卷"
surveyTestShtName = "2022年调研问卷"
# sht1ModuleName = "调研结果_输出模板"
sht1ModuleName = "二级单位调研结果"
# sht2ModuleName = "调研成绩_输出模板"
sht2ModuleName = "二级单位调研成绩"
# sht3ModuleName = "调研结果（2022年）_输出模板"
sht3ModuleName = "公司整体调研结果"
# sht4ModuleName = "调研成绩（2022年）_输出模板"
sht4ModuleName = "公司整体调研成绩"
# sht1Name = "调研结果"
sht1Name = "二级单位调研结果"
# sht2Name = "调研成绩"
sht2Name = "二级单位调研成绩"
# sht3Name = "调研结果（2022年）"
sht3Name = "公司整体调研结果"
# sht4Name = "调研成绩（2022年）"
sht4Name = "公司整体调研成绩"

# Sheet1 生成配置 : F, G
# sht1IndexScpFromSht0 = "A1:F31"
sht1TitleCopyFromSttCol = "F"
sht1TitleCopyToSttCol = "G"
# Sheet2 生成配置: "C1:J1", "D"
sht2DeleteCopiedColScp = "C1:J1"
sht2MdlTltStt = "D"
# Sheet3 生成配置:  "L", "J", "K"
sht3MdlTltStt = "L"
sht0SurLastCol = "J"
sht3ResTltStt = "K"

# Sheet4 生成配置:
sht4IndexFromMdl4Scp = 'A4:B52'
# sht4TitleFromSht2Scp = 'A1:C17'  # 自动获取， 自动识别
sht4SumTitleFromMdlScp = "T1:U3"

sht1WithLv = {'党委办公室（党群工作部、职能管理部党委）': {'党委工作室': [8.8, 9.4, 7.0, 8.4, 3.33, 9.6, 3.2, 9.4, 7.6, 9.6, 7.8, 8.67, 6.67, 9.0, 7.33, 6.0, 7.2, 6.67, 6.67, 7.33, 5.2, 7.6, 6.4, 9.6, 9.6, 0.0, 0.0, 7.2, 6.2], '党建工作室': [10.0, 10.0, 10.0, 10.0, 2.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 8.89, 8.89, 10.0, 10.0, 0.0, 0.0, 10.0, 10.0], '职能管理部党委办公室': [10.0, 10.0, 10.0, 10.0, 0.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 0.0, 0.0, 10.0, 10.0], '企业文化室': [7.25, 5.0, 8.25, 6.0, 5.0, 7.75, 4.0, 7.75, 8.0, 7.75, 9.5, 7.0, 6.0, 8.0, 8.0, 10.0, 9.5, 9.0, 4.0, 6.0, 7.5, 7.75, 7.0, 8.75, 7.0, 0.0, 0.0, 8.75, 9.25], '青年工作室': [10.0, 1.0, 10.0, 1.0, 0.0, 10.0, 2.0, 10.0, 1.0, 10.0, 0.0, 4.0, 4.0, 10.0, 4.0, 4.0, 6.0, 4.0, 4.0, 4.0, 10.0, 10.0, 10.0, 10.0, 10.0, 0.0, None, 4.0, 10.0], '二级单位': [9.19, 8.48, 8.95, 8.43, 2.5, 9.48, 6.86, 9.43, 8.62, 9.48, 8.9, 8.67, 8.0, 9.42, 8.5, 8.5, 9.05, 8.5, 7.67, 8.17, 8.38, 8.52, 8.1, 9.67, 9.33, 0.0, 0.0, 8.81, 8.95]}}
#  Author : Github: @GWillS163

# import datetime
# import os.path


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
    for orgName, orgInfo in allOrgCode.items():
        if orgInfo["line"] not in lineData:
            lineData.update({orgInfo["line"]: [orgName]})
            continue
        lineData[orgInfo["line"]] += [orgName]
    return lineData


def getAllOrgInfo(orgSht):
    """返回所有的部门代码"""
    lastRow = orgSht.used_range.last_cell.row
    lastCol = orgSht.used_range.last_cell.column
    values = orgSht.range(f"A2:{getColLtr(lastCol)}{lastRow}").value
    allOrgInfo = {}
    for row in values:
        allOrgInfo.update({row[0]: {
            "departCode": row[1],
            "level": row[2],
            "line": row[3],
            "parent": row[4],
            "staffNum": row[5] if row[5] else 0,  # 人数为空的话则为0
        }})
    print("所有部门代码：", allOrgInfo)
    return allOrgInfo


def countDepartStaffNum(sht1PeopleData: dict, sht1PartyData: dict):
    """
    统计部门人数
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
    row = 3
    while True:
        unit = sht2_lv2Score.range(f"A{row}").value
        if unit in keywords:
            break
        row += 1
    lastRow = sht2_lv2Score.used_range.last_cell.row
    sht0LastValidRow = row - 1
    return [f"A{row}:A{lastRow}  ", sht0LastValidRow]  # f"A32:A52"


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
        self.scoreLst = [0 for _ in range(len(answerLst))]

    def __str__(self):
        return f"{self.name} {self.lv2Depart} {self.lv2Code} {self.lv3Depart} {self.lv3Code} {self.ID} {self.answerLst}"

    def __repr__(self):
        return f"{self.name}, answers:{len(self.answerLst)}"  # lv2:{self.lv2Depart[:10]}, lv3:{self.lv3Depart[:10]},
#  Author : Github: @GWillS163
#  Time: 2022-10-1

# Description: 用于计算数据的模块


# import pandas as pd


def listMultipy(lst1, lst2):
    """
    需要考虑None类型 计算会报错
    :param lst1:
    :param lst2:
    :return:
    """
    # 2022-10-20更新, 考虑了None值
    res = []
    for x, y in zip(lst1, lst2):
        if x is None or y is None:
            res.append(None)
            continue
        res.append(round(x * y, 2))
    return res
    # 旧版本，无None值
    # return list(map(lambda x, y: round(x * y, 2), lst1, lst2))


def recordNoneValuePosition(lst):
    """
    记录下None值的位置
    :param lst:
    :return:
    """
    return [i for i in range(len(lst)) if lst(i) is None]


def getMeanScore(stuffScoreLst: list) -> list:
    """
    [[],[]] -> []
    个别None忽略，全为None则为None
    return allLV3.mean() list"""
    if not stuffScoreLst:
        return []
    # get the mean list of stuffScoreLst
    res = []
    for i in range(len(stuffScoreLst[0])):
        # get the mean of each index, exclude the None value
        validLst = [lst[i] for lst in stuffScoreLst if lst[i] is not None]
        cellValue = round(sumWithNone(validLst) / len(validLst), 2) if validLst else None
        res.append(cellValue)
    return res


def getScoreWithLv(staffWithLv):
    """
    从staffWithLv中得到scoreWithLv
    data PreProcess, get the score of each department
    :param staffWithLv: {lv2:{lv3: [[staff], [staff], ...]}}
    :return scoreWithLv: {lv2:{lv3: [[score], [score], ...]}}"""
    scoreWithLv = {}
    for lv2 in staffWithLv:
        scoreWithLv[lv2] = {}
        for lv3 in staffWithLv[lv2]:
            scoreWithLv[lv2][lv3] = [stu.scoreLst for stu in staffWithLv[lv2][lv3]]
    return scoreWithLv


def sht2SumLv1IndexUnitScore(lv3ScoreLst, lv1IndexSpan):
    """
    对一级指标的分数进行求和, 并插入原列表
    :param lv3ScoreLst:[4.2, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    :param lv1IndexSpan: [[0, 8], [9, 14]]
    :return: [4.2, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 【5.65】,
             0.2, 0.5, 0.5, 1.35, 【2.55】,
                                【8.20】]
    """
    if not lv3ScoreLst:
        return []
    res = []
    for unitScp in lv1IndexSpan:  # 每一个单元 - [[0, 6], [7, 10]]
        if not unitScp:
            continue
        unitLst = lv3ScoreLst[unitScp[0]:unitScp[1] + 1]
        res += unitLst  # 加入原单元分数部分
        res.append(sumWithNone(unitLst))  # 加入本单元求和
    res.append(sumWithNone(lv3ScoreLst))
    return res  # 插入总分数


def getSht1WithLv(scoreWithLv: dict) -> dict:
    """
    每个三级部门求平均，及每个二级部门的平均，
    更新：含个别None忽略，全为None则为None
    统计每个二级单位下所有人的分数
    :param scoreWithLv:
    :return:
    """
    sht1WithLv = {}
    for lv2 in scoreWithLv:
        allLv3 = []
        sht1WithLv.update({lv2: {}})

        # 每个三级部门求平均 - get the mean of each lv3
        for lv3 in scoreWithLv[lv2]:
            allLv3 += scoreWithLv[lv2][lv3]
            sht1WithLv[lv2].update({lv3: getMeanScore(scoreWithLv[lv2][lv3])})

        # 每个二级部门的所有人平均 - for each of lv2 unit get the mean score
        allLv3Mean = getMeanScore(allLv3)  #
        sht1WithLv[lv2].update({"二级单位": allLv3Mean})  #
    # 对每个二级单位求平均
    # for lv2 in sht1WithLv:
    #     sht1WithLv[lv2].update({"二级单位": getMeanScore(list(sht1WithLv[lv2].values()))})
    return sht1WithLv


def getLineDepart(lv2, lineData):
    """
    得到当前单位所在的线条 的 所有单位
    :param lv2:
    :param lineData:
    :return:
    """
    for line in lineData:
        if lv2 in lineData[line]:
            return lineData[line]
    return []


def getLineRank(currentUnitScore, lv2, lineData, sht2WithLv, lv2ScoreName="二级单位成绩") -> list:
    """
    计算当前单位在同一线条的排名
    :param lv2ScoreName:
    :param lv2:
    :param sht2WithLv:
    :param lineData:
    :param currentUnitScore: 当前单位分数
    :return: 排名
    """
    # current Line score

    lineDeparts = getLineDepart(lv2, lineData)  # 得到当前单位所在的线条 的 所有单位
    lineScoreLst = []  # 得到当前单位所在的线条 的 所有单位的分数
    for depart in lineDeparts:
        if depart not in sht2WithLv:
            continue
        lineScoreLst.append(sht2WithLv[depart][lv2ScoreName])
    return getListOrderByList(currentUnitScore, lineScoreLst)


def getCompanyRank(currentUnitScore, sht2WithLv, lv2ScoreName="二级单位成绩") -> list:
    """
    计算当前单位在同一公司的排名： 取出所有二级单位的分数，排序，返回当前单位的排名
    :param lv2ScoreName:
    :param currentUnitScore: [4.2, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 4.6, 0.0, 0.0, 0.0, 0.0, 0.0, 4.60]
    :param sht2WithLv:
    :return:
    """
    # CurrentUnitScore 和 下面的对象（所有二级单位的分数）比较
    scoreInLine = [sht2WithLv[lv2][lv2ScoreName] for lv2 in sht2WithLv]
    return getListOrderByList(currentUnitScore, scoreInLine)


def getRidOfDuplicate(allScore):
    """
    去除重复列表
    :param allScore: [1,1,2,3,3]
    :return: [1,2,3]
    """
    return list(set(allScore))


def useDuplicate(allScore):
    """应要求，更新，不去重

    """
    return allScore


def getListOrderByList(currentScore: list, allScore: list) -> list:
    """
    得到currentScore在allScore中每个数字的排名
    :param currentScore: [...]
    :param allScore: [[...], [...], [...]]
    :return: currentScore 在 allScore 中每个数字的排名
    """
    if not allScore:
        return []
    # 去除在allScore里完全相同的分数
    orderRes = [-100 for _ in range(len(allScore[0]))]
    for num in range(len(currentScore)):  # 对每个分数求排名，放入结果
        # 拿到每个单位的第num个分数 - getNumScore(scoreInLine[num], num)
        currNums = [lv2Depart[num] for lv2Depart in allScore]
        # currNumsSorted = getRidOfDuplicate(currNums)
        currNumsSorted = useDuplicate(currNums)
        currNumsSorted.sort(reverse=True)  # Desc
        orderRes[num] = currNumsSorted.index(currentScore[num]) + 1
    return orderRes


def getSht2WithLv(sht1WithLv: dict, lv2UnitSpan: list, lv1IndexSpan: list, lineData: dict) -> dict:
    """
    得到Sheet2中的数据,对指定单元格的分数进行求和 * 权重  以及新增部分求和
    :param lineData:
    :param sht1WithLv: 从sheet1中获取的数据 [1,2,3 ... , 30]
    :param lv2UnitSpan: 二级指标的单元格范围 [ [1,3], [ 4, 8], [20, 30] ]
    :param lv1IndexSpan: 一级指标的单元格范围 [ [1, 3], [7, 10] ]
    :return: sheet2中的数据{lv2:[1, 2, 3, 4, sum, 5, 6, 7, 8, sum, sum]}
    """
    sht2WithLv = {}
    for lv2 in sht1WithLv:
        sht2WithLv.update({lv2: {}})
        for lv3 in sht1WithLv[lv2]:
            title = lv3 if lv3 != "二级单位" else "二级单位成绩"  # Rename
            lv2IndexUnitScore = sumLv2IndexUnitScore(sht1WithLv[lv2][lv3], lv2UnitSpan)
            lv1IndexUnitScore = sht2SumLv1IndexUnitScore(lv2IndexUnitScore, lv1IndexSpan)
            sht2WithLv[lv2].update({title: lv1IndexUnitScore})

    sht2WithLv = addRankForSht2(sht2WithLv, lineData)
    return sht2WithLv


def getSht3WithLv(sht1WithLv: dict, lv1Name: str, lv2Mean) -> dict:
    """得到sheet3中的数据
    从Sheet1 中获取所有二级单位的分数
    """
    sht3WithLv = {}
    allLv2 = []
    for lv2 in sht1WithLv:
        sht3WithLv.update({lv2: sht1WithLv[lv2][lv2Mean]})
        allLv2.append(sht1WithLv[lv2][lv2Mean])
    allLv2Mean = getMeanScore(allLv2)
    sht3WithLv.update({lv1Name: allLv2Mean})
    return sht3WithLv


def addRankForSht4(sht4WithLv):
    """
    一类分公司	城区一分公司 // 统计此
                城区二分公司 // 统计此
                城区三分公司 // 统计此
                平均分
    :param sht4WithLv:
    :return:
    """

    def getLineScores(lineDepart):
        """
        得到线条内的所有分数
        :param lineDepart:
        :return:
        """
        res = list(lineDepart[lv2][-1] for lv2 in lineDepart.keys() if lv2 != "平均分")
        # return getRidOfDuplicate(res)
        return useDuplicate(res)

    def getLineRanks(shtWithLv):
        """
        获得添加线条内排名
        :param shtWithLv:
        :return: {lv2: 3rd, v: 2nd}
        """
        ranksLine = {}
        for lne in shtWithLv:
            ranksLine[lne] = {}
            lv2All = getLineScores(shtWithLv[lne])
            lv2All.sort(reverse=True)
            for lv2 in shtWithLv[lne]:
                if lv2 == "平均分":
                    continue
                if lv2 not in ranksLine[lne]:
                    ranksLine[lne].update({lv2: None})
                assert shtWithLv[lne][lv2][-1] in lv2All
                lineRank = lv2All.index(shtWithLv[lne][lv2][-1]) + 1
                # lineDepart[lv2].append(lineRank)  # [原分数, +排名]
                ranksLine[lne].update({lv2: lineRank})  # {原分数: +排名}
        return ranksLine

    def getAllDepartScore(shtWithLv):
        """
        获取所有二级部门的分数 - get all lv2 depart score
        :param shtWithLv:
        :return:
        """
        allDepartScore = []
        for lne in shtWithLv:
            for l2 in shtWithLv[lne]:
                if l2 == "平均分":
                    continue
                allDepartScore.append(shtWithLv[lne][l2][-1])
        # return getRidOfDuplicate(allDepartScore)
        return useDuplicate(allDepartScore)

    def getAllDepartRank(shtWithLv) -> dict:
        """
        获取所有二级部门的排名 - get all lv2 depart rank
        :return:
        """
        allDepartsRank = {}
        allDepart = getAllDepartScore(shtWithLv)
        allDepart.sort(reverse=True)
        for lne in shtWithLv:
            if lne not in allDepartsRank:
                allDepartsRank.update({lne: {}})
            for lv2 in shtWithLv[lne]:
                if lv2 == "平均分":
                    continue
                if lv2 not in allDepartsRank[lne]:
                    # 添加排序后的排名 - add rank after sort
                    whichRank = allDepart.index(shtWithLv[lne][lv2][-1]) + 1
                    allDepartsRank[lne].update({lv2: whichRank})

        return allDepartsRank

    def addRanks2Sht4(sht4WithLvs, ranksSht4WithLvs, allDepartRanks):
        """
        将全公司排名添加到sht4WithLv中
        :param sht4WithLvs:
        :param ranksSht4WithLvs:
        :param allDepartRanks:
        :return:
        """
        for lne in sht4WithLvs:
            for lv2 in sht4WithLvs[lne]:
                if lv2 == "平均分":
                    continue
                sht4WithLvs[lne][lv2].append(ranksSht4WithLvs[lne][lv2])
                sht4WithLvs[lne][lv2].append(allDepartRanks[lne][lv2])
        return sht4WithLvs

    # 每个线条内添加排名
    ranksSht4WithLv = getLineRanks(sht4WithLv)
    # 全公司排名 - the rank of all departments
    allDepartRank = getAllDepartRank(sht4WithLv)
    return addRanks2Sht4(sht4WithLv, ranksSht4WithLv, allDepartRank)


def getSht4WithLv(sht2WithLv: dict, sht4Hierarchy: list, lv1Name: str) -> dict:
    """得到sheet4中的数据
    单独获取 二级单位成绩 按分类求和
    :param lv1Name:
    :param sht2WithLv: {lv2: {lv3: [0.9, 0.4, 0.0, 1.1, 1.0, 1.15, 1.1, 5.65, 0.2, 0.5, 0.5, 1.35, 2.55, 8.2]}}
    :param sht4Hierarchy:  [["一类分公司","城区一分公司"]...
                            ["二类分公司","城区二分公司"]]
    :return: {"一类分公司": {"城区一分公司": [0.9, 2.3, ...],
                                       "平均分": [0.9, 2.3, ...]},
                                        ... ...
                           "北京公司":{"平均分": [0.9, 2.3, ...]}} }
    """
    sht4WithLv = {}
    allLv2 = []
    # 对每个二级单位放入sht4WithLv 每个分类中
    for lv2 in sht2WithLv:
        # get lv2depart class
        currClass = getSht4Class(lv2, sht4Hierarchy)
        # print(currClass)
        if not currClass:
            continue
        if not currClass[0] in sht4WithLv:
            sht4WithLv.update({currClass[0]: {}})
        if not currClass[1] in sht4WithLv[currClass[0]]:
            sht4WithLv[currClass[0]].update({currClass[1]:
                                                 sht2WithLv[lv2]['二级单位成绩']})
        allLv2.append(sht2WithLv[lv2]['二级单位成绩'])

    # 对每个部门分类求平均分
    for class_lv2 in sht4WithLv:
        sht4WithLv[class_lv2].update({"平均分": getMeanScore(list(sht4WithLv[class_lv2].values()))})
    # 北京公司平均分： 对所有二级单位求平均分
    sht4WithLv.update({lv1Name: {"平均分": getMeanScore(allLv2)}})
    return addRankForSht4(sht4WithLv)


def getSht4Class(lv2, sht4Hie):
    """获取二级单位所属的分类"""
    for class_lv2 in sht4Hie:
        if lv2 == class_lv2[1]:
            return class_lv2
    return None


def getSht4Hierarchy(sht4):
    """
    获得Sheet4的层级
    Get the hierarchy of sheet4
    :param sht4:
    :return:
    """
    raw_depart = sht4.range("A4:B50").value
    clazz = None
    sht4Hie = []
    for row in raw_depart:
        if row[0]:
            clazz = row[0]
        if row[1] == "平均分":
            continue
        sht4Hie.append([clazz, row[1].strip("\n") if row[1] else None])
    return sht4Hie


def resetUnitSum(sht, sht2UnitScp, weightCol):
    """
    重置Sheet2中的单元格权重 = 与其他几个单元格的和
    reset the weight of sheet2 equal to the sum of other cells
    :param sht:
    :param sht2UnitScp: [2, 4], [7, 10]
    :param weightCol:
    :return:
    """
    for unit in sht2UnitScp:
        cellSum = 0
        for edge in range(unit[0], unit[1] + 1):
            weight = sht.range(f"{weightCol}{edge}").value
            try:
                assert type(weight) == float or type(weight) == int
            except Exception as e:
                print("weight is not int:", e)
                weight = 0
            # print(f"\t 获得单元格值:{weightCol}{edge} = {weight} get value of weightCell: ")
            cellSum += weight
        # print(f"求和放至首格：{weightCol}{unit[0]}={cellSum} - place the sum to the first cell of the unit\n")
        sht.range(f"{weightCol}{unit[0]}").value = cellSum


def getSht2DeleteRowLst(sht2UnitScp: list) -> List[int]:
    """
    获取需要删除的行号, 仅保留每个单元内的第一行
    get the row num of the rows that need to be deleted, only keep the first row in the unit
    :param sht2UnitScp:
    :return:
    """
    sht2DeleteRowLst = []
    for eachUnitScp in sht2UnitScp:
        if len(eachUnitScp) == 1:
            continue
        for eachCell in range(eachUnitScp[0] + 1, eachUnitScp[1] + 1):
            sht2DeleteRowLst.append(eachCell)  # 除了第一行，其他行都需要删除
    return sht2DeleteRowLst


def getShtUnitScp(sht, startRow: int, endRow: int, unitCol: str, contentCol: str,
                  skipCol=None, skipWords=None) -> List[List[int]]:
    """
    以contentCol列为最小单位，获取每个unitCol列二级指标的单元范围
    跳过党廉 and 纪检 part
    :return:  [[0, 0], [1, 2], [3, 3], [4, 5] ...
    """
    # get merge cells scope dynamically
    if skipWords is None:
        skipWords = []
    resultSpan = []
    tempScp = [-1, -1]
    n = 0
    while n < endRow:
        row = startRow + n
        if skipCol:
            part = sht.range(f"{skipCol}{row}").value
            # detect skip words if part equal skip words, thus skip this row
            if part in skipWords:
                n += 1
                continue
        unit = sht.range(f"{unitCol}{row}").value
        content = sht.range(f"{contentCol}{row}").value
        if not content:  # 若无内容，则结束流程 - end the process if no content
            resultSpan.append(tempScp)
            break

        if unit:  # 若有单元值则是新的单元 - new unit if unit value exist
            if tempScp != [-1, -1]:  # 如果是新的单元，则将上一个单元的范围加入结果 - add the scope of last unit to result
                resultSpan.append(tempScp)
            tempScp = [n, n]  # 设定新单元的范围 - set the scope of new unit
        else:
            tempScp[1] = n  # 更新单元的范围 - update the scope of unit
        n += 1
    assert resultSpan != [[-1, -1]]  # 断言结果不为空 - assert the result is not empty
    return resultSpan


def getDeptUnit(shtModule, scp, offsite: int) -> Dict[Optional[Any], List[Union[int, str, None]]]:
    """
    获取分类的区间，以便裁剪sheet
    {分类: ["F", "P"], ... }
    :param shtModule:
    :param scp:
    :param offsite:
    :return:"""
    clsScp = {}
    titleRan = getTltColRange(scp, offsite)
    clazz = [-1, -1]
    lastClz = None
    lastLtr = None
    for colNum in titleRan:
        colLtr = getColLtr(colNum)
        cls = shtModule.range(f"{colLtr}1").value
        lv2 = shtModule.range(f"{colLtr}2").value
        # print(cls, lv2)
        if not lv2 and not cls:
            break
        if cls:
            if lastLtr:
                clazz[1] = lastLtr
                assert clazz[0] != -1  # 不能有未找到的值
                clsScp.update({lastClz: clazz})
                clazz = [-1, -1]
            clazz[0] = colLtr
            lastClz = cls
        lastLtr = colLtr
    clazz[1] = lastLtr
    clsScp.update({lastClz: clazz})
    return clsScp


def sumLv2IndexUnitScore(lv3ScoreLst: list, lv2Unit: list):
    """
    计算核心合并单元的分数
    [0, 1,2,3,4,5,6] & [0,1],[2,4],[6,6] * [0.2, 0.3, 0.5]
    -> [0+1, 2+4, 6]
    : params lv3ScoreLst: 分数序列（多少个问题就有多少个分数）
    : params lv2Unit: 分数求和范围（单元格范围）
    : return
    """
    if not lv3ScoreLst:
        return []
    res = []
    for unitScp in lv2Unit:  # 添加每个单元的分数
        if unitScp[0] == unitScp[1]:  # 若单元只有一个单元格，则直接添加分数
            # unit=[28, 28], but score list length is 28
            try:
                res.append(lv3ScoreLst[unitScp[0]])
            except IndexError:
                res.append(0)
            continue
        endBound = unitScp[1] + 1
        if endBound > len(lv3ScoreLst):
            endBound = len(lv3ScoreLst)
        res.append(  # 若单元有多个单元格，则求和
            sumWithNone(lv3ScoreLst[unitScp[0]:endBound]))
    return res


def sumWithNone(lst):
    """
    处理包含None值的 列表求和
    :param lst:
    :return:
    """
    return sum([validNum for validNum in lst if validNum is not None])


def getSht2WgtLst(sht2_lv2Score) -> list:
    """
    获取Sheet2中的权重列表
    :param sht2_lv2Score:
    :return:
    """
    # 通过权重计算得到sht2WithLv
    sht2WgtLstScp = "C3:C" + str(sht2_lv2Score.used_range.last_cell.row)
    sht2WgtLst = sht2_lv2Score.range(sht2WgtLstScp).value
    # # pop掉最后一个空值 - pop out the last empty value
    # for i in range(len(sht2WgtLst) - 1, -1, -1):
    #     if sht2WgtLst[i] is None:
    #         sht2WgtLst.pop(i)
    return sht2WgtLst


def getSht1WgtLst(sht1_lv2Result, sht0_survey, questionCol: str) -> List[int]:
    """
    获取Sheet1中的权重列表
    :param sht0_survey:
    :param questionCol: 问题所在列：K
    :param sht1_lv2Result:
    :return:
    """
    # 通过权重计算得到sht2WithLv
    sht1WgtLstScp = f"{questionCol}3:{questionCol}" + str(sht1_lv2Result.used_range.last_cell.row)
    sht0WgtLst = sht0_survey.range(sht1WgtLstScp).value
    # # pop掉最后一个空值 - pop out the last empty value
    # for i in range(len(sht2WgtLst) - 1, -1, -1):
    #     if sht2WgtLst[i] is None:
    #         sht2WgtLst.pop(i)
    return sht0WgtLst


def addSht1Wgt2Sht1WithLv(sht1WithLv, sht1WgtLst: List[int]):
    """
    为每个lv2 下的lv3 添加权重
    :param sht1WithLv:  {lv2: {lv3: [score]}}
    :param sht1WgtLst:  [wgt, wgt, ...]
    :return:
    """
    # sht1WithLvWgt = {}
    for lv2 in sht1WithLv:
        for lv3 in sht1WithLv[lv2]:
            sht1WithLv[lv2][lv3] = listMultipy(sht1WithLv[lv2][lv3], sht1WgtLst)
    return sht1WithLv


def clacSheet2_surveyGrade(sht1_lv2Result, sht0_survey, questionCol, sht1WithLv, lv1UnitScp, departCode):
    """
    通过sht1的值 与 权重， 计算sheet2的分数。 原数据[1,2..., 30]
    calculate the score of the sht2_lv2Score
    :param sht0_survey:
    :param departCode:
    :param lv1UnitScp:
    :param sht1_lv2Result: sheet1
    :param questionCol: 问题所在列：K
    :param sht1WithLv:
    :return:
    """

    print("开始计算sheet2数据，准备获取页面值")
    # sht2WgtLst = getSht2WgtLst(sht2_lv2Score)
    # print(f"获得 sht2 权重: {sht2WgtLst}, weight")
    sht1WgtLst = getSht1WgtLst(sht1_lv2Result, sht0_survey, questionCol)
    print(f"获得 sht1 权重: {sht1WgtLst}, weight")
    assert None not in sht1WgtLst, "权重列表中存在空值"
    sht1WithLvWgt = addSht1Wgt2Sht1WithLv(sht1WithLv, sht1WgtLst)
    lv2UnitSpan = getShtUnitScp(sht1_lv2Result, startRow=3, endRow=40,
                                unitCol="B", contentCol="D",
                                skipCol="A", skipWords=["党廉", "纪检"])
    # lv1UnitSpan = getShtUnitScp(sht2_lv2Score, startRow=3, endRow=40,
    #                             unitCol="A", contentCol="B")
    lineData = getLineData(departCode)
    sht2WithLv = getSht2WithLv(sht1WithLvWgt, lv2UnitSpan, lv1UnitScp, lineData)
    return sht2WithLv


def addRankForSht2(sht2WithLv, lineData, lv2ScoreName="二级单位成绩"):
    """为第二个sheet添加本线条排名，全公司排名

    """

    for lv2 in sht2WithLv:
        # 拿出每个二级单位成绩，去线条里比较
        currentUnitScore = sht2WithLv[lv2][lv2ScoreName]
        # 比较
        sht2WithLv[lv2].update({"本线条排名": getLineRank(currentUnitScore, lv2, lineData, sht2WithLv, lv2ScoreName)})
        sht2WithLv[lv2].update({"全公司排名": getCompanyRank(currentUnitScore, sht2WithLv, lv2ScoreName)})

    return sht2WithLv


# 2022-11-11 更新 增加参与率计算
def calcParticipateRatioCore(parts, staffs) -> list:
    """计算参与率"""
    if parts is None or staffs is None or parts == 0 or staffs == 0:
        return [0, 0, "0.00%"]
    return [staffs, parts, f"{parts / staffs:.2%}"]


def getBasicParticipates(allStaffNum: dict, orgInfo: dict, lv2Mean, lv1Str):
    """
    计算所有部门参与率
    :param lv2Mean: 二级部门
    :param allStaffNum:  { lv2 : {lv3: 33, lv3 : 2}}
    :param orgInfo:  { lv2/lv3 : {staffNum: 0}}
    :return:
    """
    basicParticipates = {}

    def getDepartStaffNum(LV2, LV3):
        if LV3 in orgInfo:
            return orgInfo[LV3]["staffNum"]
        elif LV2 in orgInfo:
            return orgInfo[LV2]["staffNum"]
        print(f"未找到 {LV2} 或 {LV3} 的人数")
        return 0

    def getParticipatesData(LV2: str, LV3: str):
        participates = allStaffNum[LV2][LV3]  # 本部门参与人数
        allStaff = getDepartStaffNum(LV2, LV3)  # 本部门总人数
        return calcParticipateRatioCore(participates, allStaff)  # 本部门参与率

    allPartsNums = 0
    allStaffNums = 0
    for lv2 in allStaffNum:
        basicParticipates[lv2] = {}
        lv2PartsSum = 0
        lv2StaffSum = 0
        for lv3 in allStaffNum[lv2]:
            staffs, parts, ratio = getParticipatesData(lv2, lv3)
            basicParticipates[lv2].update({lv3: getParticipatesData(lv2, lv3)})
            lv2PartsSum += parts
            lv2StaffSum += staffs
        basicParticipates[lv2].update({lv2Mean: calcParticipateRatioCore(lv2PartsSum, lv2StaffSum)})
        allPartsNums += lv2PartsSum
        allStaffNums += lv2StaffSum
    basicParticipates.update({lv1Str: calcParticipateRatioCore(allPartsNums, allStaffNums)})
    return basicParticipates


def combineShtRatioCore(shtWithLvOri, basicRatio):
    """
    将参与率数据合并到shtWithLv中
    :param shtWithLvOri:
    :param basicRatio:
    :return:
    """
    # hard copy shtWithLv
    shtWithLv = {}
    defaultRatio = [None, None, None]
    for lv2 in shtWithLvOri:
        shtWithLv[lv2] = {}
        isExists = lv2 in basicRatio
        for lv3 in shtWithLvOri[lv2]:
            isExists = lv3 in basicRatio[lv2] if isExists else False
            # 对所有三级单位新增参与率部分。没有值则为空
            extendRatio = basicRatio[lv2][lv3] if isExists else defaultRatio
            shtWithLv[lv2][lv3] = extendRatio + shtWithLvOri[lv2][lv3]

    return shtWithLv


def combineSht1Ratio(sht1WithLv, basicParticipateRatio):
    return combineShtRatioCore(sht1WithLv, basicParticipateRatio)


def combineSht2Ratio(sht2WithLv, basicParticipateRatio):
    return combineShtRatioCore(sht2WithLv, basicParticipateRatio)


def combineShtRatioCore2(shtWithLv, basicRatio, lv2MeanStr, lv1Str):
    """
    将参与率数据合并到sht3WithLv中
    :param shtWithLv:
    :param basicRatio:
    :param lv2MeanStr: "二级单位"字段
    :return:
    """
    defaultRatio = [None, None, None]
    newShtWithLv = {}
    lv1AllParts = 0
    for lv2 in shtWithLv:
        if lv2 == lv1Str:
            newShtWithLv[lv1Str] = basicRatio[lv1Str] + shtWithLv[lv1Str]
            continue
        # 对所有三级单位新增参与率部分。没有值则为空
        extendRatio = basicRatio[lv2][lv2MeanStr] if lv2 in basicRatio else defaultRatio
        newShtWithLv[lv2] = extendRatio + shtWithLv[lv2]
        lv1AllParts += extendRatio[1] if extendRatio[1] else 0
    return newShtWithLv


def combineSht3Ratio(sht3WithLv, basicRatio, lv2MeanStr, lv1Str):
    return combineShtRatioCore2(sht3WithLv, basicRatio, lv2MeanStr, lv1Str)


def getLv2Class(lv2, sht4Hie):
    """
    获取二级单位的类别
    """
    for row in sht4Hie:
        if lv2 == row[1]:
            return row[0]
    return ""


def turnSht4Ratio(basicRatio, sht4Hie, lv1Str, lv2Mean):
    """
     转换为sht4格式的参与率数据。
    : basicRatio: 基础参与率数据 ： {城区一分公司:{综合部, 市场部}, 城区二分公司: {网络部, ..} }
    : sht4Hie:[['分公司', '城区一分公司'] ['分公司', '城区二分公司']...]
    :
    : return {分公司:{城区一分公司，城区二分公司}, 北京公司:{平均分}}
    """
    meanStr = "平均分"
    sht4Ratio = {}
    for lv2 in basicRatio:  # 拿出来每个lv2的总数
        if lv2 == lv1Str:
            continue
        lv2Class = getLv2Class(lv2, sht4Hie)
        if lv2Class not in sht4Ratio:
            sht4Ratio[lv2Class] = {}
        if lv2 not in sht4Ratio:
            sht4Ratio[lv2Class][lv2] = {}

        sht4Ratio[lv2Class].update({lv2: basicRatio[lv2][lv2Mean]})

    # 新增每个分类的总数, 分公司的平均分
    for lv2Class in sht4Ratio:
        lv2ClassParts = []
        lv2ClassStaffs = []
        for lv2 in sht4Ratio[lv2Class]:
            lv2ClassParts.append(sht4Ratio[lv2Class][lv2][0])
            lv2ClassStaffs.append(sht4Ratio[lv2Class][lv2][1])
        # 新增每个lv2Class的 汇总值
        sht4Ratio[lv2Class].update({meanStr: calcParticipateRatioCore(
            sum(lv2ClassStaffs),
            sum(lv2ClassParts)
        )})
    # 一级单位 北京的平均分
    sht4Ratio.update({lv1Str: {}})
    sht4Ratio[lv1Str].update({meanStr: basicRatio[lv1Str]})

    return sht4Ratio


def combineSht4Ratio(sht4WithLv, sht4Ratio, lv2MeanStr, lv1Str):
    """
    将参与率数据合并到sht4WithLv中
    """
    meanStr = "平均分"
    defaultRatio = [None, None, None]
    newShtWithLv = {}
    for lv2Class in sht4WithLv:
        if lv2Class == lv1Str:
            newShtWithLv.update({lv1Str: {meanStr: []}})
            newShtWithLv[lv1Str][meanStr] = sht4Ratio[lv1Str][meanStr] + sht4WithLv[lv1Str][meanStr]
            continue
        for lv2 in sht4WithLv[lv2Class]:
            if lv2 == lv1Str:
                # 取出来basicRatio的平均分
                newShtWithLv.update({lv1Str: {meanStr: []}})
                newShtWithLv[lv1Str][meanStr] = sht4Ratio[lv1Str][meanStr] + sht4WithLv[lv1Str][meanStr]
                continue
            ratioLst = sht4Ratio[lv2Class][lv2] if lv2Class in sht4Ratio and lv2 in sht4Ratio[lv2Class] \
                else defaultRatio
            if lv2Class not in newShtWithLv:
                newShtWithLv[lv2Class] = {}
            if lv2 not in newShtWithLv[lv2Class]:
                newShtWithLv[lv2Class][lv2] = []
            newShtWithLv[lv2Class][lv2] = ratioLst + sht4WithLv[lv2Class][lv2]
            # lv1AllParts += ratioLst[1] if ratioLst[1] else 0
    return newShtWithLv


def getSht3Ratio(basicParticipateRatio: dict, lv1Name, lv2Mean: str) -> dict:
    lv1Parts = 0
    lv1Staffs = 0
    sht3Ratio = {}
    for lv2 in basicParticipateRatio:
        for lv3 in basicParticipateRatio[lv2]:
            if lv3 == lv2Mean:
                sht3Ratio.update({lv2: basicParticipateRatio[lv2][lv2Mean]})
                continue
            lv1Parts += basicParticipateRatio[lv2][lv3][0]
            lv1Staffs += basicParticipateRatio[lv2][lv3][1]
    sht3Ratio.update({lv1Name:  # [lv1Parts, lv1Staffs,
                                calcParticipateRatioCore(lv1Parts, lv1Staffs)
                      # ]
                      })
    return sht3Ratio
#
#
# if __name__ == '__main__':
#     basicRatio = {'党委办公室': {'党委工作室': [5.0, 5, '100.00%'], '党建工作室': [5.0, 9, '180.00%'], '职能管理部党委办公室': [4.0, 2, '50.00%'], '企业文化室': [3.0, 4, '133.33%'], '青年工作室': [2.0, 1, '50.00%'], '二级单位': [21, 19.0, '90.48%']}}
#     sht1WithLv = {'党委办公室': {
#                         '党委工作室': [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, -1.0, 10.0, 10.0,
#                                   0.0, 10.0, 10.0, 10.0, 10.0, 10.0, 0.0, 10.0, 10.0, 10.0, 10.0, 10.0],
#                         '党建工作室': [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, -1.0, 10.0,
#                                        10.0, 0.0, 10.0, 10.0, 10.0, 10.0, 10.0, 0.0, 10.0, 10.0, 10.0, 10.0, 10.0],
#                         '1级单位': [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, -1.0, 10.0, 10.0,
#                                  0.0, 10.0, 10.0, 10.0, 10.0, 10.0, 0.0, 10.0, 10.0, 10.0, 10.0]},
#          }
#     res = combineSht1Ratio(sht1WithLv, basicRatio)
#     from pprint import pprint
#     pprint(res)
#
#     print(sht1WithLv == res)
#  Author : Github: @GWillS163
# Description: 用于 添加数据，增加行列


def shtCopyTo(sht1, sht1Scp, sht2, sht2Start):
    """
    将sht1中的数据复制到sht2中
    copy data and format from sht1 to sht2
    :param sht1:
    :param sht1Scp:
    :param sht2:
    :param sht2Start:
    :return:
    """
    # sht1.activate()
    if not sht1.range(sht1Scp).value:
        print(f"\t{sht1.name} - {sht1Scp} - 无数据")
        return
    sht1.range(sht1Scp).api.Copy()
    # judge whether clipboard is empty
    # retry 3 times
    error = None
    for _ in range(3):
        try:
            sht2.activate()
            sht2.range(sht2Start).api.Select()
            sht2.api.Paste()
            # sht2.range(sht2Start).api.PasteSpecial(
            #     Paste=-4163, Operation=2, SkipBlanks=False, Transpose=False)
            return
        except Exception as e:
            error = e
            print(f"\t{sht1.name} - {sht1Scp} - 复制失败 - {error}")
            time.sleep(0.3)
            continue  # 总是会报错，不知道为什么pywintypes.com_error: (-2147352567, 'Exception occurred.', (0, 'Microsoft Excel',
    raise error


def getLastColCell(sht):
    """
    获取标题行的起始单元格
    :param sht:
    :return:
    """
    print("   自动获取标题粘贴起点 - ",
          end="")
    lastColNum = sht.used_range.last_cell.column  # 这个封装好了， 稳定
    # lastColNum = sht.range("A1").end("right").column  # 这个遇到空值会失效， 这个直观
    shtTitleCopyTo = f"{getColLtr(lastColNum)}1"
    print(f"{sht.name} - {shtTitleCopyTo}")
    return shtTitleCopyTo


def getLastRowCell(sht):
    print("   自动获取sht4标题粘贴起点 -",
          end="")
    lastRowNum = sht.used_range.last_cell.row  # 这个封装好了， 稳定
    # lastColNum = sht.range("A1").end("right").column  # 这个遇到空值会失效， 这个直观
    lastCell = f"A{lastRowNum + 1}"
    print(f"[{sht.name}] - {lastCell}")
    return lastCell


def sht2AddSummary(sht2_lv2Score, sht2WithLv, row, startCol, endCol):
    """
    为Sheet2 添加合计行
    :param sht2_lv2Score:
    :param sht2WithLv:
    :param row:
    :param startCol:
    :param endCol:
    :return:
    """
    unitScoreSum = 0
    while True:
        unit = sht2_lv2Score.range(f"A{row}").value
        unitScoreSum += sht2_lv2Score.range(f"{startCol}{row - 1}").value
        if unit:
            break
    sht2_lv2Score.range(f"{startCol}{row}").value = unitScoreSum


def addUnitScpOffsite(unitScp: list, offsite: int = 2) -> list:
    """
    为unitScp添加偏移量
    :param offsite: 默认2 是包含标题行
    :param unitScp:
    :return:
    """
    return [[node + offsite for node in unit] for unit in unitScp]


def sht2OprAddSummaryRows(sht2_lv2Score, unitScp: list):
    """
    为Sheet2 添加合计行
    add summary rows to sheet2
    :param sht2_lv2Score:
    :param unitScp:
    :return:
    """
    unitScpOffsite = addUnitScpOffsite(unitScp, 3)
    sumStr = ",".join([f"C{unitScp[0]}:C{unitScp[1]}" for unitScp in unitScpOffsite])
    endRow = unitScpOffsite[-1][-1] + 1  # 最后一行 - last row
    sht2_lv2Score.range(f"A{endRow}").api.EntireRow.Insert()
    sht2_lv2Score.range(f"B{endRow}").value = "总计"
    sht2_lv2Score.range(f"C{endRow}").value = f"=SUM({sumStr})"

    # 为Sheet2 添加合计行 - add summary rows to sheet2
    while unitScpOffsite:
        unit = unitScpOffsite.pop()
        insertRow = unit[-1] + 1
        sht2_lv2Score.range(f"B{insertRow}").api.EntireRow.Insert()
        sht2_lv2Score.range(f"B{insertRow}").value = "合计"
        sht2_lv2Score.range(f"C{insertRow}").value = f"=SUM(C{unit[0]}:C{unit[-1]})"

    # insertRow = []
    # for row in range(4, 20):
    #     unit = sht2_lv2Score.range(f"A{row}").value
    #     ques = sht2_lv2Score.range(f"B{row}").value
    #     if not ques:
    #         if not unit:
    #             insertRow.append(row)
    #             break
    #         continue
    #     if unit:
    #         insertRow.append(row)
    #
    # endRow = insertRow[-1]
    # # 增加每单元的合计行 - add summary for each unit
    # sumForAll = []
    # while insertRow:
    #     row = insertRow.pop()
    #     sht2_lv2Score.range(f"A{row}").api.EntireRow.Insert()
    #     sht2_lv2Score.range(f"B{row}").value = "合计"
    #     unitSumScp = fillSht2UnitSumLineHor(sht2_lv2Score, row, "C")
    #     sumForAll.append(unitSumScp)
    #     # 以下代码不需计算其他列的合计
    #     # sht2CalcSummary(sht2_lv2Score, sht2WithLv, row, "C", "L")
    # sht2_lv2Score.range(f"C{endRow}").value = f"=SUM({','.join(sumForAll)})"


def fillSht2UnitSumLineHor(sht2, summaryRow: int, sumCol: str, unitCol="A") -> str:
    """
    负责每个单元横向填充 的“合计” 及 求和权重，目前只需填充一列2022-10-1
    responsible for filling one line of summary and summing up the weight
    :param unitCol: 用来判断单元格大小
    :param sumCol: "D:L"
    :param summaryRow:
    :param sht2:"""
    # 获得最上面的范围 - get unit top scope
    unitRow = summaryRow
    while True:
        unitRow -= 1
        if sht2.range(f"{unitCol}{unitRow}").value:
            break
    # 单列填充 - Fill one Line
    unitScp = f"{sumCol}{unitRow}:{sumCol}{summaryRow - 1}"
    sht2.range(f"{sumCol}{summaryRow}").value = f"=SUM({unitScp})"
    return unitScp
    # 横向填充 - Fill one Line
    # fillRan = getTltColRange(sumCol)
    # for colNum in fillRan:
    #     colLtr = getColLtr(colNum)
    #     unitScp = f"{colLtr}{unitRow}:{colLtr}{summaryRow - 1}"
    #     sht2.range(f"{colLtr}{summaryRow}").value = f"=SUM({unitScp})"


def sht1SetData(sht1_lv2Result, sht1WithLv, titleRan):
    """
    Sheet1 中，纵向放入 每个lv2_3部门的数据(如果有) 包含“二级单位”
    :param titleRan:
    :param sht1_lv2Result:
    :param sht1WithLv:
    :return: None
    """
    lv2 = None
    n = 0
    for colNum in titleRan:
        n += 1
        colLtr = getColLtr(colNum)
        curLv2 = sht1_lv2Result.range(f"{colLtr}1").value
        lv3 = sht1_lv2Result.range(f"{colLtr}2").value
        if curLv2:
            lv2 = curLv2
        if not lv3:
            continue
        if lv2 not in sht1WithLv:
            continue
        if lv3 not in sht1WithLv[lv2]:
            continue
        # print(f"{lv2} & {lv3} exists")
        print(f"Sheet1 Progress:{n}/{len(titleRan)} - [{lv2}-{lv3}]")  # , end="\r")
        sht1_lv2Result.range(f"{colLtr}3"). \
            options(transpose=True).value = sht1WithLv[lv2][lv3]
    print("Sheet1 Progress:100% - [Done]")


def sht2SetData(sht2_lv2Score, sht2WithLv, titleRan: range):
    """
    Sheet2 中，纵向放入 每个lv3部门的数据(如果有) * 该lv3部门的权重
    :param titleRan: Range
    :param sht2_lv2Score:
    :param sht2WithLv:
    :return:
    """
    lv2 = None
    n = 0
    for colNum in titleRan:
        n += 1
        colLtr = getColLtr(colNum)
        curLv2 = sht2_lv2Score.range(f"{colLtr}1").value
        lv3 = sht2_lv2Score.range(f"{colLtr}2").value
        if curLv2:
            lv2 = curLv2
        if not lv3:
            continue
        if lv2 not in sht2WithLv:
            continue
        if lv3 not in sht2WithLv[lv2]:
            continue
        # print(f"{lv2} & {lv3} exists")
        print(f"Sheet2 Progress:{n}/{len(titleRan)} - [{lv2}-{lv3}]")  # , end="\r")
        sht2_lv2Score.range(f"{colLtr}3") \
            .options(transpose=True).value = sht2WithLv[lv2][lv3]
    print("Sheet2 Progress:100% - [Done]")


def sht3SetData(sht3, sht3WithLv: dict, titleRange: str, lv1Name: str):
    """
    Sheet3 中，纵向放入 每个lv2部门的数据(如果有)
    :param lv1Name:
    :param sht3:
    :param sht3WithLv:
    :param titleRange:
    :param lv1Name: 默认是 北京公司
    :return:
    """
    titleRan = getTltColRange(titleRange)
    # lv2Clz = None
    n = 0
    for col in titleRan:
        n += 1
        colLtr = getColLtr(col)
        lv2UpCurr = sht3.range(f"{colLtr}1").value
        lv2 = sht3.range(f"{colLtr}2").value
        # if lv2UpCurr:
        if lv2UpCurr == lv1Name:
            sht3.range(f"{colLtr}3").options(transpose=True).value = sht3WithLv[lv1Name]
        # lv2Clz = lv2UpCurr
        if not lv2 in sht3WithLv:
            continue
        # place score list vertically
        print(f"Sheet3 Progress:{n}/{len(titleRan)} - [{lv2UpCurr}-{lv2}]")  # , end="\r")
        sht3.range(f"{colLtr}3").options(transpose=True).value = sht3WithLv[lv2]
    print("Sheet3 Progress:100% - [Done]")


def sht4SetData(sht4, sht4WithLv, titleRan, lv1Name):
    """
    Sheet4 中，横放入 每个lv2部门的数据(如果有)
    :param lv1Name:
    :param sht4:
    :param sht4WithLv:
    :param titleRan:
    :return:
    """
    lv1 = None
    for row in titleRan:
        lv1Curr = sht4.range(f"A{row}").value
        lv2 = sht4.range(f"B{row}").value
        if lv1Curr:
            if lv1Curr == lv1Name:
                sht4.range(f"C{row}").value = sht4WithLv[lv1Name]
            lv1 = lv1Curr
        if not lv1 in sht4WithLv:
            continue
        if not lv2 in sht4WithLv[lv1]:
            continue
        # place score list vertically,  row object of type 'int' has no len()
        sht4.range(f"C{row}").value = sht4WithLv[lv1][lv2]
    print("Sheet4 Progress:100% - [Done]")


def addOneDptData(shtSum, scpLst, height,
                  shtDept, shtTitleTo):
    """
    粘贴一个部门的数据从 sht1Sum 到 sht1Dept
    :param shtDept:
    :param height:
    :param scpLst:
    :param shtTitleTo:
    :param shtSum:
    :param  从模板表中复制的部门范围
    :return:
    """
    # 数据栏 复制
    sht1BorderL, sht1BorderR = scpLst  # deptUnitSht1[deptName]
    sht1DataZone = f"{sht1BorderL}1:{sht1BorderR}{height}"
    # shtDept.activate()
    # pywintypes.com_error: (-2147352567, 'Exception occurred.', (0, None, None, None, 0, -2146827284), None)
    shtCopyTo(shtSum, sht1DataZone,
              shtDept, shtTitleTo)
    return sht1BorderL, sht1BorderR


def getUnitScpRowList(sht, unitCol: str, baseCol: str, keywords: list) -> list:
    """
    找到关键词单位的范围, 多个单元必须是一片连续的范围
    :param sht: sheet
    :param unitCol: 单元列，用来识别关键词
    :param baseCol: 基准列
    :param keywords: 单元的关键词
    :return: [int, int]
    """
    res = [-1, -1]
    lastUnit = None
    lastRow = sht.used_range.last_cell.row + 1
    for row in range(0, lastRow):
        unit = sht.range(f"{unitCol}{row}").value
        base = sht.range(f"{baseCol}{row}").value
        if unit or not base:
            if lastUnit in keywords:
                res[1] = row
            break
        if unit in keywords:
            res[0] = row
            lastUnit = unit
    return res


def dltOneDptData(shtDept, shtTitleCopyTo, deptCopyHeight, shtBorderL, shtBorderR):
    """
    删除部门数据，用于重新填入
    :param shtDept:
    :param shtTitleCopyTo:
    :param deptCopyHeight:
    :param shtBorderR:
    :param shtBorderL:
    :return:
    """
    borderWidth = getColNum(shtBorderR) - getColNum(shtBorderL)
    borderStart = getColNum(shtTitleCopyTo[0])
    borderEnd = getColLtr(borderStart + borderWidth)
    shtDept.range(f"{shtTitleCopyTo}:{borderEnd}{deptCopyHeight}").api.Delete()


def getRuleByQuestionSurvey(name, questTitle, surveyTestSht, surveyQuesCol, surveyRuleCol):
    """

    # 找到所属规则 - locate which row is rule by questTitle in scoreExl
    :param name:
    :param questTitle:
    :param surveyTestSht:
    :param surveyQuesCol: 问题所在列
    :param surveyRuleCol:
    :return:
    """
    answerRow = -1
    for row in range(3, 40):
        # find the cell in the surveyExl by Question column
        ruleQuest = surveyTestSht.range(f"{surveyQuesCol}{row}").value
        if ruleQuest is None:
            continue
        if ruleQuest in questTitle:
            # print("Check_cellQuestion: ", ruleQuest)
            answerRow = row
            break
    if answerRow == -1:
        print(f"{name} [not found]: {questTitle}")
        return answerRow, None
    # get rule in the surveyExl App
    rule = surveyTestSht.range(f"{surveyRuleCol}{answerRow}").value
    return answerRow, rule


def getRuleByQuestionList( questTitle, surveyDataList):
    """
    读取到内存加速判断
    # 找到所属规则 - locate which row is rule by questTitle in scoreExl
    :param questTitle:
    :param surveyDataList:
    :return:
    """
    for row in surveyDataList:
        # find the cell in the surveyExl by Question column
        ruleQuest = row[0]  # 问题所在列
        if not ruleQuest:
            continue
        if ruleQuest.strip() in questTitle:
            return row[1], row[2]  # 类型， 规则

    return None, None


# 2022-11-16 更新内容: 新增参与率等

# placeBar 函数更改的部分 ： 新增了参与率三个单元格
# placeData 部分： 在插入数据的时候，将参与率的数据插入进去
def genericAddParticipateRatio(mdlSht, partitionRowScp, sht, insertPoint):
    # insert 3 rows in sht1
    sht.range(insertPoint).api.EntireRow.Insert()
    sht.range(insertPoint).api.EntireRow.Insert()
    sht.range(insertPoint).api.EntireRow.Insert()
    shtCopyTo(mdlSht, partitionRowScp,  sht, insertPoint)

    # # entire row copy and paste
    # mdlSht1.range(partitionRowScp).api.EntireRow.Copy()
    # # paste
    # sht1.range(insertPoint).api.EntireRow.PasteSpecial(Paste=-4163)


def sht1OprAddPartRatio(mdlSht1, partitionRowScp, sht1, insertPoint="A3"):
    """
    在 sht1 中插入参与率
    :param mdlSht1:
    :param partitionRowScp:
    :param sht1:
    :param insertPoint:
    :return:
    """
    genericAddParticipateRatio(mdlSht1, partitionRowScp, sht1, insertPoint)


def sht2OprAddPartRatio(mdl1Sht2, participateRowScp, sht2, insertPoint="A3"):
    """
    在 sht2 中插入参与率
    :param mdl1Sht2:
    :param participateRowScp:
    :param sht2:
    :param insertPoint:
    :return:
    """

    genericAddParticipateRatio(mdl1Sht2, participateRowScp, sht2, insertPoint)


def sht3OprAddPartRatio(mdl1Sht3, participateRowScp, sht3, insertPoint="A3"):
    """
    在 sht3 中插入参与率
    :param mdl1Sht3:
    :param participateRowScp:
    :param sht3:
    :param insertPoint:
    :return:
    """
    genericAddParticipateRatio(mdl1Sht3, participateRowScp, sht3, insertPoint)#  Author : Github: @GWillS163
#  Time: $(Date)


def judgeGradeSingle(answerIntLst, ruleSelect, ruleScore):
    # 1分:1
    # 2.2分
    # 9:9分
    # 10.10分
    if len(answerIntLst) != 1:
        # print("识别到的数字不止一个，请检查！", end="")
        # print(debugPrint)
        return -100

    # get the number in ruleSelect by regex
    numOfRuleDig = re.search(r"(\d{,3})([-|或])?(\d{,3})?", ruleSelect).groups()
    if not numOfRuleDig[1]:  # only one number
        if answerIntLst[0] == int(numOfRuleDig[0]):
            return ruleScore
    else:  # present scope or "或"
        if numOfRuleDig[1] == "或":
            if answerIntLst[0] == int(numOfRuleDig[0]) or answerIntLst[0] == int(numOfRuleDig[2]):
                return ruleScore
        elif numOfRuleDig[1] == "-":
            if int(numOfRuleDig[0]) <= answerIntLst[0] <= int(numOfRuleDig[2]):
                return ruleScore

    return -100


def judgeGradeMulti(answerIntLst, ruleSelect, ruleScore):
    # 已覆盖效果 (2022-8-29)
    # 单个选择: 10分：4
    # 单个任意: 10分：4或5
    # 全部选择: 8分：全选
    # 局部全选: 8分：1-4
    # 局部全选: 0分：1-4全选
    # 全局多选: 任选3个
    # 局部多选: 1-4任选3个
    # 局部多选以上: 1-4任选3个及以上

    # 识别效果(下行为标题):
    # 单选，4或5, 选择范围开始, 选择范围结束, 全选，任选，n个，n个及以上
    # ('4', None, None, None, None, None, None, None)
    # (None, '4或5', None, None, None, None, None, None)
    # (None, '4或5或20', None, None, None, None, None, None)
    # (None, None, None, None, '全选', None, None, None)
    # (None, None, '1', '4', None, None, None, None)
    # (None, None, '1', '4', '全选', None, None, None)
    # (None, None, None, None, None, '任选', '3', None)
    # (None, None, '1', '4', None, '任选', '3', None)
    # (None, None, '1', '4', None, '任选', '3', '及以上')

    # write a regex to identify above case
    scopeRan = re.search(
        r"(^\d{,3})$|(^\d{,3}(?:或\d{,3})+$)|(?:^(\d{,3})-(\d{,3}))?(?:(全选)|(任选)(\d{,3})-?(\d{,3})?个)?(及以上)?",
        ruleSelect).groups()
    sglSlt, dblSlts, permitNumStart, permitNumEnd, isAllSlt, isAnySlt, permitQtyMin, permitQtyMax, isMore = scopeRan

    # 判断是否在允许范围 judge each score if is not in permit scope
    if not permitNumStart and not permitNumEnd:
        permitNumStart, permitNumEnd = 1, 99  # default
        validAns = answerIntLst
    else:
        validAns = []
        permitScp = range(int(permitNumStart), int(permitNumEnd) + 1)
        for num in answerIntLst:
            if int(num) in permitScp:
                validAns.append(num)
        validAns = list(set(validAns))

    # e.g. 单个选择的规则: 4
    if sglSlt and len(validAns) == 1:
        if validAns[0] == int(sglSlt):
            return ruleScore

    # 单个任选: e.g. 4或5, 一旦选了就给分
    elif dblSlts:
        permitNumLst = list(map(int, dblSlts.split("或")))
        # check some element of the answerIntLst is duplicate with permitNumLst
        for num in validAns:
            if int(num) in permitNumLst:
                return ruleScore

    # 全部选择与部分全选:
    # e.g. 全选, 1-5, 1-5全选  (默认1-99)
    elif isAllSlt or (not isAllSlt and not isAnySlt):
        # return "多选 或部分全选"
        if not permitNumStart and permitNumEnd:
            print("全部选择与部分全选，需要指定范围！")
            return -100
        # 选择的数量与范围一致
        if len(validAns) == len(range(int(permitNumStart), int(permitNumEnd) + 1)):
            return ruleScore

    # 局部  (默认1-99)
    # 全局多选: 任选3个
    # 局部多选: 1-4任选3个
    # 局部多选: 1-4任选3-4个
    # 局部多选以上: 1-4任选3个及以上
    elif isAnySlt:
        # 判断数量是否足够
        # 匹配两种格式： 任选n(-m)个及以上
        if not permitQtyMax:
            permitQtyMax = permitQtyMin

        # 任选n个及以上
        if isMore:
            if len(validAns) >= int(permitQtyMin):
                return ruleScore
        # 任选n(-m)个
        else:
            if int(permitQtyMin) <= len(validAns) <= int(permitQtyMax):
                return ruleScore

    return -100


def judgeRulePreProcess(ruleP, debugPrint):
    ruleL, ruleR = 0, 0
    for char in [':', "：", "."]:
        if char in ruleP:
            ruleL, ruleR = ruleP.split(char)
            break

    if not (ruleL and ruleR):
        print("没有找到匹配的分隔字符，将处理为-100分 :")
        print(debugPrint)
        return -100, -100

    # get permit scope
    if "分" in ruleL:
        ruleScore = int(ruleL.strip("分"))
        ruleSelect = ruleR
    elif "分" in ruleR:
        ruleScore = int(ruleR.strip("分"))
        ruleSelect = ruleL
    else:
        print("无法分辨哪边是分数! 将处理为-100分 :", debugPrint)
        return -100, -100

    return ruleScore, ruleSelect


def judgeAnswerGrade(answer, rule, quesType):
    debugPrint = f"\tanswer: {answer}\n" \
                 f"\trule: {rule}\n" \
                 f"\tquesType: {quesType}"
    # 如果能直接匹配分数则返回 - match the number of digital in answer by regex, form is a number+分
    answerInt = re.findall(r"(\d{,3}?)分", answer.strip())
    if answerInt and answerInt[0]:
        return int(answerInt[0])

    if "开放题" in quesType:
        return 0
    elif "评分题" in quesType:
        return int(re.search(r"\d{0,3}", answer.strip()).group(0))

    # get RuleL & RuleR and verify
    answerIntStr = re.findall(r"(\d{1,3})\..*?", answer)
    assert answerIntStr, "answer is not a number, please check the answer"
    answerIntLstDup = list(map(int, answerIntStr))
    answerIntLst = list(set(answerIntLstDup))
    # check each rule to answer
    for ruleP in rule.split("\n"):
        if not ruleP:
            continue
        ruleScore, ruleSelect = judgeRulePreProcess(ruleP, debugPrint)
        if ruleScore == -100 or ruleSelect == -100:
            continue

        # get answer scope with different type of ques
        score = -100
        if "单项" in quesType or "单选" in quesType:
            score = judgeGradeSingle(answerIntLst, ruleSelect, ruleScore)
        elif "不定项" in quesType:
            score = judgeGradeMulti(answerIntLst, ruleSelect, ruleScore)
        if score != -100:
            return score
    return -100
# Github: GWillS163
# User: 駿清清 
# Date: 12/10/2022 
# Time: 12:47

def printShtWithLv(shtName, shtWithLv):
    """
    print the sheet with level
    :param shtName:
    :param shtWithLv:
    :return:
    """
    for lv2 in shtWithLv:
        for lv3 in shtWithLv[lv2]:
            try:
                newName = shtName[:4]
                newLv2 = lv2[:4]
                newLv3 = lv3[:4]
            except Exception as e:
                newName = shtName
                newLv2 = lv2
                newLv3 = lv3 + str(e)
            print(f"{newName}-[{newLv2}]\t[{newLv3}]:{shtWithLv[lv2][lv3]}")


def printSht1Data(typ, staffWithLv, scoreExlTitle):
    print("staffWithLv:", staffWithLv)
    print("scoreExlTitle:", scoreExlTitle)
    print(f"{typ}分数：")
    # print(stuffWithLv) all score


def printLv2Lv3(lv2Lv3Dict: dict, additionalInfo: str = ""):
    for lv2 in lv2Lv3Dict:
        for lv3 in lv2Lv3Dict[lv2]:
            print(f"[{additionalInfo}] - [{lv2}][{lv3}]： {lv2Lv3Dict[lv2][lv3]}")


def printSht1WithLv(sht1WIthLv):
    """
    输出Sht1WithLv
    :param sht1WIthLv:
    :return:
    """
    for lv2 in sht1WIthLv:
        for lv3 in sht1WIthLv[lv2]:
            print(f"[{lv2}][{lv3}] - {sht1WIthLv[lv2][lv3]}")


def printStaffWithLv(staffWithLv):
    for lv2 in staffWithLv:
        for lv3 in staffWithLv[lv2]:
            for stu in staffWithLv[lv2][lv3]:
                print(stu.name, stu.scoreLst)


def printScoreBugIf(answer, rule, questTitle, quesType, stuff, questionNum):
    if stuff.scoreLst[questionNum] == -100:
        print(f"answer: {answer}\n"
              f"rule: {rule}\n"
              f"questTitle: {questTitle}\n"
              f"quesType: {quesType}\n"
              f"score: {stuff.scoreLst[questionNum]}")


def printAutoParamSht1(sht1TitleCopyFromMdlScp, sht1DeptTltRan, sht1DataColRan):
    print("Sheet1 获取sheet1页填充范围数据 - I. get sheet data")
    print(f"\t从sht1模板这里复制:sht1TitleCopyFromMdlScp: {sht1TitleCopyFromMdlScp}")
    print(f"\tsht1模板标题至: sht1DeptTltRan: {sht1DeptTltRan}")
    print(f"\t数据列范围：sht1DataColRan: {sht1DataColRan}")


def printAutoParamSht2(sht2DeleteCopiedColScp, sht2TitleCopyFromMdlScp,
                       sht2DeptTltRan, sht2IndexCopyFromSvyScp, sht2IndexCopyTo):
    print(f"Sheet2 自Sht2模板自动获取的参数如下: ")
    print(f"\tsht2DeleteCopiedColScp: {sht2DeleteCopiedColScp}")
    print(f"\tsht2TitleCopyFromMdlScp: {sht2TitleCopyFromMdlScp}")
    print(f"\tsht2DeptTltRan: {sht2DeptTltRan}")
    print(f"\tsht2IndexCopyFromSvyScp: {sht2IndexCopyFromSvyScp}")
    print(f"\tsht2IndexCopyTo: {sht2IndexCopyTo}")


def printAutoParamSht3(sht3IndexCopyFromSvyScp, sht3DataColRan, sht3TitleCopyFromMdlScp):
    print(f"Sheet3 自Sht3模板自动获取的参数如下: ")
    print(f"\tsht3IndexCopyFromSvyScp: {sht3IndexCopyFromSvyScp}")
    print(f"\tsht3DataColRan: {sht3DataColRan}")
    print(f"\tsht3TitleCopyFromMdlScp: {sht3TitleCopyFromMdlScp}")


def printAutoParamSht4(sht4IndexFromSht2Scp, sht4SumTitleFromMdlScp,
                       ):
    print(f"Sheet4 自Sht4模板自动获取的参数如下: ")
    print(f"\tsht4IndexFromSht2Scp: {sht4IndexFromSht2Scp}")
    # print(f"\tsht4TitleFromSht2Scp: {sht4TitleFromSht2Scp}")
    print(f"\tsht4SumTitleFromMdlScp: {sht4SumTitleFromMdlScp}")
    # print(f"\tsht4DataRowRan: {sht4DataRowRan}")
# Github: GWillS163
# User: 駿清清 
# Date: 06/10/2022 
# Time: 20:57


def combineMain(questLst, peopleQuestLst, sht1People, partyQuestLst, sht1Party, debugPath):
    """
    依照统计表的答案顺序，将问卷的答案按照顺序排列，没有则为0.
    :param questLst: 统计结果表的答案顺序
    :param peopleQuestLst: 问题顺序
    :param sht1People: sht1PeopleData {lv2: {lv3: [[scoreLst], [scoreLst], ...]}}
    :param partyQuestLst:  问题顺序
    :param sht1Party:sht1PartyData {lv2: {lv3: [[scoreLst], [scoreLst], ...]}}
    :return: sht1WithLv
    """
    # 得到答案的顺序 - get order of answer
    partyOrderLst = []
    peopleOrderLst = []
    for quest in questLst:
        if quest is None:
            continue
        quest = quest.strip()
        peopleIndex = getMappingIndex(quest, peopleQuestLst)
        partyIndex = getMappingIndex(quest, partyQuestLst)
        peopleOrderLst.append(peopleIndex)
        partyOrderLst.append(partyIndex)
    sortDebug(questLst, peopleOrderLst, partyOrderLst, partyQuestLst, peopleQuestLst, debugPath, debug=True)

    # 依照统计表的答案顺序，将sht1WithLv整形
    sht1WithLvPeople = reformatSht1WithLv(sht1People, peopleOrderLst)
    sht1WithLvParty = reformatSht1WithLv(sht1Party, partyOrderLst)
    sht1WithLvCombine = lastCombination(sht1WithLvPeople, sht1WithLvParty)
    return getSht1WithLv(sht1WithLvCombine)


def reformatSht1WithLv(sht1WithLv, orderLst):
    """
    每个人都按照orderLst的顺序进行排序, 没有则是None
    :param sht1WithLv:
    :param orderLst:  -100 是没有对应分数的
    :return:
    """
    for lv2 in sht1WithLv.keys():
        for lv3 in sht1WithLv[lv2].keys():
            lv3Scores = []
            for lv3StaffScore in sht1WithLv[lv2][lv3]:  # lv3 部门的所有人都按照orderLst的顺序进行摘选
                # 找不到对应的题目，处理为None
                lv3Scores.append([lv3StaffScore[i] if i != -1 else None for i in orderLst])
            sht1WithLv[lv2][lv3] = lv3Scores
    return sht1WithLv


def lastCombination(sht1WithLvPeople, sht1WithLvParty):
    """
    将people 与 party 结合起来。
    :param sht1WithLvPeople: {lv2: {lv3:[[scoreLst], [scoreLst]]}}
    :param sht1WithLvParty: {lv2: {lv3:[[scoreLst], [scoreLst]]}}
    :return: {lv2: {lv3:[[scoreLst], [scoreLst]]}}
    """
    sumSht1WithLv = sht1WithLvPeople.copy()
    # 对于每一个党员的二级单位进行处理 - for each lv2 of party
    for lv2 in sht1WithLvParty.keys():
        if lv2 not in sumSht1WithLv.keys():
            sumSht1WithLv.update({lv2: sht1WithLvParty[lv2]})
            continue
        # 对于每一个党员的三级单位进行处理 - for each lv3 of party
        for lv3 in sht1WithLvParty[lv2].keys():
            if lv3 not in sumSht1WithLv[lv2].keys():
                sumSht1WithLv[lv2].update({lv3: sht1WithLvParty[lv2][lv3]})
                continue
            # 如果有相同lv3 -  if lv3 is same
            sumSht1WithLv[lv2][lv3] += sht1WithLvParty[lv2][lv3]
    return sumSht1WithLv


def getMappingIndex(question, questLst):
    index = -1
    # 方式1， 如果questLst中有全量的question，则返回对应的scoreLst中的值
    # index = questLst.index(question)
    # 方式2， 如果仅有部分question，则需要遍历，返回对应的scoreLst中的值
    for partyQuest in questLst:
        if partyQuest is None:
            continue
        if question in partyQuest:  # 若quest 一致
            index = questLst.index(partyQuest)
            break
    return index


def saveRawQuestLst(questLst, peopleQuestLst, partyQuestLst, debug, debugPath, pathPre):
    """
    保存原始的问卷顺序 便于调试
    :param questLst:
    :param peopleQuestLst:
    :param partyQuestLst:
    :param debug:
    :param debugPath:
    :param pathPre:
    :return:
    """
    # 转置保存三个列表到csv中 - save three lists to csv vertically -
    rawLst = [questLst, peopleQuestLst, partyQuestLst]
    # 对齐长度 - align length
    maxLen = max(len(questLst), len(peopleQuestLst), len(partyQuestLst))
    for i in range(len(rawLst)):
        if len(rawLst[i]) < maxLen:
            rawLst[i] += [None] * (maxLen - len(rawLst[i]))
    # 转置 - transpose
    rawLst = list(map(list, zip(*rawLst)))
    saveDebugFile(["结果表问题列", "群众问题列表", "党员问题列表"],
                  rawLst,
                  debug, debugPath, pathPre)


def sortDebug(questLst, peopleOrderLst, partyOrderLst, partyQuestLst, peopleQuestLst, debugPath, debug=True):
    """
    用于调试排序
    题目:19 11.【不定项选择题		19.【单选题】您所
    :param questLst:
    :param partyQuestLst:
    :param peopleQuestLst:
    :param debug:
    :param partyOrderLst:
    :param peopleOrderLst:
    :return:
    """
    if not debug:
        return
    notFoundSign = "—————未找到—————"
    print("\t\t people \tparty对应问题顺序:")
    n = 0
    saveData = []
    for index1, index2 in zip(peopleOrderLst, partyOrderLst):
        questAns = questLst[n]
        peopleStr = peopleQuestLst[index1] if index1 != -1 else notFoundSign
        partyStr = partyQuestLst[index2] if index2 != -1 else notFoundSign
        # questAns = questLst[n] if "不计分" not in questLst[n] else questLst[n][:6] + "(不计分)"
        print(f"题目{n}:\t{questAns:<20}\t{peopleStr:<20}\t{partyStr:<20}")
        n += 1
        saveData.append([str(n), questAns, peopleStr, partyStr])
    # save SaveData to csv
    saveDebugFile(["No.", "结果表问题", "群众问题", "党员问题"],
                  saveData, debug, debugPath, "题目对应参照表")
    saveRawQuestLst(questLst, peopleQuestLst, partyQuestLst, debug, debugPath, "题目原始顺序表")


def getQuestionLst(surSht):
    """
    获取问卷的题目列表, 为了加速判分，将题目列表存储在内存中
    :param surSht:
    :return:
    """
    # get all content of surSht
    return surSht.range("A1:K" + str(surSht.used_range.last_cell.row)).value


class scoreJudgement:
    def __init__(self, testSurveySht, otherTitle, surveyQuesCol, surveyRuleCol, surveyQuesTypeCol):
        # 输入配置-分数表
        self.scoreExlTitle = None  # 存放scoreExl的标题
        self.surveyQuesCol = surveyQuesCol  # "E"  # 题目列
        self.surveyRuleCol = surveyRuleCol  # "J"  # 赋分规则列
        self.surveyQuesTypeCol = surveyQuesTypeCol  # "G"  # 题目类型列
        self.otherTitle = otherTitle
        self.testSurveySht = testSurveySht
        self.app4Ans = xw.App(visible=True, add_book=False)  # 党员问卷表
        self.app4Ans.display_alerts = False
        self.app4Ans.api.CutCopyMode = False

    def getStaffData(self, ansExlPh, fileName, deBugPath, surveyData, isDebug=True):
        """
        打开文件，获取答题后所有分数数据
        :param surveyData:
        :param deBugPath:
        :param fileName:
        :param ansExlPh:
        :param isDebug:
        :return:
        """
        # 问卷表打开 - open the survey sheet
        ansExl = self.app4Ans.books.open(ansExlPh)
        staffWithLv, self.scoreExlTitle = step1StaffDict(ansExl.sheets[0], self.otherTitle)
        ansExl.close()
        # print("得到员工字典完毕")
        # print("开始分数计算")
        staffWithLv = self.step2JudgeScoreWithLv(staffWithLv, deBugPath, fileName, surveyData, isDebug)
        scoreWithLv = getScoreWithLv(staffWithLv)
        # sht1WithLv = getSht1WithLv(scoreWithLv)
        printStaffWithLv(staffWithLv)
        return self.scoreExlTitle.answerLst, scoreWithLv  # sht1WithLv

    def step2JudgeScoreWithLv(self, staffWithLv, debugPath, fileName, surveyData, debug=True):
        """
        给每个人打分 得到stuffScoreWithLv Dict:
        :param surveyData:
        :param debugPath:
        :param staffWithLv:
        :param fileName:
        :param debug: whether save to debug csv
        :return:{lv2Depart: {lv3Depart: [stuff1, stuff2, ...]}}
        """
        debugScoreAllLst = []  # store [name, questTitle, answer, rule, score] for debug
        lv2Num = 0
        for lv2 in staffWithLv:
            lv2Num += 1
            lv3Num = 0
            for lv3 in staffWithLv[lv2]:
                lv3Num += 1
                print(f"Lv2:[{lv2Num}/{len(staffWithLv.keys())}] "
                      f"Lv3:[{lv3Num}/{len(staffWithLv[lv2].keys())}]", end="\r")
                stuffScoreList, debugScoreLst = self.calcEachStaff(staffWithLv[lv2][lv3], surveyData)
                staffWithLv[lv2][lv3] = stuffScoreList
                debugScoreAllLst += debugScoreLst
        print("")
        # if debug on, save the debugScoreLst to csv with current time
        saveDebugLogIfTrue(debugScoreAllLst, fileName, debug, debugPath)
        return staffWithLv

    def calcEachStaff(self, lv3StaffScoreList, surveyQuestionList: list = None):
        """
        通过所有员工列表获得员工的分数列表 {二级部门:{三级部门: [[分数, 分数], [分数, 分数]]}}
        from the staffWithLv, get the scoreLst, get the staff score list from the surveySht
        :param surveyQuestionList:  将问卷题目列表存储在内存中，加速判分
        :param lv3StaffScoreList: {lv2Depart:{lv3Depart: [staff, staff]}}
        :return: {lv2Depart:{lv3Depart: [[score], [score]]}}
        """
        debugScoreLst = []
        # 优化方式v3：将所有题目和规则读取到内存中
        for staff in lv3StaffScoreList:  # each staff in the lv3Depart
            # every staff need to get the all score
            for questionNum in range(len(self.scoreExlTitle.answerLst)):
                if not staff.answerLst[questionNum]:
                    continue
                # 得到每个问题的Title - get every questTitle by questTitle num
                questTitle = self.scoreExlTitle.answerLst[questionNum]
                # 如果是不计分的题目，跳过 - if the questTitle is not score, skip
                # if "不计分" in questTitle:
                #     staff.scoreLst[questionNum] = 0
                #     continue
                # 得到员工答案 - get staff staffAns
                staffAns = staff.answerLst[questionNum]
                if not staffAns:  # 员工没有答案则零分 - if staffAns is None, score is 0
                    staff.scoreLst[questionNum] = 0
                    continue
                # 找到问题所属判分规则 - locate which row is rule by questTitle in scoreExl
                # (answerRow, rule) = getRuleByQuestionSurvey(staff.name, questTitle, self.testSurveySht,
                #                                             self.surveyQuesCol, self.surveyRuleCol)
                (quesType, rule) = getRuleByQuestionList(questTitle, surveyQuestionList)
                if rule is None:  # 继续寻找问题规则 - continue to find rule of next question
                    continue
                # quesType = self.testSurveySht.range(f"{self.surveyQuesTypeCol}{answerRow}").value

                staff.scoreLst[questionNum] = judgeAnswerGrade(staffAns, rule, quesType)
                printScoreBugIf(staffAns, rule, questTitle, quesType, staff, questionNum)
                debugScoreLst.append([staff.name, questTitle, quesType, staffAns, rule, staff.scoreLst[questionNum]])
        return lv3StaffScoreList, debugScoreLst

    def close(self):
        self.app4Ans.quit()


def isLineValid(i: list) -> bool:
    """
    判断是否是有效行
    :param i:
    :return:
    """
    # if I is all None, skip
    if not i:
        return False

    for j in i:  # 但凡有一个不是None，就不是空行 - if any one is not None, it is not empty
        if j:
            return True
    return False


def step1StaffDict(ansSht, otherTitle):
    """
    动态获取最大使用范围，从答案表得到数据
    get the stuff list from the surveySht
    :return: stuffLst
    """
    staffWithLv = {}
    # scoreWithLv = {}
    # use all range to the value
    lastRow = ansSht.used_range.last_cell.row
    lastCol = ansSht.used_range.last_cell.column
    content = ansSht.range((1, 1), (lastRow, lastCol)).value
    # content = ansSht.range(departmentScope).value
    scoreExlTitle = ""
    addedSort = 0
    for i in content:
        if not isLineValid(i):
            print("空行无效注意：", i)
            continue

        if i[0] == "序号":
            scoreExlTitle = Stuff(i[1], i[2], i[3], i[4], i[5], i[6], i[9:])
            continue
        stu = Stuff(i[1], i[2], i[3], i[4], i[5], i[6], i[9:])
        # print(stu)
        if stu.lv2Depart not in staffWithLv:
            staffWithLv[stu.lv2Depart] = {}
            # scoreWithLv[stu.lv2Depart] = {}
        if not stu.lv3Depart:
            stu.lv3Depart = otherTitle
        if stu.lv3Depart not in staffWithLv[stu.lv2Depart]:
            staffWithLv[stu.lv2Depart][stu.lv3Depart] = []
            # scoreWithLv[stu.lv2Depart][stu.lv3Depart] = []
        staffWithLv[stu.lv2Depart][stu.lv3Depart].append(stu)
        addedSort += 1
        # scoreWithLv[stu.lv2Depart][stu.lv3Depart].append(stu.scoreLst)
    flag = f"step1StaffDict: 原数据{lastRow}行，有效数据{addedSort}行" if lastRow - 1 != addedSort else "step1StaffDict: 有效数量 全部匹配"
    print(flag)
    return staffWithLv, scoreExlTitle  # , scoreWithLv


def getSurveyData(sht0TestSurvey):
    """
    读取问卷数据
    :param sht0TestSurvey:
    :return:
    """
    allContent = sht0TestSurvey.used_range.address
    content = sht0TestSurvey.range(allContent).value

    surveyData = []
    questionNum = -1
    questionTypeNum = -1
    questionRuleNum = -1
    for i in content:
        if not isLineValid(i):
            continue
        if i[0] == "一级指标":
            questionNum = i.index("问题")
            questionTypeNum = i.index("题型")
            questionRuleNum = i.index("赋分方式")
            continue
        surveyData.append([i[questionNum], i[questionTypeNum], i[questionRuleNum]])

    return surveyData
# Github: GWillS163
# User: 駿清清 
# Date: 11/10/2022 
# Time: 22:16



def printAutoParamSht0(surveyQuesCol, surveyRuleCol, surveyQuesTypeCol,
                       sht0QuestionScp):
    print(f"surveyQuesCol: {surveyQuesCol}")
    print(f"surveyRuleCol: {surveyRuleCol}")
    print(f"surveyQuesTypeCol: {surveyQuesTypeCol}")
    print(f"sht0QuestionScp: {sht0QuestionScp}")
    return surveyQuesCol, surveyRuleCol, surveyQuesTypeCol, \
        sht0QuestionScp


def autoGetSht0Params(sht0, sht0LastValidRow):
    """
    得到Sht1复制Sht0的区间, 需要排除excludeSht0UnitLst
    """
    # get the top header of sht0
    sht0TopHeader = sht0.range("A1").expand('right').value
    res = []
    findKeyWords = {"问题": "E",
                    "赋分方式": "J",
                    "题型": "G"
                    }
    for key, value in findKeyWords.items():
        if key in sht0TopHeader:
            indexColNum = sht0TopHeader.index("问题")
        else:
            indexColNum = value
            print(f"Sht0的表头不符合要求(无{key}, {sht0TopHeader}), 请检查, 已默认")
        res.append(getColLtr(indexColNum))
    surveyQuesCol, surveyRuleCol, surveyQuesTypeCol = res

    sht0QuestionScp = f"{surveyQuesTypeCol}3:" \
                      f"{surveyQuesTypeCol}{sht0LastValidRow}"  # "E3:E31" 问题列 问题题目.

    return printAutoParamSht0(surveyQuesCol, surveyRuleCol,
                              surveyQuesTypeCol, sht0QuestionScp
                              )


def autoGetSht1Params(sht1Module, sht1TitleCopyFromSttCol, sht1TitleCopyToSttCol, Sht0LastValidRow):
    """
    通过少量用户输入, 自动获取问卷模板的参数.
    :param sht1Module: 问卷模板Sheet1
    :param sht1TitleCopyFromSttCol: "G" 给定模板的标题起始点，自动获取标题的范围
    :param sht1TitleCopyToSttCol: "G"  给定粘贴的起始点，自动获取标题粘贴和数据栏的范围
    :param Sht0LastValidRow: 问卷模板Sheet0的最后一行 (非党廉&纪检)
    :return:
    """
    # 获得模板表标题范围 - get the last column of the sht1Module
    sht1TitleCopyEndCol = sht1Module.used_range.last_cell.address.split("$")[1]
    sht1TitleCopyFromMdlScp = f"{sht1TitleCopyFromSttCol}1:{sht1TitleCopyEndCol}2"  # F1:MG2

    # 获得结果表标题最后列 - get the last column of the sht1Result
    sht1TitleCopyToEndCol = getColLtr(
        getColNum(sht1TitleCopyEndCol) - getColNum(sht1TitleCopyFromSttCol) + getColNum(sht1TitleCopyToSttCol))
    # 部门文件拆分用, 相同值不要合并，未经大量测试，不知道是否会出现问题
    sht1DeptTltRan = f"{sht1TitleCopyToSttCol}:{sht1TitleCopyToEndCol}"
    # 运行时自动获取 > sht1TitleCopyTo = f"{sht1TitleCopyToSttCol}1"
    sht1DataColRan = f"{sht1TitleCopyToSttCol}:{sht1TitleCopyToEndCol}"
    # Sht0的总体侧栏范围 - get the left column of the sht1Module
    sht1IndexScpFromSht0 = f"A1:F{Sht0LastValidRow}"  # 选项列的 最后一行非党廉数据
    printAutoParamSht1(sht1TitleCopyFromMdlScp, sht1DeptTltRan, sht1DataColRan)
    return sht1TitleCopyFromMdlScp, sht1DeptTltRan, sht1DataColRan, sht1IndexScpFromSht0


def autoGetSht2Params(sht2Mdl, sht0Sur, sht2DeleteCopiedColScp, mdlTltStt):
    """
    通过少量用户输入, 自动获取sht2问卷模板的参数

    :param mdlTltStt:
    :param sht2DeleteCopiedColScp:
    :param sht0Sur:
    :param sht2Mdl:
    :return:
    """

    # 已自动获取 sht2WgtLstScp = "C3:C13"
    # 已自动获取 sht2DeleteCopiedRowScp = "A32:A55"  # 要删除的部分需要动态获取 党廉&纪检 的区间
    # 用户指定 sht2DeleteCopiedColScp = "C1:J1"  需要删除的列

    # Title标题 - 从模板中获取
    # 用户指定 mdlTltStt = "D"
    mdlTltEnd = sht2Mdl.used_range.last_cell.address.split("$")[1]  # "PO"
    sht2TitleCopyFromMdlScp = f"{mdlTltStt}1:{mdlTltEnd}2"  # autoGetSht2TltScp(self.sht2Module)
    sht2DeptTltRan = f"{mdlTltStt}:{mdlTltEnd}"  # 部门文件 拆分用

    # Index侧栏 - 从测试问卷中获取
    surLastCol = sht0Sur.used_range.last_cell.address.split("$")[1]  # 一般是 K
    surLastRow = sht0Sur.used_range.last_cell.address.split("$")[2]  # 一般是 32
    sht2IndexCopyFromSvyScp = f"A1:{surLastCol}{surLastRow}"  # "A1:K32"
    sht2IndexCopyTo = "A1"  # 默认粘贴在左上角 - default paste to the left top corner

    # 结果表 - 粘贴的起始点
    # 自动获取最后一列 > sht2TitleCopyTo = "D1"
    # 已自动获取 > sht2TitleDataColScp = "D1:L2"

    printAutoParamSht2(sht2DeleteCopiedColScp, sht2TitleCopyFromMdlScp,
                       sht2DeptTltRan, sht2IndexCopyFromSvyScp, sht2IndexCopyTo)
    return sht2DeleteCopiedColScp, sht2TitleCopyFromMdlScp, sht2DeptTltRan, sht2IndexCopyFromSvyScp, sht2IndexCopyTo


def autoGetSht3Params(sht3Mdl, sht0Sur, mdlTltStt, surLastCol, resTltStt, vaildLastRow):
    """
    通过少量用户输入, 自动获取sht3问卷模板的参数
    :param sht3Mdl: sht3模板
    :param sht0Sur: sht0问卷
    :param mdlTltStt: 模板表的标题起始列
    :param surLastCol: 测试问卷的最后一列
    :param resTltStt: 结果表的标题粘贴起始列
    :return:
    """
    # title标题 - 从模板中获取
    # mdlTltStt = "L"
    mdlTltEnd = sht3Mdl.used_range.last_cell.address.split("$")[1]  # "BA"
    sht3TitleCopyFromMdlScp = f"{mdlTltStt}1:{mdlTltEnd}2"

    # index侧栏 - 从测试问卷中获取
    # surLastCol = "J"
    # surLastRow = sht0Sur.used_range.last_cell.address.split("$")[2]  # 54不是 "32"
    sht3IndexCopyFromSvyScp = f"A1:{surLastCol}{vaildLastRow}"  # 这个32是两个大单元的行数

    # result结果表 - 粘贴的起始点
    # resTltStt = "K"
    resTltEnd = getColLtr(getColNum(mdlTltEnd) - getColNum(mdlTltStt) + getColNum(resTltStt))  # "AZ"
    sht3DataColRan = f"{resTltStt}:{resTltEnd}"
    sht3TitleCopyTo = f"{resTltStt}1"
    printAutoParamSht3(sht3IndexCopyFromSvyScp, sht3DataColRan, sht3TitleCopyFromMdlScp)
    return sht3IndexCopyFromSvyScp, sht3DataColRan, sht3TitleCopyFromMdlScp


def autoGetSht4Params(sht4, sht4IndexFromMdl4Scp, sht4SumTitleFromMdlScp, sht4DataRowRan=None):
    """
    通过少量用户输入, 自动获取sht4问卷模板的参数
    :param sht4IndexFromMdl4Scp: 'A4:B52'  # Sht4固定两列AB公司, 长度是变量  title标题 - 从模板中获取
    :param sht4SumTitleFromMdlScp: "P1:Q3"  # 汇总单元格（本线条、全公司排名）
    :param sht4DataRowRan: 扫描行范围
    :param sht4:
    :return:
    """
    # index侧栏 - 从sht2中获取
    # 用户输入：sht4IndexFromMdl4Scp =
    # 用户输入：sht4TitleFromSht2Scp =

    #
    # 用户输入： sht4SumTitleFromMdlScp =

    # result结果表 - 粘贴的起始点
    # 默认值 sht4TitleCopyTo = 'A1'  # 默认值 - 无需修改
    # 已自动获取最后一列 sht4SumTitleCopyTo = "R1"  # 有改动, 应该要根据sht2的标题行数自动调整

    printAutoParamSht4(sht4IndexFromMdl4Scp, sht4SumTitleFromMdlScp,
                       )
    return sht4IndexFromMdl4Scp, sht4SumTitleFromMdlScp,


def paramsCheckExist(surveyExlPath, partyAnsExlPh, peopleAnsExlPh):
    """
    检查输入文件是否存在, 并新建保存路径
    Check Input files are
    :param peopleAnsExlPh:
    :param surveyExlPath:
    :param partyAnsExlPh:
    :return:
    """
    if surveyExlPath == partyAnsExlPh:
        raise FileExistsError("文件名输出重复,", surveyExlPath, partyAnsExlPh)
    fileDict = {
        "问卷模板文件": surveyExlPath,
        "党员答题文件": partyAnsExlPh,
        "群众答题文件": peopleAnsExlPh
    }
    for name, path in fileDict.items():
        if not os.path.exists(path):
            raise FileNotFoundError(f"{name} 不存在:")


def getCurrentYear(userYear=None):
    # if userYear is a yearNum within 1970-2500, return year, otherwise return current year
    if not userYear or not userYear.isdigit():
        return datetime.datetime.now().year
    if 1970 <= int(userYear) <= 2500:
        return int(userYear)
    else:
        return datetime.datetime.now().year


def getSumSavePathNoSuffix(savePath, fileYear, fileName):
    """
    得到每一个文件全路径的输出的前缀
    :param savePath:
    :param fileYear:
    :param fileName:
    :return:
    """
    fileYear = getCurrentYear(fileYear)
    return os.path.join(savePath, f"{fileYear}_{fileName}")


def readLvDict(orgSht):
    """返回结构化的字典，key是部门名，value是部门下的子部门"""
    allOrg = {}
    row = 1
    while True:
        a = orgSht.range(f"A{row}").value
        b = orgSht.range(f"B{row}").value
        if not (a and b):
            break
        if a not in allOrg:
            allOrg.update({a: [b]})
        else:
            allOrg[a].append(b)
        row += 1
    return allOrg


def paramsCheckSurvey(surveyExl, shtNameList: list):
    """
    调查问卷 文件名检查
    Survey Excel params check
    :param surveyExl:
    :param shtNameList:
    :return:
    """
    for shtName in shtNameList:
        try:
            surveyExl.sheets[shtName]
        except Exception as e:
            raise Exception(f"{shtName} 不存在于{surveyExl.name}中.\n ({e})")
    print(f"{surveyExl.name} Sheet 参数检查通过")


def getSavePath(savePath, fileYear, fileName):
    """
    生成用户保存路径
    :param fileYear:
    :param fileName:
    :param savePath:
    :return:
    """
    # make an output dir with current time
    outputDir = os.path.join(savePath, "PartyBuildOutput_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    os.makedirs(outputDir)

    sumSavePathNoSuffix = getSumSavePathNoSuffix(outputDir, fileYear, fileName)
    return outputDir, sumSavePathNoSuffix
# GitHub: @GWillS163
# Start Time: 2022-08-18
# End Time:


lv1Name = "北京公司"
lv2MeanStr = "二级单位"


class Excel_Operation:
    surveyRuleCol: str
    surveyQuesCol: str
    surveyQuesTypeCol: str

    def __init__(self, surveyExlPath, partyAnsExlPh, peopleAnsExlPh,
                 surveyTestShtName, sht1ModuleName, sht2ModuleName, sht3ModuleName, sht4ModuleName,
                 # ResultExl 配置
                 sht1Name, sht2Name, sht3Name, sht4Name,
                 # Sheet1 配置 : "F", "G"
                 sht1TitleCopyFromSttCol, sht1TitleCopyToSttCol,
                 # Sheet2 配置:  "C1:J1", "D"
                 sht2DeleteCopiedColScp, sht2MdlTltStt,
                 # Sheet3 配置:  "L", "J", "K"
                 sht3MdlTltStt, sht0SurLastCol, sht3ResTltStt,
                 # Sheet4 配置:
                 sht4IndexFromMdl4Scp, sht4SumTitleFromMdlScp,  # ,sht4DataRowRan
                 # 是否生成部门文件
                 isGenDepartments
                 ):
        """
        param surveyExlPath: the path of the survey excel
        :param scrExlPh:
        """
        # Saving File Settings
        self.surveyWgtCol = "K"
        self.orgShtName = '行政机构组织'
        self.otherTitle = "其他人员"
        self.lv2AvgTitle = "二级单位成绩"
        excludeSht0UnitLst = ["党廉", "纪检"]
        paramsCheckExist(surveyExlPath, partyAnsExlPh, peopleAnsExlPh)

        # self.surveyExlPath = surveyExlPath
        # self.scoreExlPath = scrExlPh
        self.app4Survey1 = xw.App(visible=True, add_book=False)
        self.app4Result3 = xw.App(visible=True, add_book=False)
        self.app4Survey1.display_alerts = False
        self.app4Result3.display_alerts = False
        self.app4Survey1.api.CutCopyMode = False
        self.app4Result3.api.CutCopyMode = False
        # open the survey file with xlwings
        self.surveyExl = self.app4Survey1.books.open(surveyExlPath)
        self.resultExl = self.app4Result3.books.add()

        # 输入配置-规则表 修改后请核对以下配置
        paramsCheckSurvey(self.surveyExl, [surveyTestShtName, sht2ModuleName, sht3ModuleName, sht4ModuleName])
        self.sht0TestSurvey = self.surveyExl.sheets[surveyTestShtName]  # "测试问卷"
        # module settings
        self.sht1Mdl = self.surveyExl.sheets[sht1ModuleName]  # "调研结果_输出模板"
        self.sht2Mdl = self.surveyExl.sheets[sht2ModuleName]  # "调研成绩_输出模板"
        self.sht3Mdl = self.surveyExl.sheets[sht3ModuleName]  # "调研结果（2022年）_输出模板"
        self.sht4Mdl = self.surveyExl.sheets[sht4ModuleName]  # "调研成绩（2022年）_输出模板"
        # basic output settings 
        self.sht1NameRes = sht1Name
        self.sht2NameGrade = sht2Name
        self.sht3NameResYear = sht3Name
        self.sht4NameScoreYear = sht4Name

        # 通用配置
        self.deletedUnitList = excludeSht0UnitLst  # 删除的单位
        self.deptCopyHeight = 40  # 从总表复制到 各个部门表时的高度

        # Sheet0 survey表 数据获取 - Module Sheet 0 TestSurvey
        # 调查规则表中的问题列 规则列 问题类型列
        self.sht0DeleteCopiedRowScp, sht0LastValidRow = getSht0DeleteCopiedRowScp(
            self.sht0TestSurvey, self.deletedUnitList)
        self.surveyQuesCol, self.surveyRuleCol, \
            self.surveyQuesTypeCol, self.sht0QuestionScp = \
            autoGetSht0Params(self.sht0TestSurvey, sht0LastValidRow)

        # Sheet1  每次更改模板表后之后请留意
        self.sht1MdlPartRatioRowScp = "A3:D5"  # 新增的参与率区域 参与率粘贴的位置，一般不需要修改
        self.sht1PartitionInsertPoint = "A3"  # 插入，无法自动获取
        self.sht1TitleCopyFromMdlScp, self.sht1DeptTltRan, \
            self.sht1DataColRan, self.sht1IndexScpFromSht0 = \
            autoGetSht1Params(self.sht1Mdl,
                              sht1TitleCopyFromSttCol,
                              sht1TitleCopyToSttCol, sht0LastValidRow)
        # Sheet2:
        self.sht2MdlPartRatioRowScp = "A3:C5"  # Sheet2 参与率部分的范围
        self.sht2PartitionInsertPoint = "A3"  # Sheet2 插入参与率的位置 无法自动获取

        self.sht2TitleCopyTo = None  # 自动获取sheet2 title 起始点
        self.sht2DeleteCopiedColScp, self.sht2TitleCopyFromMdlScp, \
            self.sht2DeptTltRan, self.sht2IndexCopyFromSvyScp, self.sht2IndexCopyTo = \
            autoGetSht2Params(self.sht2Mdl, self.sht0TestSurvey,
                              sht2DeleteCopiedColScp,  # ="C1:J1"
                              sht2MdlTltStt)  # ="D"

        # Sheet3:
        self.sht3MdlPartRatioRowScp = "A3:E5"
        self.sht3PartitionInsertPoint = "A3"
        self.sht3TitleCopyTo = None  # 自动获取sheet3 title 起始点
        self.sht3IndexCopyFromSvyScp, self.sht3DataColRan, self.sht3TitleCopyFromMdlScp = \
            autoGetSht3Params(self.sht3Mdl, self.sht0TestSurvey, sht3MdlTltStt, sht0SurLastCol,
                              sht3ResTltStt, sht0LastValidRow)  # "L", "J", "K"

        # Sheet4:
        self.sht4TitleCopyTo = None  # 自动获取sheet4 title 起始点
        self.sht4TitleFromSht2Scp = None  # 'A1:C17'  # Sht2模板中的index侧栏，长度是固定的
        self.sht4IndexFromMdl4Scp, self.sht4SumTitleFromMdlScp = \
            autoGetSht4Params(self.sht4Mdl, sht4IndexFromMdl4Scp, sht4SumTitleFromMdlScp)

        # When add Sheet 2
        self.lv2UnitColLtr = "B"
        self.weightColLtr = "K"
        self.sht2SttRow = 3
        self.sht2EndRow = 40

        # When generate department file
        self.isGenDepartments = isGenDepartments
        self.sht1IndexScp4Depart = None  # 生成侧标题后 自动获取"A1:F32"  # 生成部门文件时，需要复制的范围
        self.sht2IndexScp4Depart = None  # 生成侧标题后 自动获取"A1:C20"  # 生成部门文件用，复制左侧栏
        self.sht1TitleCopyTo = None

        # 新增参与率统计 - 2022-11-11
        self.allStaffNum = {}
        # self.allStaffNum = {
        #     '党委办公室（党群工作部、职能管理部党委）': {'党委工作室': 5, '党建工作室': 9, '职能管理部党委办公室': 2, '企业文化室': 4, '青年工作室': 1}}  # 保存所有人员的人数

    def addSheet1_surveyResult(self):
        """
        新增 Sheet1
        generate sheet1 of the surveyExl, which is the survey without weight
        :return:
        """
        # titleStart, r = self.sht1MdlTltScope.split(":")
        # dataStart = r + str(int(self.sht1MdlTltScope.split(":")[1][-1]) + 1)
        # Step1: add new sheet and define module sheet
        sht1_lv2Result = self.resultExl.sheets.add(self.sht1NameRes)

        # Step2.1: copy left column the surveySht to sht1 partially with style
        # UnitScpRowList = getUnitScpRowList(self.sht0TestSurvey, "A", "D", ["党建", "宣传文化"])

        print("Sheet1 侧栏问题列处理 - Index Columns Processing...")
        print("Step1: 从Sht0整体复制侧栏 - copy left column the surveySht to sht1, with style")
        shtCopyTo(self.sht0TestSurvey, self.sht1IndexScpFromSht0,
                  sht1_lv2Result, f"A1")
        print("Step2.1 删除多余行(党廉&纪检) - delete the row of left column redundant")
        sht1_lv2Result.range(self.sht0DeleteCopiedRowScp).api.EntireRow.Delete()

        # getSht12DeleteCopiedRowScp
        print("Sheet1 复制参与率部分 - Copying Participation Rate...")
        sht1OprAddPartRatio(self.sht1Mdl, self.sht1MdlPartRatioRowScp,
                            sht1_lv2Result, self.sht1PartitionInsertPoint)

        # 记录左侧栏的范围 为生成部门文件时使用 - Record the left column range for generating department files
        self.sht1IndexScp4Depart = sht1_lv2Result.used_range.address

        # Step2.2: copy title
        print("Sheet1 部门标题处理 - Title Rows Processing...")
        self.sht1TitleCopyTo = getLastColCell(sht1_lv2Result)
        shtCopyTo(self.sht1Mdl, self.sht1TitleCopyFromMdlScp,
                  sht1_lv2Result, self.sht1TitleCopyTo)  # sht1_tltScope = "F1:KZ2"
        return sht1_lv2Result

    def addSheet2_surveyGrade(self):
        """
        生成sheet2的成绩表无数据，仅有二级标题，新增二级求和与全部求和。
        generate sheet2 of the surveyExl, only with title and sum
        :return: None
        """
        # Step1: 新增Sheet2 - add new sheet and define module sheet
        sht2_lv2Score = self.resultExl.sheets.add(self.sht2NameGrade, after=self.sht1NameRes)

        print("Sheet2 表头和侧栏部分处理 - header and sidebar section")
        sht2_lv2Score.range("B1").column_width = 18.8
        print("Step2: 从Sht0整体复制侧栏 - copy left column the surveySht to sht1, with style")
        shtCopyTo(self.sht0TestSurvey, self.sht2IndexCopyFromSvyScp,
                  sht2_lv2Score, self.sht2IndexCopyTo)
        print("Step2.1 删除多余行(党廉&纪检) - delete the row of left column redundant")
        sht2_lv2Score.range(self.sht0DeleteCopiedRowScp).api.EntireRow.Delete()

        print("Step2.2: 删除左侧多余单元行 - delete the row of left column redundant")
        print("Step2.2.1: 删除多余行 - delete the row of left column redundant")
        sht2UnitScp = getShtUnitScp(sht2_lv2Score, self.sht2SttRow, self.sht2EndRow, self.lv2UnitColLtr, "D")
        print("Step2.2.2: 为单元格重新计算权重 - recalculate the weight to the cell")
        # 给所有单元格边缘增加偏移 - add offset to all cells edge
        sht2UnitScpOffsite = [[edge + self.sht2SttRow for edge in eachUnit] for eachUnit in sht2UnitScp]
        resetUnitSum(sht2_lv2Score, sht2UnitScpOffsite, self.weightColLtr)
        print("Step2.2.3: 重设单元值完成 - Reset unit value completed")
        sht2DeleteRowLst = getSht2DeleteRowLst(sht2UnitScpOffsite)
        for _ in range(len(sht2DeleteRowLst)):
            row = sht2DeleteRowLst.pop()
            sht2_lv2Score.range(f"{self.lv2UnitColLtr}{row}").api.EntireRow.Delete()
        print("Step2.3 删除多余列 - delete the column C to I")
        sht2_lv2Score.range(self.sht2DeleteCopiedColScp).api.EntireColumn.Delete()

        print("Step3: 增加合计行 -  add summary row")
        lv2UnitScp = getShtUnitScp(sht2_lv2Score, self.sht2SttRow, self.sht2EndRow, "A", "B")
        sht2OprAddSummaryRows(sht2_lv2Score, lv2UnitScp)

        print("Step4: 增加参与率统计 - add participation rate statistics")
        sht2OprAddPartRatio(self.sht2Mdl, self.sht2MdlPartRatioRowScp, sht2_lv2Score, self.sht2PartitionInsertPoint)
        # 记录左侧栏的范围 为生成部门文件时使用 及Sheet4使用 - Record the left column range for generating department files
        self.sht2IndexScp4Depart = sht2_lv2Score.used_range.address

        print("Step4: 整体复制title - copy title")
        # get last column of the sht2
        self.sht2TitleCopyTo = getLastColCell(sht2_lv2Score)
        shtCopyTo(self.sht2Mdl, self.sht2TitleCopyFromMdlScp, sht2_lv2Score, self.sht2TitleCopyTo)

        return sht2_lv2Score, lv2UnitScp

    def addSheet3_surveyResultByYear(self):
        """
        generate sheet3 of the surveyExl, which is the survey without weight
        :return: None
        """

        # Step1: add new sheet and define module sheet
        sht3_ResYear = self.resultExl.sheets.add(self.sht3NameResYear, after=self.sht2NameGrade)

        # Step2: Set Index column
        shtCopyTo(self.sht0TestSurvey, self.sht3IndexCopyFromSvyScp, sht3_ResYear,
                  self.sht3IndexCopyFromSvyScp.split(":")[0])

        print("\t 新增参与率统计")
        sht3OprAddPartRatio(self.sht3Mdl, self.sht3MdlPartRatioRowScp, sht3_ResYear, self.sht3PartitionInsertPoint)

        # Step3: copy title
        self.sht3TitleCopyTo = getLastColCell(sht3_ResYear)
        shtCopyTo(self.sht3Mdl, self.sht3TitleCopyFromMdlScp, sht3_ResYear, self.sht3TitleCopyTo)

        return sht3_ResYear

    def addSheet4_surveyGradeByYear(self):
        """
        generate sheet4 of the surveyExl, which is the survey with weight
        :return: None
        """
        print("Step1: 新增Sheet4 - add new sheet")
        sht4_surveyGradeByYear = self.resultExl.sheets.add(self.sht4NameScoreYear, after=self.sht3NameResYear)
        sht2_lv2Score = self.resultExl.sheets[self.sht2NameGrade]

        print("Step2: 粘贴问卷单元title - copy title of survey")
        # sht2_lv2Score.api.Range(self.sht4TitleFromSht2Scp).Copy()
        sht2_lv2Score.api.Range(self.sht2IndexScp4Depart).Copy()
        sht4_surveyGradeByYear.api.Range("A1").PasteSpecial(Transpose=True)

        print("Step3: 复制模板的左侧线条公司栏 - copy left column of the template")
        sht4LineCompanyCopyTo = getLastRowCell(sht4_surveyGradeByYear)
        shtCopyTo(self.sht4Mdl, self.sht4IndexFromMdl4Scp,
                  sht4_surveyGradeByYear, sht4LineCompanyCopyTo)

        print("Step4: 粘贴汇总title - summarize Title patch")
        self.sht4TitleCopyTo = getLastColCell(sht4_surveyGradeByYear)
        shtCopyTo(self.sht4Mdl, self.sht4SumTitleFromMdlScp,
                  sht4_surveyGradeByYear, self.sht4TitleCopyTo)
        # set column B width = 20
        sht4_surveyGradeByYear.range("B1").column_width = 28
        return sht4_surveyGradeByYear

    def genDepartFile(self, departCode, sumSavePathNoSuffix):
        """ 通过汇总表生成所有部门文件, 生成固定的标题侧栏，然后填充数据-保存-清空数据
        generate the department file of the surveyExl， generate the fixed title sidebar, then fill data-save-clear data
        :return: None
        """
        if not self.isGenDepartments:
            print("选择未生成部门文件 - No department file generated")
            return

        # 从汇总表 获取 部门分类区间
        sht1Sum = self.resultExl.sheets[self.sht1NameRes]
        sht2Sum = self.resultExl.sheets[self.sht2NameGrade]
        deptUnitSht1 = getDeptUnit(sht1Sum, self.sht1DeptTltRan, 0)
        deptUnitSht2 = getDeptUnit(sht2Sum, self.sht2DeptTltRan, 0)

        print("新建部门文件 - create new excel with xlwings")
        app4Depart = xw.App(visible=True, add_book=False)
        deptResultExl = app4Depart.books.add()
        app4Depart.display_alerts = False
        app4Depart.api.CutCopyMode = False
        sht1Dept = deptResultExl.sheets.add(self.sht1NameRes)
        sht2Dept = deptResultExl.sheets.add(self.sht2NameGrade, after=sht1Dept)
        try:
            deptResultExl.sheets["Sheet1"].delete()
        except Exception as e:
            pass
        print("从汇总表 复制 边栏")
        # sht1Dept.activate()
        shtCopyTo(sht1Sum, self.sht1IndexScp4Depart, sht1Dept, "A1")
        # sht2Dept.activate()
        shtCopyTo(sht2Sum, self.sht2IndexScp4Depart, sht2Dept, "A1")

        # 填充数据 - 保存 - 删除
        sht2BorderL, sht2BorderR = "G", "Z"
        departStt = time.time()
        n = 0
        for deptName in deptUnitSht1:
            n += 1
            # add department data
            sht1BorderL, sht1BorderR = addOneDptData(sht1Sum, deptUnitSht1[deptName], self.deptCopyHeight,
                                                     sht1Dept, self.sht1TitleCopyTo)
            if deptName in deptUnitSht2:
                sht2BorderL, sht2BorderR = addOneDptData(sht2Sum, deptUnitSht2[deptName], self.deptCopyHeight,
                                                         sht2Dept, self.sht2TitleCopyTo)

            # Save Excel 保存文件名需要 加上部门Code
            deptCode = ""
            try:
                deptCode = departCode[deptName]['departCode']
            except:
                pass
            # departFilePath = self.sumSavePath.replace(".xlsx", f"_{deptName}_{deptCode}.xlsx")
            departFilePath = sumSavePathNoSuffix + f"_{deptCode}.xlsx"
            print(f"\033[32m{n:2} - 正在保存:[{deptCode}] - [{int(time.time() - departStt)}s] {deptName} - \033[0m")
            deptResultExl.save(departFilePath)
            departStt = time.time()

            # Method1: Clear the sheet for next loop dynamically
            # sht1Dept.activate()
            # dltOneDptData(sht1Dept, self.sht1TitleCopyTo, self.deptCopyHeight,
            #               sht1BorderR, sht1BorderL)
            # if deptName in deptUnitSht2:
            #     sht2Dept.activate()
            #     dltOneDptData(sht2Dept, self.sht2TitleCopyTo, self.deptCopyHeight,
            #                   sht2BorderL, sht2BorderR)

            # Method2
            borderWidth = getColNum(sht1BorderR) - getColNum(sht1BorderL)
            borderStart = getColNum(self.sht1TitleCopyTo[0])
            borderEnd = getColLtr(borderStart + borderWidth)
            sht1Dept.activate()
            sht1Dept.range(f"{self.sht1TitleCopyTo}:{borderEnd}{self.deptCopyHeight}").api.Delete()
            if deptName in deptUnitSht2:
                borderWidth = getColNum(sht2BorderR) - getColNum(sht2BorderL)
                borderStart = getColNum(self.sht2TitleCopyTo[0])
                borderEnd = getColLtr(borderStart + borderWidth)
                sht2Dept.activate()
                sht2Dept.range(f"{self.sht2TitleCopyTo}:{borderEnd}{self.deptCopyHeight}").api.Delete()

        print("部门文件全部生成完毕，即将关闭文件")
        deptResultExl.close()
        app4Depart.quit()

        self.resultExl.close()
        self.app4Result3.quit()

    def placeBarWithoutData(self) -> list:
        # Add Title & column
        sht1_lv2Result = self.addSheet1_surveyResult()
        print("sheet1 无数据页面生成完成\n")
        sht2_lv2Score, lv2UnitScp = self.addSheet2_surveyGrade()
        print("sheet2 无数据页面生成完成\n")
        sht3_ResYear = self.addSheet3_surveyResultByYear()
        print("sheet3 无数据页面生成完成\n")
        sht4_surveyGradeByYear = self.addSheet4_surveyGradeByYear()
        print("sheet4 无数据页面生成完成")
        return [sht1_lv2Result, sht2_lv2Score, sht3_ResYear, sht4_surveyGradeByYear, lv2UnitScp]

    def fillAllData(self, sht1WithLv, shtList: list, departCode: dict, sumSavePathNoSuffix: str):
        """
        使用sheet1的数据计算出来接下来的数据，然后填充到excel中, 获得汇总的1 个文件
        use sheet1 data to calculate the data of the next sheet, then fill it into the excel
        :param sumSavePathNoSuffix: 
        :param departCode: 
        :param shtList: sht1_lv2Result, sht2_lv2Score, sht3_ResYear, sht4_surveyGradeByYear 
        :param sht1WithLv: 
        :return: 
        """""
        sht1_lv2Result, sht2_lv2Score, sht3_ResYear, sht4_surveyGradeByYear, lv1UnitScp = shtList
        print("开始生成参与率")
        basicParticipateRatio = getBasicParticipates(self.allStaffNum, departCode, lv2MeanStr, lv1Name)

        # Step3: Set data
        if sht1WithLv:
            sht1WithLv = sht1WithLv  # mock data, will be deleted

        print("sheet1 填充数据 - Sheet1 fill data vertically")
        sht1_lv2Result.activate()
        # two Methods to set data
        # sht1PlcScoreByPD(self.sht1Module, sht1_lv2Result, staffWithLv, self.sht1MdlTltScope, dataStart)
        printShtWithLv("sht1WithLv：", sht1WithLv)
        sht1WithLvPtRt = combineSht1Ratio(sht1WithLv, basicParticipateRatio)
        printShtWithLv("sht1WithLvPtRt：", sht1WithLvPtRt)
        sht1SetData(sht1_lv2Result, sht1WithLvPtRt, getTltColRange(self.sht1DataColRan, 1))

        print("sheet2 填充数据 - sheet2 fill data vertically")
        sht2_lv2Score.activate()
        sht2WithLv = clacSheet2_surveyGrade(sht1_lv2Result, self.sht0TestSurvey, self.surveyWgtCol,
                                            sht1WithLv, lv1UnitScp, departCode)
        sht2WithLvPtRt = combineSht2Ratio(sht2WithLv, basicParticipateRatio)
        print("sht2WithLv：", sht2WithLvPtRt)
        sht2SetData(sht2_lv2Score, sht2WithLvPtRt, getTltColRange(self.sht2TitleCopyFromMdlScp, 1))

        print("sheet3 填充数据 - sheet3 fill data vertically")
        sht3_ResYear.activate()
        sht3WithLv = getSht3WithLv(sht1WithLv, lv1Name, lv2MeanStr)
        print("sht3WithLv：", sht3WithLv)
        sht3WithLvPtRt = combineSht3Ratio(sht3WithLv, basicParticipateRatio, lv2MeanStr, lv1Name)
        print("sht3WithLvPtRt：", sht3WithLvPtRt)
        sht3SetData(sht3_ResYear, sht3WithLvPtRt, self.sht3DataColRan, lv1Name)
        # sht3 set conditional formatting partially

        print("sheet4 填充横向数据 - Sheet4 fill data horizontally")
        sht4_surveyGradeByYear.activate()
        sht4Hie = getSht4Hierarchy(sht4_surveyGradeByYear)
        sht4WithLv = getSht4WithLv(sht2WithLv, sht4Hie, lv1Name)
        print("sht4WithLv：", sht4WithLv)
        sht4Ratio = turnSht4Ratio(basicParticipateRatio, sht4Hie, lv1Name, lv2MeanStr)
        sht4WithLvPtRt = combineSht4Ratio(sht4WithLv, sht4Ratio, lv2MeanStr, lv1Name)
        print("sht4WithLvPtRt：", sht4WithLvPtRt)
        # Get last row Num by used_range
        sht4LastRow = sht4_surveyGradeByYear.used_range.last_cell.row
        sht4DataRowRan = range(4, sht4LastRow + 1)
        sht4SetData(sht4_surveyGradeByYear, sht4WithLvPtRt, sht4DataRowRan, lv1Name)

        print("删除无用的sheet - Delete useless sheet")
        self.resultExl.sheets["Sheet1"].delete()
        savePath = sumSavePathNoSuffix + "_200000000.xlsx"
        print(f"汇总表将保存在：{savePath}")
        self.resultExl.save(savePath)
        self.surveyExl.close()
        self.app4Survey1.quit()

    def getFirstSht1WithLvData(self, partyAnsExlPh, peopleAnsExlPh, savePath):
        """
        获取第一个sheet1的数据，用于计算其他sheet的数据， 使用后关闭答案
        :return:
        """
        print("开始获取第一个sheet1的数据")
        debugPath = os.path.join(savePath, "分数判断记录")
        judges = scoreJudgement(self.sht0TestSurvey, self.otherTitle, self.surveyQuesCol, self.surveyRuleCol,
                                self.surveyQuesTypeCol)
        questionLst = self.sht0TestSurvey.range(self.sht0QuestionScp).value  # 问题列表
        print("开始获取群众数据 - Start to get people data")
        surveyData = getSurveyData(self.sht0TestSurvey)
        peopleQuesLst, sht1PeopleData = judges.getStaffData(peopleAnsExlPh, "群众", debugPath, surveyData, True)
        printSht1Data("群众", sht1PeopleData, peopleQuesLst)
        print("开始获取党员数据 - Start to get party data")
        partyQuesLst, sht1PartyData = judges.getStaffData(partyAnsExlPh, "党员", debugPath, surveyData, True)
        printSht1Data("党员", sht1PartyData, partyQuesLst)
        # 计算所有部门人数
        self.allStaffNum = countDepartStaffNum(sht1PeopleData, sht1PartyData)
        questionSortDebugPath = os.path.join(savePath, "题目对应记录")
        sht1WithLvCombine = combineMain(questionLst, peopleQuesLst, sht1PeopleData, partyQuesLst, sht1PartyData,
                                        questionSortDebugPath)
        judges.close()
        printSht1WithLv(sht1WithLvCombine)
        return sht1WithLvCombine

    def run(self, partyAnsExlPh, peopleAnsExlPh, outputDir, sumSavePathNoSuffix, mockSht1WithLV=None):
        """
        主程序
        run the whole process, the main function.
        :return:
        """

        stt = time.time()
        departsInfo = getAllOrgInfo(self.surveyExl.sheets(self.orgShtName))
        print("一、获取答题数据，开始判分 - 0. get data of score sheet, start to calculate score")
        if mockSht1WithLV is None:
            sht1WithLvCombine = self.getFirstSht1WithLvData(partyAnsExlPh, peopleAnsExlPh, outputDir)
            print(f"\n\033[33m\nGetScore time: {int(time.time() - stt)}s \033[0m")
        else:
            sht1WithLvCombine = mockSht1WithLV
        print("\n二、填充边栏 - II. fill the sidebar")
        shtList = self.placeBarWithoutData()
        print(f"\n\033[33m\nPlaceBar time: {int(time.time() - stt)}s \033[0m")

        print("\n三、填充参与率&分数数据、生成汇总文件 - III. fill data, generate summary file")
        self.fillAllData(sht1WithLvCombine, shtList, departsInfo, sumSavePathNoSuffix)
        print(f"\n\033[33m\nFillData time: {int(time.time() - stt)}s \033[0m")

        print("\n五、生成各部门文件 - IV. generate each department file")
        self.genDepartFile(departsInfo, sumSavePathNoSuffix)

        print(f"\n\033[33m\nTotal time: {int(time.time() - stt)}s [ll Done! Saved to:\033[0m "
              f"\n\033[32m{outputDir}\033[0m")
# Github: GWillS163
# User: 駿清清 
# Date: 29/09/2022 
# Time: 14:01

# import sys
# sys.path.append(r"D:\Project\python_scripts\forWorking\HuayunTechRPA\Beijing_ExlGenerate_2022-8-18")


print("Start to run the process...")
outputDir, sumSavePathNoSuffix = getSavePath(savePath, fileYear, fileName)

exlMain = Excel_Operation(
    surveyExlPh, partyAnsExlPh, peopleAnsExlPh,
    surveyTestShtName, sht1ModuleName, sht2ModuleName, sht3ModuleName, sht4ModuleName,
    sht1Name, sht2Name, sht3Name, sht4Name,

    # Sheet1 生成配置 : F, G
    sht1TitleCopyFromSttCol, sht1TitleCopyToSttCol,
    # Sheet2 生成配置: C1:J1, D
    sht2DeleteCopiedColScp, sht2MdlTltStt,
    # Sheet3 生成配置:  "L", "J", "K"
    sht3MdlTltStt, sht0SurLastCol, sht3ResTltStt,
    # Sheet4 生成配置:
    sht4IndexFromMdl4Scp, sht4SumTitleFromMdlScp,  # , sht4DataRowRan
    isGenDepartments  # 是否生成部门

)
# exlMain.run(partyAnsExlPh, peopleAnsExlPh, outputDir, sumSavePathNoSuffix, mockSht1WithLV=sht1WithLv)
exlMain.run(partyAnsExlPh, peopleAnsExlPh, outputDir, sumSavePathNoSuffix)
