#  Author : Github: @GWillS163
#  Time: $(Date)
import re
import pandas as pd
import numpy as np


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


def getNoneColDf(col, row):
    """return a df with all columns are None"""
    currentColResDf = pd.DataFrame([pd.NA for _ in range(length)]).transpose()
    # generate NA df with row and col
    pd.empty((row, col))
    return currentColResDf


def getColLtr(colNum) -> str:
    """0 -> A, 1 -> B, 2 -> C, ..."""
    if colNum > 27 * 26 - 1:  # 大于ZZ 不考虑
        return ""
    first = chr(colNum // 26 + (65 - 1)) if colNum > 25 else ""
    second = chr(colNum % 26 + 65)
    return first + second


def getColNum(colLetter) -> int:
    """A -> 0, B -> 1, C -> 2, ... KZ -> 285"""
    if len(colLetter) == 1:
        return ord(colLetter) - 65
    else:
        return (ord(colLetter[0]) - 65) * 26 + ord(colLetter[1]) - 65


def getTltColRange(titleScope):
    """titleScope : A1:B2, in other words is ColA to Col B
    return iterable Range"""
    titleStart, titleEnd = titleScope.split(":")
    # get the letter of titleStart by regex
    titleStartLetter = re.findall(r"[A-Z]+", titleStart)[0]
    titleEndLetter = re.findall(r"[A-Z]+", titleEnd)[0]
    # convert to number
    titleStartLetterNum = getColNum(titleStartLetter)
    titleEndLetterNum = getColNum(titleEndLetter)
    return range(titleStartLetterNum, titleEndLetterNum)


def getMeanScore(stuffScoreLst):
    """return allLV3.mean() list"""
    df = pd.DataFrame(stuffScoreLst).transpose()
    return df.mean(axis=1).tolist()


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

    while insertRow:
        row = insertRow.pop()
        sht2_lv2Score.range(f"A{row}").api.EntireRow.Insert()
        sht2_lv2Score.range(f"B{row}").value = "合计"


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


def getMergeZoneDynamically(sht2_WithWeight):
    """
    for Sheet2
    :return:
    """
    # get merge cells scope dynamically
    mergeCells = []
    temp = None
    n = 3
    while True:
        if not sht2_WithWeight.range(f"B{n}").value:
            # print(temp)
            mergeCells.append(temp)
            break
        if sht2_WithWeight.range(f"A{n}").value:
            if temp:
                # print(temp)
                mergeCells.append(temp)
            # print(f"A{n}")
            mergeCells.append(n)
        else:
            temp = n
        n += 1
    return mergeCells


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


def judgeGradeSingle(answerIntLst, ruleSelect, ruleScore):
    # 1分:1
    # 2.2分
    # 9:9分
    # 10.10分
    if len(answerIntLst) != 1:
        # print("识别到的数字不止一个，请检查！", end="")
        # print(debugPrint)
        return -1

    # get the number in ruleSelect by regex
    numOfRuleDig = re.search(r"(\d{,3})([-|或])?(\d{,3})?", ruleSelect).groups()
    if not numOfRuleDig[1]:  # only one number
        if answerIntLst[0] == int(numOfRuleDig[0]):
            return ruleScore
    else:  # present scope or "或"
        if numOfRuleDig[1] == "或":
            if answerIntLst[0] == int(numOfRuleDig[0]) or answerIntLst[0] == int(numOfRuleDig[2]):
                return ruleScore
        elif numOfRuleDig[1] == "-":
            if int(numOfRuleDig[0]) <= answerIntLst[0] <= int(numOfRuleDig[2]):
                return ruleScore

    return -1


def judgeGradeMulti(answerIntLst, ruleSelect, ruleScore):
    # 已覆盖效果 (2022-8-29)
    # 单个选择: 10分：4
    # 单个任意: 10分：4或5
    # 全部选择: 8分：全选
    # 局部全选: 8分：1-4
    # 局部全选: 0分：1-4全选
    # 全局多选: 任选3个
    # 局部多选: 1-4任选3个
    # 局部多选以上: 1-4任选3个及以上

    # 识别效果(下行为标题):
    # 单选，4或5, 选择范围开始, 选择范围结束, 全选，任选，n个，n个及以上
    # ('4', None, None, None, None, None, None, None)
    # (None, '4或5', None, None, None, None, None, None)
    # (None, '4或5或20', None, None, None, None, None, None)
    # (None, None, None, None, '全选', None, None, None)
    # (None, None, '1', '4', None, None, None, None)
    # (None, None, '1', '4', '全选', None, None, None)
    # (None, None, None, None, None, '任选', '3', None)
    # (None, None, '1', '4', None, '任选', '3', None)
    # (None, None, '1', '4', None, '任选', '3', '及以上')

    # write a regex to identify above case
    scopeRan = re.search(
        r"(^\d{,3})$|(^\d{,3}(?:或\d{,3})+$)|(?:^(\d{,3})-(\d{,3}))?(?:(全选)|(任选)(\d{,3})-?(\d{,3})?个)?(及以上)?",
        ruleSelect).groups()
    sglSlt, dblSlts, permitNumStart, permitNumEnd, isAllSlt, isAnySlt, permitQtyMin, permitQtyMax, isMore = scopeRan

    # judge each score if is not in permit scope
    if not permitNumStart and not permitNumEnd:
        permitNumStart, permitNumEnd = 1, 99  # default
    else:
        permitScp = range(int(permitNumStart), int(permitNumEnd) + 1)
        isInScope = False
        for num in answerIntLst:
            if int(num) in permitScp:
                isInScope = True
        if not isInScope:
            return -1

    # e.g. 单个选择的规则: 4
    if sglSlt and len(answerIntLst) == 1:
        if answerIntLst[0] == int(sglSlt):
            return ruleScore

    # 单个任选: e.g. 4或5, 一旦选了就给分
    elif dblSlts:
        permitNumLst = list(map(int, dblSlts.split("或")))
        # check some element of the answerIntLst is duplicate with permitNumLst
        for num in answerIntLst:
            if int(num) in permitNumLst:
                return ruleScore

    # 全部选择与部分全选:
    # e.g. 全选, 1-5, 1-5全选  (默认1-99)
    elif isAllSlt or (not isAllSlt and not isAnySlt):
        # return "多选 或部分全选"
        if not permitNumStart and permitNumEnd:
            print("全部选择与部分全选，需要指定范围！")
            return -1
            # TODO: 如何统计题目的数量
        # 选择的数量与范围一致
        if len(answerIntLst) == len(range(int(permitNumStart), int(permitNumEnd) + 1)):
            return ruleScore

    # 局部  (默认1-99)
    # 全局多选: 任选3个
    # 局部多选: 1-4任选3个
    # 局部多选: 1-4任选3-4个
    # 局部多选以上: 1-4任选3个及以上
    elif isAnySlt:
        # 判断数量是否足够
        # 匹配两种格式： 任选n(-m)个及以上
        if not permitQtyMax:
            permitQtyMax = permitQtyMin

        # 任选n个及以上
        if isMore:
            if len(answerIntLst) >= int(permitQtyMin):
                return ruleScore
        # 任选n(-m)个
        else:
            if int(permitQtyMin) <= len(answerIntLst) <= int(permitQtyMax):
                return ruleScore

    return -1


def judgeRulePreProcess(ruleP, debugPrint):
    ruleL, ruleR = 0, 0
    for char in [':', "：", "."]:
        if char in ruleP:
            ruleL, ruleR = ruleP.split(char)
            break

    if not (ruleL and ruleR):
        print("没有找到匹配的分隔字符，将处理为-1分 :")
        print(debugPrint)
        return -1, -1

    # get permit scope
    if "分" in ruleL:
        ruleScore = int(ruleL.strip("分"))
        ruleSelect = ruleR
    elif "分" in ruleR:
        ruleScore = int(ruleR.strip("分"))
        ruleSelect = ruleL
    else:
        print("无法分辨哪边是分数! 将处理为-1分 :", debugPrint)
        return -1, -1

    return ruleScore, ruleSelect


def judgeAnswerGrade(answer, rule, quesType):
    debugPrint = f"answer: {answer}\n" \
                 f"rule: {rule}\n" \
                 f"quesType: {quesType}"
    # match the number of digital in answer by regex, form is a number+分
    answerInt = re.findall(r"(\d{,3}?)分", answer.strip())
    if answerInt and answerInt[0]:
        return int(answerInt[0])

    if "开放题" in quesType:
        return 0
    elif "评分题" in quesType:
        return int(re.search(r"(\d{,3}?)", answer.strip()).groups()[0])

    # get RuleL & RuleR and verify
    answerIntLst = list(map(int, re.findall(r"(\d{,3})\..*?", answer)))
    # check each rule to answer
    for ruleP in rule.split("\n"):
        if not ruleP:
            continue
        ruleScore, ruleSelect = judgeRulePreProcess(ruleP, debugPrint)
        if ruleScore == -1 or ruleSelect == -1:
            continue

        # get answer scope with different type of ques
        score = -1
        if "单项" in quesType or "单选" in quesType:
            score = judgeGradeSingle(answerIntLst, ruleSelect, ruleScore)
        elif "不定项" in quesType:
            score = judgeGradeMulti(answerIntLst, ruleSelect, ruleScore)

        if score != -1:
            return score

    return -1


class Stuff:
    def __init__(self, name, lv2Depart, lv2Code, lv3Depart, lv3Code, ID, answerLst=None):
        self.name = name
        self.lv2Depart = lv2Depart
        self.lv2Code = lv2Code
        self.lv3Depart = lv3Depart
        self.lv3Code = lv3Code
        self.ID = ID
        self.answerLst = answerLst
        self.scoreLst = [0 for _ in range(len(answerLst))]

    def __str__(self):
        return f"{self.name} {self.lv2Depart} {self.lv2Code} {self.lv3Depart} {self.lv3Code} {self.ID} {self.answerLst}"

    def __repr__(self):
        return f"name:{self.name}, answerLen:{len(self.answerLst)}"  # lv2:{self.lv2Depart[:10]}, lv3:{self.lv3Depart[:10]},

def getLv3AvgScore(lv3ScoreLst):
    """
    Use Pandas [[],[],[]...] get the mean score of the department
    :param param:
    :return:
    """
    # TODO: use pandas
    pass


def sht2SetScore(sht2_lv2Score, allUnitScore, sht2ScrCol,
                 sht2UntCol="B", sht2WgtCol="C"):
    """遍历每个Unit 逐个放入Unit相应的分数"""
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

