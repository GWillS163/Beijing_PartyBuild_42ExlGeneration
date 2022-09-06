#  Author : Github: @GWillS163
#  Time: $(Date)
import pandas as pd

from shtDataCalc import getMeanScore
from shtOperation import shtCopyTo


def sht2DeleteRows(sht2_lv2Score, deleteRowLst):
    """ delete the row of left column redundantly, reserve unit for one row """
    for row in deleteRowLst:
        sht2_lv2Score.range(f"B{row}").api.EntireRow.Delete()
    sht2_lv2Score.range("B1").column_width = 18.8
    # Step2.2 delete the column C to I
    sht2_lv2Score.range("C1:I1").api.EntireColumn.Delete()
    sht2_lv2Score.range("A14:A19").api.EntireRow.Delete()


# self.sht1Module, sht1_lv2Result, staffWithLv, self.sht1MdlTltScope, sht1Start
def sht1PlcScoreByPD(sht1Module, sht1, staffWithLv, sht1MdlTltScope, sht1Start, answerLen):
    titleMatrix = sht1Module.range(sht1MdlTltScope).value
    # titleMatrix = sht1_lv2Result.range(self.sht1ModuleTltScope).value
    titleDf = pd.DataFrame(titleMatrix)
    sht1Value = sht1_calculateByPD(staffWithLv, titleDf, answerLen)
    sht1ValueDf = pd.DataFrame(sht1Value).transpose()
    # place sht1ValueDf to sht1_lv2Result at dataStart without index column
    sht1.range(sht1Start).value = sht1ValueDf.reset_index(drop=True)
    # get sht1ValueDf without column name by method reset_index(drop=True)

    # delete range G3:G6 and fill by right value
    sht1.range("G3:G33").api.Delete()
    sht1.range("G3:KZ3").api.Delete()



def findLv3Pos(sht1_lv2Result, startRow, startCol):
    pass


def sht2OprPlcLv3(sht2_lv2Score, param, param1):
    pass

# def sht2SetScore(sht2_lv2Score, allUnitScore, sht2ScrCol,
#                  sht2UntCol="B", sht2WgtCol="C"):
    """
    遍历每个Unit 逐个放入Unit相应的分数
    :param sht2_lv2Score: sheet2
    :param allUnitScore: {"分1": 28}
    :param sht2ScrCol:
    :param sht2UntCol:
    :param sht2WgtCol:
    :return: None
    """
    # for row in range(3, 40):
    #     currUnit = sht2_lv2Score.range(f"{sht2UntCol}{row}").value
    #     if not currUnit:
    #         break
    #     if currUnit not in allUnitScore:
    #         continue
    #     wgt = sht2_lv2Score.range(f"{sht2WgtCol}{row}").value
    #     sht2_lv2Score.range(f"{sht2ScrCol}{row}").value = allUnitScore[currUnit] * wgt

def sht2GetSht1ScoreCol(sht1_lv2Result, getSht1Col):
    """
    Sheet2 按行得到 sheet1 中的分数列
    sheet 2 get Unit score single column"""
    unit = None
    allUnitScore = {}
    for row in range(3, 40):
        currUnit = sht1_lv2Result.range(f"B{row}").value
        if currUnit:
            unit = currUnit
            allUnitScore.update({unit: 0})
        currScore = sht1_lv2Result.range(f"{getSht1Col}{row}").value  # 变量
        if not currScore:
            currScore = 0
        allUnitScore[unit] += currScore
    return allUnitScore


def sht1_calculateByPD(staffWithLv, titleDf, answerLen):
    """
    calculate the score of sheet1
    :param answerLen:
    :param titleDf:
    :param staffWithLv:
    :return:
    """
    currentLv2 = None
    allInfo = []
    debugTitle = []
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

        # print(f"{currentLv2} {currentLv3} process")
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

def mergeSht2SummarizeCells(sht2_WithWeight, mergeCells, columns):
    columnLst = []
    if type(columns) == str:
        columnLst.append(columns)
    elif type(columns) == list:
        columnLst = columns
    else:
        raise Exception("the parameter columns type error, should be String or list")
    for column in columnLst:
        # show the merged cells gradually with step 2
        for i in range(0, len(mergeCells), 2):
            # print(mergeCells[i:i + 1])
            sht2_WithWeight.range(f"{column}{mergeCells[i]}:{column}{mergeCells[i + 1]}").merge()


def placeDepartmentTitle(sht, departmentLst, titleStart="K1"):
    """
    place the department title in the sht
    :param sht:
    :param departmentLst:
    :param titleStart:
    :return:
    """
    sht.range(titleStart).value = departmentLst
    # get merge info
    startRow = titleStart[1]
    endLetter = chr(ord(titleStart[0]) + len(departmentLst[1]) - 1)
    # merge K1:L1 cells
    # TODO: record index position
    sht.range(f"{titleStart}:{endLetter}{startRow}").merge()


def mergeSht2Lv3Title(sht2_WithWeight, departmentLen, startLv2="C2"):
    """
    merge the title of the third level in the sht2.
    Need Concern about Multi-department situation.
    :param startLv2:
    :param sht2_WithWeight:
    :param departmentLen:
    :return:
    """
    startCol = startLv2[0]
    startRow = startLv2[1]
    for gap in range(0, departmentLen + 1, 2):
        startRowLetter = chr(ord(startCol) + gap)
        endRowLetter = chr(ord(startRowLetter) + 1)
        # print(f"{startRowLetter}{startRow}:"
        #       f"{endRowLetter}{startRow}")
        sht2_WithWeight.range(f"{startRowLetter}{startRow}:"
                              f"{endRowLetter}{startRow}").merge()


def sht4AddTitleIndex(sht2_lv2Score, sht4, moduleSht4):
    """Sheet4 表头和侧栏部分处理"""
    shtCopyTo(sht2_lv2Score, 'A4:B52', sht4, 'A4')