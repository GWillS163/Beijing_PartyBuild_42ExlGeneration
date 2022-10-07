#  Author : Github: @GWillS163
#  Time: 2022-10-1

# Description: 用于计算数据的模块
from typing import Dict, Optional, Any, List, Union
from .utils import *


# import pandas as pd


def listMultipy(lst1, lst2):
    return list(map(lambda x, y: round(x * y, 2), lst1, lst2))


def getMeanScore(stuffScoreLst: list) -> list:
    """
    [[],[]] -> []
    return allLV3.mean() list"""
    if not stuffScoreLst:
        return []
    # get the mean list of stuffScoreLst
    res = []
    for i in range(len(stuffScoreLst[0])):
        # TODO: IndexError: list index out of range
        res.append(sum([stu[i] for stu in stuffScoreLst]) / len(stuffScoreLst))
    return res


def getScoreWithLv(staffWithLv):
    """ 从staffWithLv中得到scoreWithLv
    data PreProcess, get the score of each department"""
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
        res.append(sum(unitLst))  # 加入本单元求和
    res.append(sum(lv3ScoreLst))
    return res  # 插入总分数


def getSht1WithLv(scoreWithLv: dict) -> dict:
    """
    每个三级部门求平均，及每个二级部门的平均
    统计每个二级单位下所有人的分数"""
    sht1WithLv = {}
    for lv2 in scoreWithLv:
        allLv3 = []
        sht1WithLv.update({lv2: {}})

        # 每个三级部门求平均
        for lv3 in scoreWithLv[lv2]:
            allLv3 += scoreWithLv[lv2][lv3]
            sht1WithLv[lv2].update({lv3: getMeanScore(scoreWithLv[lv2][lv3])})

        # 每个二级部门的所有人平均
        allLv3Mean = getMeanScore(allLv3)  #
        sht1WithLv[lv2].update({"二级单位": allLv3Mean})  #
    # 对每个二级单位求平均
    # for lv2 in sht1WithLv:
    #     sht1WithLv[lv2].update({"二级单位": getMeanScore(list(sht1WithLv[lv2].values()))})
    return sht1WithLv


def getSht2WithLv(sht1WithLv: dict, lv2UnitSpan: list, lv1IndexSpan: list, sht2WgtLst: list) -> dict:
    """
    得到Sheet2中的数据,对指定单元格的分数进行求和 * 权重  以及新增部分求和
    :param sht1WithLv: 从sheet1中获取的数据 [1,2,3 ... , 30]
    :param lv2UnitSpan: 二级指标的单元格范围 [ [1,3], [ 4, 8], [20, 30] ]
    :param lv1IndexSpan: 一级指标的单元格范围 [ [1, 3], [7, 10] ]
    :param sht2WgtLst: sheet2中的权重
    :return: sheet2中的数据{lv2:[1, 2, 3, 4, sum, 5, 6, 7, 8, sum, sum]}
    """
    # TODO:  本线条排名计算 & 全公司排名计算
    # TODO: 第一个单元合计之后，生成的位置应该在靠前一个 2022-10-7
    sht2WithLv = {}
    for lv2 in sht1WithLv:
        sht2WithLv.update({lv2: {}})
        for lv3 in sht1WithLv[lv2]:
            title = lv3 if lv3 != "二级单位" else "二级单位成绩"  # Rename
            lv2IndexUnitScore = sumLv2IndexUnitScoreByWgt(sht1WithLv[lv2][lv3], lv2UnitSpan, sht2WgtLst)
            lv1IndexUnitScore = sht2SumLv1IndexUnitScore(lv2IndexUnitScore, lv1IndexSpan)
            sht2WithLv[lv2].update({title: lv1IndexUnitScore})
    return sht2WithLv


def getSht3WithLv(sht1WithLv: dict, lv1Name: str) -> dict:
    """得到sheet3中的数据
    从Sheet1 中获取所有二级单位的分数"""
    sht3WithLv = {}
    allLv2 = []
    for lv2 in sht1WithLv:
        sht3WithLv.update({lv2: sht1WithLv[lv2]['二级单位']})
        allLv2.append(sht1WithLv[lv2]['二级单位'])
    allLv2Mean = getMeanScore(allLv2)
    sht3WithLv.update({lv1Name: allLv2Mean})
    return sht3WithLv


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
        sht4WithLv.update({currClass[0]:
                               {currClass[1]: sht2WithLv[lv2]['二级单位成绩']}})
        allLv2.append(sht2WithLv[lv2]['二级单位成绩'])

    # 对每个部门分类求平均分
    for class_lv2 in sht4WithLv:
        sht4WithLv[class_lv2].update({"平均分": getMeanScore(list(sht4WithLv[class_lv2].values()))})
    # 对所有二级单位求平均分
    sht4WithLv.update({lv1Name: {"平均分": getMeanScore(allLv2)}})
    return sht4WithLv


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
        sht4Hie.append([clazz, row[1].strip("\n")])
    return sht4Hie


def resetUnitSum(sht, sht2UnitScp, weightCol):
    """
    重置Sheet2中的单元格权重 = 与其他几个单元格的和
    reset the weight of sheet2 equal to the sum of other cells
    :param startRow:
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


def getDeptUnit(shtModule, scp) -> Dict[Optional[Any], List[Union[int, str, None]]]:
    """
    获取分类的区间，以便裁剪sheet
    {分类: ["F", "P"], ... }"""
    clsScp = {}
    titleRan = getTltColRange(scp)
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
                clsScp.update({lastClz: clazz})
                clazz = [-1, -1]
            clazz[0] = colLtr
            lastClz = cls
        lastLtr = colLtr
    clazz[1] = lastLtr
    clsScp.update({lastClz: clazz})
    return clsScp


def sumLv2IndexUnitScoreByWgt(lv3ScoreLst: list, lv2Unit: list, sht2_wgt: list):
    """
    计算核心合并单元的分数
    [0, 1,2,3,4,5,6] & [0,1],[2,4],[6,6] * [0.2, 0.3, 0.5]
    -> [0+1, 2+4, 6]
    : params lv3ScoreLst: 分数序列（多少个问题就有多少个分数）
    : params lv2Unit: 分数求和范围（单元格范围）"""
    if not lv3ScoreLst:
        return []
    res = []
    for unitScp in lv2Unit:  # 添加每个单元的分数
        if unitScp[0] == unitScp[1]:  # 若单元只有一个单元格，则直接添加分数
            # TODO: 为什么这里判分的数据长度与单元格不匹配 - why the length of score is not equal to the length of unit
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
            sum(lv3ScoreLst[unitScp[0]:endBound]))
    return listMultipy(res, sht2_wgt)


def getSht2WgtLst(sht2_lv2Score) -> list:
    """
    获取Sheet2中的权重列表
    :param sht2_lv2Score:
    :return:
    """
    # 通过权重计算得到sht2WithLv TODO: 把参数抽调上去
    sht2WgtLstScp = "C3:C" + str(sht2_lv2Score.used_range.last_cell.row)
    sht2WgtLst = sht2_lv2Score.range(sht2WgtLstScp).value
    # # pop掉最后一个空值 - pop out the last empty value
    # for i in range(len(sht2WgtLst) - 1, -1, -1):
    #     if sht2WgtLst[i] is None:
    #         sht2WgtLst.pop(i)
    return sht2WgtLst


def clacSheet2_surveyGrade(sht1_lv2Result, sht2_lv2Score, sht1WithLv, lv1UnitScp):
    """
    通过sht1的值 与 权重， 计算sheet2的分数。 原数据[1,2..., 30]
    calculate the score of the sht2_lv2Score
    :param lv1UnitScp:
    :param sht1_lv2Result: sheet1
    :param sht2_lv2Score: sheet2
    :param sht1WithLv:
    :return:
    """
    print("开始计算sheet2数据，准备获取页面值")
    sht2WgtLst = getSht2WgtLst(sht2_lv2Score)
    print(f"获得 sht2 权重: {sht2WgtLst}, weight")
    assert None not in sht2WgtLst, "权重列表中存在空值"
    lv2UnitSpan = getShtUnitScp(sht1_lv2Result, startRow=3, endRow=40,
                                unitCol="B", contentCol="D",
                                skipCol="A", skipWords=["党廉", "纪检"])
    # lv1UnitSpan = getShtUnitScp(sht2_lv2Score, startRow=3, endRow=40,
    #                             unitCol="A", contentCol="B")
    sht2WithLv = getSht2WithLv(sht1WithLv, lv2UnitSpan, lv1UnitScp, sht2WgtLst)
    return sht2WithLv
