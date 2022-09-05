#  Author : Github: @GWillS163
#  Time: $(Date)
from lib import *
import pandas as pd
from shtDataCalc import listMultipy, sht1_calculate


# self.sht1Module, sht1_lv2Result, staffWithLv, self.sht1MdlTltScope, sht1Start
def sht1PlcScoreByPD(sht1Module, sht1, staffWithLv, sht1MdlTltScope, sht1Start):
    titleMatrix = sht1Module.range(sht1MdlTltScope).value
    # titleMatrix = sht1_lv2Result.range(self.sht1ModuleTltScope).value
    titleDf = pd.DataFrame(titleMatrix)
    sht1Value = sht1_calculate(staffWithLv, titleDf)
    sht1ValueDf = pd.DataFrame(sht1Value).transpose()
    # place sht1ValueDf to sht1_lv2Result at dataStart without index column
    sht1.range(sht1Start).value = sht1ValueDf.reset_index(drop=True)
    # get sht1ValueDf without column name by method reset_index(drop=True)

    # delete range G3:G6 and fill by right value
    sht1.range("G3:G33").api.Delete()
    sht1.range("G3:KZ3").api.Delete()


def sht2SetColumnTitle(srcSht, desSht, sht1_moduleSht, columnScope, titleStart="D1"):
    """Sheet2 表头和侧栏部分处理"""
    # Step2: copy left column the surveySht to sht1, with style
    shtCopyTo(srcSht, columnScope, desSht, columnScope.split(":")[0])

    # Step2.1: delete the row of left column redundant
    deleteRowLst = [31, 29, 27, 24, 18, 17, 15, 14, 13, 12, 11, 8, 5]
    for row in deleteRowLst:
        desSht.range(f"B{row}").api.EntireRow.Delete()
    desSht.range("B1").column_width = 18.8

    # Step2.2 delete the column C to I
    desSht.range("C1:J1").api.EntireColumn.Delete()
    desSht.range("A14:A19").api.EntireRow.Delete()
    # TODO: 两个单元格可能需要动态的

    # Step3: copy title
    shtCopyTo(sht1_moduleSht, "D1:L2", desSht, titleStart)


def sht2DeleteRows(sht2_lv2Score, deleteRowLst):
    """ delete the row of left column redundantly, reserve unit for one row """
    for row in deleteRowLst:
        sht2_lv2Score.range(f"B{row}").api.EntireRow.Delete()
    sht2_lv2Score.range("B1").column_width = 18.8
    # Step2.2 delete the C to I column
    sht2_lv2Score.range("C1:I1").api.EntireColumn.Delete()
    sht2_lv2Score.range("A14:A19").api.EntireRow.Delete()


def sht2GetUnitScp(sht2_lv2Score):
    """获取每个单位的范围"""
    unitScp = {}

    return unitScp


def sht2CalcSummary(sht2_lv2Score, sht2WithLv, row, startCol, endCol):
    unitScoreSum = 0
    while True:
        unit = sht2_lv2Score.range(f"A{row}").value
        unitScoreSum += sht2_lv2Score.range(f"{startCol}{row-1}").value
        if unit:
            break
    sht2_lv2Score.range(f"{startCol}{row}").value = unitScoreSum


def sht2OprAddSummaryRows(sht2_lv2Score):
    """add summary rows to sheet2"""
    # TODO: 并且要计算出每个单元格的值
    insertRow = []
    for row in range(4, 20):
        unit = sht2_lv2Score.range(f"A{row}").value
        ques = sht2_lv2Score.range(f"B{row}").value
        if not ques:
            if not unit:
                insertRow.append(row)
                break
            continue
        if unit:
            insertRow.append(row)

    while insertRow:
        row = insertRow.pop()
        sht2_lv2Score.range(f"A{row}").api.EntireRow.Insert()
        sht2_lv2Score.range(f"B{row}").value = "合计"
        # TODO: 计算合计值
        fillSht2SumOneLine(sht2_lv2Score, row, "D:L")
        # sht2CalcSummary(sht2_lv2Score, sht2WithLv, row, "C", "L")


def fillSht2SumOneLine(sht2, summaryRow, summaryScp, unitCol="A"):
    """ 负责填充一行的“合计”
    :param unitCol: 用来判断单元格大小
    :param summaryScp: "D:L"
    :param summaryRow: C
    :param sht2:"""
    # get unit top scope
    unitRow = summaryRow
    while True:
        unitRow -= 1
        print(unitRow)
        if sht2.range(f"{unitCol}{unitRow}").value:
            break
    # Fill one Line
    fillRan = getTltColRange(summaryScp)
    for colNum in fillRan:
        colLtr = getColLtr(colNum)
        sht2.range(f"{colLtr}{summaryRow}").value = \
            f"=SUM({colLtr}{unitRow}:{colLtr}{summaryRow-1})"


def sht2SetData(sht2_lv2Score, sht2WithLv, titleRange, wgtLst):
    """
    Sheet2 中，纵向放入 每个lv3部门的数据(如果有) * 该lv3部门的权重
    :param sht2_lv2Score:
    :param sht2WithLv:
    :param titleRange:
    :param wgtLst:
    :return:
    """
    titleRan = getTltColRange(titleRange)
    lastLv2 = None
    for col in titleRan:
        colLtr = getColLtr(col)
        lv2 = sht2_lv2Score.range(f"{colLtr}1").value
        lv3 = sht2_lv2Score.range(f"{colLtr}2").value
        if lv2:
            lastLv2 = lv2
        print(f"{lastLv2}:{lv3}", end=" ")
        if not lastLv2 in sht2WithLv:
            print(f" lv2不存在")
            continue
        if not lv3 in sht2WithLv[lastLv2]:
            print(f" lv3不存在")
            continue
        # print(f" ! 存在")
        # if lv3 in sht2WithLv:
        # place score list vertically
        # TODO: 这里会获取总计的百分比 NOne [0.1, 0.05, 0.0, 0.1, 0.1, 0.025, 0.1, None, 0.05, 0.05, 0.05]
        sht2_lv2Score.range(f"{colLtr}3").options(transpose=True).value = sht2WithLv[lastLv2][lv3]


def shtCopyTo(sht1, sht1Scp, sht2, sht2Start):
    sht1.range(sht1Scp).api.Copy()
    sht2.range(sht2Start).api.Select()
    # Cells(1, 1).Select
    sht2.api.Paste()


def sht4AddTitleIndex(sht2_lv2Score, sht4, moduleSht4):
    """Sheet4 表头和侧栏部分处理"""
    shtCopyTo(sht2_lv2Score, 'A4:B52', sht4, 'A4')
