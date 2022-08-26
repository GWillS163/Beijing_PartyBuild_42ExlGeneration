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


def judgeAnswerGrade(answer, rule, type):
    if "开放题" in type:
        return 0
    elif "单项" in type or "单选" in type:
        # 1:1分
        # 2.2分
        # 9:9分
        # 10.10分

        # get the number of digital and dot by regex
        numOfAnswerDigitalList = re.findall(r"(\d{,3}?)\..*?", answer)
        if len(numOfAnswerDigitalList) != 1:
            print("识别到的数字不止一个，请检查！", end="")
            print(f"answer: {answer}")
            return 0
        for ruleP in rule.split("\n"):
            if not ruleP:
                continue
            if ":" in rule:
                ruleL, ruleR = ruleP.split(":")
            elif "：" in rule:
                ruleL, ruleR = ruleP.split("：")
            elif "." in rule:
                ruleL, ruleR = ruleP.split(".")
            else:
                print("没有找到匹配的规则，将处理为-1分 :")
                print(f"answer: {answer}\n"
                      f"rule: {rule}\n"
                      f"type: {type}")
                return -1
            # get permit scope
            if "分" in ruleL:
                ruleScore = int(ruleL.strip("分"))
                ruleSelect = ruleR
            elif "分" in ruleR:
                ruleScore = int(ruleR.strip("分"))
                ruleSelect = ruleL
            else:
                print("无法分辨哪边是分数! 将处理为-1分 :")
                print(f"answer: {answer}\n"
                      f"rule: {rule}\n"
                      f"type: {type}")
                return -1
            # get the number of digital in ruleSelect by regex
            numOfRuleDig = re.search(r"(\d{,3})-?(\d{,3})?", ruleSelect).groups()
            if not numOfRuleDig[1]:  # only one number
                if numOfAnswerDigitalList[0] == numOfRuleDig[0]:
                    return ruleScore
            else:  # two numbers
                if int(numOfAnswerDigitalList[0]) in range(int(numOfRuleDig[0]), int(numOfRuleDig[1]) + 1):
                    return ruleScore

        print("没有找到匹配的规则，将处理为-1分 :")
        print(f"answer: {answer}\n"
              f"rule: {rule}\n"
              f"type: {type}")
        return -1

    elif "不定项" in type:
        # 已适配规则:
        # 10分：1-4全选
        # 10分：1-6任选5个及以上
        # 8分：1-4任选3个
        # 8分：1-6任选3-4个
        # 0分：5

        # get the number of digital and dot by regex
        numOfAnswerDigitalList = re.findall(r"(\d{,3})\..*?", answer)
        # compare answerLst with standard answerLst
        for ruleP in rule.split("\n"):
            if not ruleP:
                continue
            scoreStr, scopeStr = ruleP.split("：")

            # judge the score if only digital
            if scopeStr.strip().isdigit():
                if scopeStr in numOfAnswerDigitalList:
                    return int(scoreStr.strip("分"))
                else:
                    print("[数字判断]无法处理此规则, 请检查！将处理为-1分 :", answer, rule, type)
                    return -1

            # get the two digit before "全选" by regex
            scopeRan = re.search(r"(?:(.*?)|"
                                 r"(\d{,3})-(\d{,3}))(.选)",
                                 scopeStr).groups()
            if scopeRan == ('', None, None, '全选'):

                startNum, endNum = re.findall(r"(\d{,3})-?(\d{,3})?.选", scopeStr)[0]
            else:
                startNum, endNum = 1, 99  # default
            permitScopeLst = range(int(startNum), int(endNum) + 1)

            # judge the score if is not permit scope
            isInScope = False
            for num in numOfAnswerDigitalList:
                if int(num) in permitScopeLst:
                    isInScope = True
            if not isInScope:
                continue
                # print(f"[不定项模式]答案({numOfAnswerDigitalList})出现了越界({ruleP}), 请检查！将处理为0分.\n"
                #       f"Answer:{answer}\n"
                #       f"rule:{rule},"
                #       f"type:{type}")
                # return 0

            # in scope
            if "全选" in scopeStr:
                if len(permitScopeLst) == len(numOfAnswerDigitalList):
                    return int(scoreStr.strip("分"))
            elif "任选" in scopeStr:
                # get the number between "任选" and "个" by regex
                permitQuantity = re.search(r"任选(?:(\d{1,3})|(\d{,3})-(\d{,3}))个", ruleP).groups()
                if permitQuantity[0]:
                    if "及以上" in scopeStr:
                        if len(numOfAnswerDigitalList) >= int(permitQuantity[0]):
                            return int(scoreStr.strip("分"))
                    elif len(numOfAnswerDigitalList) == int(permitQuantity[0]):
                        return int(scoreStr.strip("分"))
                elif permitQuantity[1] and permitQuantity[2]:
                    if int(permitQuantity[1]) <= len(numOfAnswerDigitalList) <= int(permitQuantity[2]):
                        return int(scoreStr.strip("分"))
            else:
                print("[不定项选择模块]:不能分辨此规则类型. ")
                print(f"Answer:{answer}\n"
                      f"rule:{rule},"
                      f"type:{type}")
                return 0
        print("[不定项选择模块]:不能处理此规则请检查！将处理为-1分 :", answer, rule, type)
        return -1
    else:
        print("不能判断此题分数请留意! 将处理为-1分 :")
        print(f"Answer:{answer}\n"
              f"rule:{rule},"
              f"type:{type}")
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
