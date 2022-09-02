#  Author : Github: @GWillS163
#  Time: $(Date)
import numpy as np
import pandas as pd


def getMeanScore(stuffScoreLst):
    """return allLV3.mean() list"""
    df = pd.DataFrame(stuffScoreLst).transpose()
    return df.mean(axis=1).tolist()


def getScoreWithLv(staffWithLv):
    """data PreProcess, get the score of each department"""
    scoreWithLv = {}
    for lv2 in staffWithLv:
        scoreWithLv[lv2] = {}
        for lv3 in staffWithLv[lv2]:
            scoreWithLv[lv2][lv3] = [stu.scoreLst for stu in staffWithLv[lv2][lv3]]
    return scoreWithLv


def getSht1WithLv(scoreWithLv_):
    """统计每个二级单位下所有人的分数"""
    Sht1WithLv = {}
    for lv2 in scoreWithLv_:
        allLv3 = []
        Sht1WithLv.update({lv2: {}})
        for lv3 in scoreWithLv_[lv2]:
            Sht1WithLv[lv2].update({lv3: getMeanScore(scoreWithLv_[lv2][lv3])})
            allLv3 += scoreWithLv_[lv2][lv3]
        allLv3Mean = getMeanScore(allLv3)
        Sht1WithLv[lv2].update({"二级单位": allLv3Mean})
    return Sht1WithLv


def sht1_calculate(staffWithLv, titleDf, answerLen=30):
    """
    calculate the score of sheet1
    :param titleDf:
    :param staffWithLv:
    :return:
    """
    currentLv2 = None
    allInfo = []
    debugTitle = []
    skipLv2 = []
    for colI in titleDf:
        if titleDf[colI][0]:
            currentLv2 = titleDf[colI][0]
        currentLv3 = titleDf[colI][1]
        # scoreWithLv[lv1][lv2] - > [[], [], ...]
        # stuffWithLv[lv1][lv2] - > [stu1, stu2, ...]  -> [stu.scoreLst for stu in stuffWithLv[lv2][lv3]]
        # print(f"{currentLv2}:{currentLv3}")

        if currentLv2 not in staffWithLv:  # 检查是否有该lv2
            allInfo.append([np.nan for _ in range(answerLen)])
            debugTitle.append(currentLv3)
            continue
        if currentLv3 not in staffWithLv[currentLv2]:  # 检查是否有该lv3
            allInfo.append([np.nan for _ in range(answerLen)])
            debugTitle.append(currentLv3)
            continue

        print(f"{currentLv2} {currentLv3} process")
        currentColRes = []
        # "二级部门" 单独处理
        if currentLv3 == "二级部门":
            for lv3 in staffWithLv[currentLv2]:
                currentColRes += list(map(lambda x: x.scoreLst, staffWithLv[currentLv2][lv3]))
                # allLv3OfLv2 += [stu.scoreLst for stu in stuffScoreWithLv[currentLv2][lv3]]
        else:
            # operate each score column of departments
            currentColRes = [stu.scoreLst for stu in staffWithLv[currentLv2][currentLv3]]
        # allInfo.update({currentLv3: getMeanScore(currentColRes)})
        allInfo.append(getMeanScore(currentColRes))
    # allInfoDf = pd.DataFrame(allInfo)
    return allInfo
    # scoreWithLv[lv2][lv3] - > [[], [], ...]
    # stuffWithLv[lv2][lv3] - > [stu1, stu2, ...]  -> [stu.scoreLst for stu in stuffWithLv[lv2][lv3]]


def getSht2Lv2UnitScope(sht2):
    """ get unit Span for Sheet2
    跳过党廉 and 纪检
    :return:  [[0, 0], [1, 2], [3, 3], [4, 5] ...
    """
    # get merge cells scope dynamically
    resultSpan = []
    tempScp = [-1, -1]
    n = 0
    adds = 3
    while n < 40:
        part = sht2.range(f"A{n + adds}").value
        unit = sht2.range(f"B{n + adds}").value
        content = sht2.range(f"D{n + adds}").value
        if part and "党廉" == part or "纪检" == part:
            resultSpan.append(tempScp)
            break
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


def getSht2WithLv(scoreWithLv, lv2Unit):
    """对指定单元格的分数进行求和处理"""
    sht2WithLv = {}
    for lv2 in scoreWithLv:
        sht2WithLv.update({lv2: []})
        for unitScp in lv2Unit:
            sht2WithLv[lv2].append(sum(scoreWithLv[lv2]["二级单位"][unitScp[0]:unitScp[1] + 1]))
    return sht2WithLv


def getSht3WithLv(sht1WithLv):
    """从Sheet1 中获取所有二级单位的分数"""
    sht3WithLv = {}
    for lv2 in sht1WithLv:
        sht3WithLv.update({lv2: sht1WithLv[lv2]['二级单位']})
    return sht3WithLv
