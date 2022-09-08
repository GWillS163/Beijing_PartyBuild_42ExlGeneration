#  Author : Github: @GWillS163
#  Time: $(Date)
# Description: 用于 添加数据，增加行列
from lib import *


def shtCopyTo(sht1, sht1Scp, sht2, sht2Start):
    sht1.range(sht1Scp).api.Copy()
    sht2.range(sht2Start).api.Select()
    # Cells(1, 1).Select
    sht2.api.Paste()


def sht2AddSummary(sht2_lv2Score, sht2WithLv, row, startCol, endCol):
    unitScoreSum = 0
    while True:
        unit = sht2_lv2Score.range(f"A{row}").value
        unitScoreSum += sht2_lv2Score.range(f"{startCol}{row - 1}").value
        if unit:
            break
    sht2_lv2Score.range(f"{startCol}{row}").value = unitScoreSum


def sht2OprAddSummaryRows(sht2_lv2Score):
    """add summary rows to sheet2"""
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

    sht2_lv2Score.range(f"A{insertRow[-1]}").api.EntireRow.Insert()
    sht2_lv2Score.range(f"B{insertRow[-1]}").value = "总计"
    while insertRow:
        row = insertRow.pop()
        sht2_lv2Score.range(f"A{row}").api.EntireRow.Insert()
        sht2_lv2Score.range(f"B{row}").value = "合计"
        fillSht2SumOneLine(sht2_lv2Score, row, "C:D")
        # 以下代码不需计算其他列的合计
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
            f"=SUM({colLtr}{unitRow}:{colLtr}{summaryRow - 1})"


def sht1SetData(sht1_lv2Result, sht1WithLv, titleRan):
    """
    Sheet1 中，纵向放入 每个lv2_3部门的数据(如果有) 包含“二级单位”
    :param titleRan:
    :param sht1_lv2Result:
    :param sht1WithLv:
    :return: None
    """
    lv2 = None
    for colNum in titleRan:
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
        sht1_lv2Result.range(f"{colLtr}3"). \
            options(transpose=True).value = sht1WithLv[lv2][lv3]


def sht2SetData(sht2_lv2Score, sht2WithLv, titleRan):
    """
    Sheet2 中，纵向放入 每个lv3部门的数据(如果有) * 该lv3部门的权重
    :param sht2_lv2Score:
    :param sht2WithLv:
    :return:
    """
    lv2 = None
    for colNum in titleRan:
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
        sht2_lv2Score.range(f"{colLtr}3").options(transpose=True).value = sht2WithLv[lv2][lv3]


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
    lv2Clz = None
    for col in titleRan:
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
        sht3.range(f"{colLtr}3").options(transpose=True).value = sht3WithLv[lv2]


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
        # place score list vertically
        sht4.range(f"C{row}").value = sht4WithLv[lv1][lv2]


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
    shtDept.activate()
    shtCopyTo(shtSum, sht1DataZone,
              shtDept, shtTitleTo)
    return sht1BorderL, sht1BorderR


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

