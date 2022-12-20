#  Author : Github: @GWillS163
#  Time: 2022-10-1

# Description: 用于计算数据的模块
from typing import Dict, Optional, Any, List, Union
from .utils import *


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
        if type(x) == str:
            x = float(x.strip("%")) / 100
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
        # 单独计算 有效数据，并用来计算平均值
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


def addAllTotal(lv3ScoreLst, lv1IndexSpan):
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
        res.append(getSht2UnitWgtScore(unitLst))  # 加入本单元求和
    res.append(getSht2UnitWgtScore(lv3ScoreLst))
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


def descSortWithNone(currNumsSorted):
    """
    降序排序，None放在最后
    """
    currNumsSorted.sort(key=lambda x: x if x is not None else -100, reverse=True)
    return currNumsSorted


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
        descSortWithNone(currNumsSorted)  # Desc
        orderRes[num] = currNumsSorted.index(currentScore[num]) + 1
    return orderRes


def getSht2WithLvData(sht1WithLv: dict, lv1IndexSpan: list, lv2UnitSpan: list, lineData: dict) -> dict:
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
            lv2Avg = "二级单位" if "二级单位" in lv3 else lv3  # Rename
            eachUnitScore = sumEachSmallUnitScore(sht1WithLv[lv2][lv3], lv1IndexSpan)
            bigUnitSum = addAllTotal(eachUnitScore, lv2UnitSpan)
            sht2WithLv[lv2].update({lv2Avg: bigUnitSum})

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


def getSht4WithLv(sht2WithLv: dict, sht4Hierarchy: list, lv1Name: str, lv2MeanStr) -> dict:
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
                                                 sht2WithLv[lv2][lv2MeanStr]})
        allLv2.append(sht2WithLv[lv2]['二级单位'])

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
    weightLst = sht.range(f"{weightCol}1:{weightCol}{sht2UnitScp[-1][-1]}").value
    for unit in sht2UnitScp:
        cellSum = 0
        unitWeight = weightLst[unit[0] - 1: unit[1]]
        weight = sumWithNone(unitWeight)
        # for edge in range(unit[0], unit[1] + 1):
        #     # weight = sht.range(f"{weightCol}{edge}").value
        #     try:
        #         assert type(weight) == float or type(weight) == int
        #     except Exception as e:
        #         print("weight is not int:", e)
        #         weight = 0
        #     # print(f"\t 获得单元格值:{weightCol}{edge} = {weight} get value of weightCell: ")
        if not type(weight) == float or type(weight) == int:
            weight = 0
        cellSum += weight
        # print(f"求和放至首格：{weightCol}{unit[0]}={cellSum} - place the sum to the first cell of the unit\n")
        sht.range(f"{weightCol}{unit[0]}").value = f"{round(cellSum * 100, 1)}%"


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
    global partLst
    if skipWords is None:
        skipWords = []
    resultSpan = []
    tempScp = [-1, -1]
    if skipCol:
        partLst = sht.range(f"{skipCol}1:{skipCol}{endRow}").value
    unitLst = sht.range(f"{unitCol}1:{unitCol}{endRow}").value
    contentLst = sht.range(f"{contentCol}1:{contentCol}{endRow}").value
    n = 0
    while n < endRow:
        row = startRow + n - 1
        if skipCol:
            # part = sht.range(f"{skipCol}{row}").value
            part = partLst[row]
            # detect skip words if part equal skip words, thus skip this row
            if part in skipWords:
                n += 1
                continue
        unit = unitLst[row]
        content = contentLst[row]
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
    if resultSpan[0][0] == -1:  # 若是第一个为-1 则置位0
        resultSpan[0][0] = 0
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


def sumEachSmallUnitScore(lv3ScoreLst: list, lv2Unit: list):
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
        # 限定最后一个单元格范围
        endBound = len(lv3ScoreLst) if unitScp[1] + 1 > len(lv3ScoreLst) else unitScp[1] + 1
        res.append(  # 若单元有多个单元格，则求和
            sumWithNone(lv3ScoreLst[unitScp[0]:endBound]))
    return res


def sumWithNone(lst):
    """
    处理包含None值的 列表求和
    :param lst:
    :return:
    """
    if all([i is None for i in lst]):  # 若全为None，则返回None
        return None
    return sum([validNum for validNum in lst if validNum is not None])


def getSht2UnitWgtScore(lst):
    sumScore = sumWithNone(lst)
    if sumScore == 0:
        return sumScore
    return round(sumScore / 10, 2)


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
    sht1WithLvWgt = {}
    for lv2 in sht1WithLv:
        sht1WithLvWgt.update({lv2: {}})
        for lv3 in sht1WithLv[lv2]:
            sht1WithLvWgt[lv2].update({lv3: []})
            sht1WithLvWgt[lv2][lv3] = listMultipy(sht1WithLv[lv2][lv3], sht1WgtLst)
    return sht1WithLvWgt


def getSht2WithLv(sht1_lv2Result, sht2_lv2Score, sht0_survey, questionCol, sht1WithLv,
                  lv1UnitSpan, lv2UnitSpan, departCode,

                  ):
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
    # lv2UnitSpan = getShtUnitScp(sht1_lv2Result, sht2StartRow, sht2EndRow,
    #                             sht2UnitCol, sht2ContentCol, sht2SkipCol, sht2SkipWords)
    # lv1UnitSpan = getShtUnitScp(sht1_lv2Result, startRow=3, endRow=40,
    #                             unitCol="A", contentCol="B")
    lineData = getLineData(departCode)
    # 单元格求和
    sht2WithLv = getSht2WithLvData(sht1WithLvWgt, lv1UnitSpan, lv2UnitSpan, lineData)
    return sht2WithLv


def getNewUnitWgts(sht2_lv2Score, sht2SttRow, sht2EndRow, lv2UnitColLtr, WgtColLtr):
    sht2UnitScp = getShtUnitScp(sht2_lv2Score, sht2SttRow, sht2EndRow, lv2UnitColLtr, WgtColLtr)
    sht2UnitScpOffsite = [[edge + sht2SttRow for edge in eachUnit] for eachUnit in sht2UnitScp]
    return sht2UnitScpOffsite


def addRankForSht2(sht2WithLv, lineData, lv2ScoreName="二级单位"):
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
