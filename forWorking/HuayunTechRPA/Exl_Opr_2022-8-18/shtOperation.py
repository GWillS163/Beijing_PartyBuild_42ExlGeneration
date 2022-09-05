#  Author : Github: @GWillS163
#  Time: $(Date)


def sht2SetColumnTitle(srcSht, desSht, sht1_moduleSht, columnScope="A1:J32", titleStart="D1"):
    """Sheet2 表头和侧栏部分处理"""
    # Step2: copy left column the surveySht to sht1, with style
    srcSht.range(columnScope).api.Copy()
    desSht.range(columnScope.split(":")[0]).api.Select()
    desSht.api.Paste()

    # Step2.1: delete the row of left column redundantly
    deleteRowLst = [31, 29, 27, 24, 18, 17, 15, 14, 13, 12, 11, 8, 5]
    for row in deleteRowLst:
        desSht.range(f"B{row}").api.EntireRow.Delete()
    desSht.range("B1").column_width = 18.8
    # Step2.2 delete the C to I  column
    desSht.range("C1:I1").api.EntireColumn.Delete()
    desSht.range("A14:A19").api.EntireRow.Delete()

    # Step3: copy title
    sht1_moduleSht.range("D1:L2").api.Copy()
    desSht.range(titleStart).api.Select()
    desSht.api.Paste()


def sht2SetScore(sht2_lv2Score, allUnitScore, sht2ScrCol,
                 sht2UntCol="B", sht2WgtCol="C"):
    """
    遍历每个Unit 逐个放入Unit相应的分数
    :param sht2_lv2Score: sheet2
    :param allUnitScore: {"分1": 28}
    :param sht2ScrCol:
    :param sht2UntCol:
    :param sht2WgtCol:
    :return: None
    """
    for row in range(3, 40):
        currUnit = sht2_lv2Score.range(f"{sht2UntCol}{row}").value
        if not currUnit:
            break
        if currUnit not in allUnitScore:
            continue
        wgt = sht2_lv2Score.range(f"{sht2WgtCol}{row}").value
        sht2_lv2Score.range(f"{sht2ScrCol}{row}").value = allUnitScore[currUnit] * wgt


def sht2PlcScore(sht2_lv2Score, score, row, col):
    for ss in score:
        sht2_lv2Score.range(f"{col}{row}").value = ss
        row += 1


def sht2OprAddSummaryRows(sht2_lv2Score, sht2WithLv):
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


def sht2GetScoreCol(sht1_lv2Result, getSht1Col):
    """sheet 2 get Unit score single column and """
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


def sht2DeleteRows(sht2_lv2Score, deleteRowLst):
    """ delete the row of left column redundantly, reserve unit for one row """
    for row in deleteRowLst:
        sht2_lv2Score.range(f"B{row}").api.EntireRow.Delete()
    sht2_lv2Score.range("B1").column_width = 18.8
    # Step2.2 delete the C to I column
    sht2_lv2Score.range("C1:I1").api.EntireColumn.Delete()
    sht2_lv2Score.range("A14:A19").api.EntireRow.Delete()


def shtCopyTo(sht1, sht1Scp, sht2, sht2Start):
    sht1.range(sht1Scp).api.Copy()
    sht2.range(sht2Start).api.Select()
    sht2.api.Paste()


def sht4AddTitleIndex(sht2_lv2Score, sht4, moduleSht4):
    """Sheet4 表头和侧栏部分处理"""

    moduleSht4.api.Range('A4:B52').Copy()
    sht4.api.Range('A4').Select()
    sht4.api.Paste()