#  Author : Github: @GWillS163
#  Time: $(Date)
# Description: 用于计算数据的模块
from typing import Dict, Optional, Any, List, Union

from lib import *
import numpy as np
import pandas as pd


def listMultipy(lst1, lst2):
    return list(map(lambda x, y: round(x * y, 2), lst1, lst2))


def getMeanScore(stuffScoreLst):
    """return allLV3.mean() list"""
    df = pd.DataFrame(stuffScoreLst).transpose()
    return df.mean(axis=1).tolist()


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
    :param lv3ScoreLst:[0.9, 0.4, 0.0, 1.1, 1.0, 1.15, 1.1, 0.2, 0.5, 0.5, 1.35]
    :param lv1IndexSpan: [[0, 6], [7, 10]]
    :return: [0.9, 0.4, 0.0, 1.1, 1.0, 1.15, 1.1, 【5.65】,
             0.2, 0.5, 0.5, 1.35, 【2.55】,
                                【8.20】]
    """
    if not lv3ScoreLst:
        return []
    res = []
    for unitScp in lv1IndexSpan:
        if not unitScp:
            continue
        unitLst = lv3ScoreLst[unitScp[0]:unitScp[1] + 1]
        res += unitLst  # 截取原分数
        res.append(sum(unitLst))  # 插入求和
    res.append(sum(lv3ScoreLst))
    return res  # 插入总分数


def getSht1WithLv(scoreWithLv_: dict) -> dict:
    """得到sheet1中的数据
    统计每个二级单位下所有人的分数"""
    sht1WithLv = {}
    for lv2 in scoreWithLv_:
        # allLv3 = []  #
        sht1WithLv.update({lv2: {}})
        for lv3 in scoreWithLv_[lv2]:
            sht1WithLv[lv2].update({lv3: getMeanScore(scoreWithLv_[lv2][lv3])})
        #     allLv3 += scoreWithLv_[lv2][lv3]
        # allLv3Mean = getMeanScore(allLv3)  #
        # sht1WithLv[lv2].update({"二级单位": allLv3Mean})  #
    # 对每个二级单位求平均
    for lv2 in sht1WithLv:
        sht1WithLv[lv2].update({"二级单位": getMeanScore(sht1WithLv[lv2].values())})

    return sht1WithLv


def getSht2WithLv(sht1WithLv: dict, lv2UnitSpan: list, lv1IndexSpan: list, sht2WgtLst: list) -> dict:
    """得到Sheet2中的数据
    对指定单元格的分数进行求和 * 权重  以及新增部分求和"""
    # TODO:  本线条排名计算 & 全公司排名计算
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
        sht4WithLv[class_lv2].update({"平均分": getMeanScore(sht4WithLv[class_lv2].values())})
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


def getShtUnitScp(sht, startRow, endRow, unitCol, contentCol, skipCol=None, skipWords=None):
    """ get unit Span for Sheet2
    以D列为最小单位，获取每个B列二级指标的单元范围
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
        if skipCol:
            part = sht.range(f"{skipCol}{n + startRow}").value
            # detect skip words if part equal skip words, thus skip this row
            if part in skipWords:
                n += 1
                continue
        unit = sht.range(f"{unitCol}{n + startRow}").value
        content = sht.range(f"{contentCol}{n + startRow}").value
        if not content:
            resultSpan.append(tempScp)
            break
        if unit:
            if tempScp != [-1, -1]:
                resultSpan.append(tempScp)
            tempScp = [n, n]
        else:
            tempScp[1] = n
        n += 1
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


def sumLv2IndexUnitScoreByWgt(lv3ScoreLst, lv2Unit, sht2_wgt):
    """
    计算核心合并单元的分数
    [0, 1,2,3,4,5,6] & [0,1],[2,4],[6,6] * [0.2, 0.3, 0.5]
    -> [0+1, 2+4, 6]"""
    if not lv3ScoreLst:
        return []
    res = []
    for unitScp in lv2Unit:
        if unitScp[0] == unitScp[1]:
            res.append(lv3ScoreLst[unitScp[0]])
            continue
        res.append(
            sum(lv3ScoreLst[unitScp[0]:unitScp[1] + 1]))
    return listMultipy(res, sht2_wgt)
