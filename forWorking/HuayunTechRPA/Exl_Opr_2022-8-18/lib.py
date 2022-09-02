#  Author : Github: @GWillS163
#  Time: $(Date)
import re


def listMultipy(lst1, lst2):
    return list(map(lambda x, y: x * y, lst1, lst2))


def readOrgDict(orgSht):
    """返回结构化的字典，key是部门名，value是部门下的子部门"""
    allOrg = {}
    row = 1
    while True:
        a = orgSht.range(f"A{row}").value
        b = orgSht.range(f"B{row}").value
        if not (a and b):
            break
        if a not in allOrg:
            allOrg.update({a: [b]})
        else:
            allOrg[a].append(b)
        row += 1
    return allOrg


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
