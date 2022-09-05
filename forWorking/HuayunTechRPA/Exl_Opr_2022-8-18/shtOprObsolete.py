#  Author : Github: @GWillS163
#  Time: $(Date)


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

