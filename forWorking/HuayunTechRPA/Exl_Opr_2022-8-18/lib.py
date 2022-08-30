#  Author : Github: @GWillS163
#  Time: $(Date)
import re


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


def judgeGradeSingle(answerIntLst, debugPrint, ruleSelect, ruleScore):
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


def judgeGradeMulti(answerIntLst, debugPrint, ruleSelect, ruleScore):
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
    debugPrint = f"answer: {answer}\n"\
                 f"rule: {rule}\n"\
                  f"quesType: {quesType}"
    # match the number of digital in answer by regex, form is a number+分
    answerInt = re.findall(r"(\d{,3}?)分", answer.strip())
    if answerInt and answerInt[0]:
        return int(answerInt[0])

    if "开放题" in quesType:
        return 0

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
            score = judgeGradeSingle(answerIntLst, debugPrint, ruleSelect, ruleScore)
        elif "不定项" in quesType:
            score = judgeGradeMulti(answerIntLst, debugPrint, ruleSelect, ruleScore)

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
