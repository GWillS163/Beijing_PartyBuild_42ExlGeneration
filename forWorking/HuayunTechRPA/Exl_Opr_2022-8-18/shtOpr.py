#  Author : Github: @GWillS163
#  Time: $(Date)


def sht2PlcScore(sht2_lv2Score, score, row, col):
    for ss in score:
        sht2_lv2Score.range(f"{col}{row}").value = ss
        row += 1


def findLv3Pos(sht1_lv2Result, startRow, startCol):
    pass


def sht2OprPlcLv3(sht2_lv2Score, param, param1):
    pass


def sht2SetTitleIndex(srcSht, desSht, sht1_moduleSht, columnScope="A1:J32", titleStart="D1"):
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


def shtCopyTo(sht1, sht1Scp, sht2, sht2Start):
    sht1.range(sht1Scp).api.Copy()
    sht2.range(sht2Start).api.Select()
    sht2.api.Paste()


def sht2DeleteRows(sht2_lv2Score, deleteRowLst):
    """ delete the row of left column redundantly, reserve unit for one row """
    for row in deleteRowLst:
        sht2_lv2Score.range(f"B{row}").api.EntireRow.Delete()
    sht2_lv2Score.range("B1").column_width = 18.8
    # Step2.2 delete the C to I column
    sht2_lv2Score.range("C1:I1").api.EntireColumn.Delete()
    sht2_lv2Score.range("A14:A19").api.EntireRow.Delete()


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


def sht4AddTitleIndex(sht2_lv2Score, sht4, moduleSht4):
    """Sheet4 表头和侧栏部分处理"""
    sht2_lv2Score.api.Range('A1:C15').Copy()
    sht4.api.Range('A1').PasteSpecial(Transpose=True)
    moduleSht4.api.Range('A4:B52').Copy()
    sht4.api.Range('A4').Select()
    sht4.api.Paste()


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

