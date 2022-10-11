#  Author : Github: @GWillS163
#  Time: $(Date)

#  Author : Github: @GWillS163
#  Time: $(Date)
import csv
import datetime
import os.path
import re
import time


def paramsCheckExist(surveyExlPath, partyAnsExlPh, peopleAnsExlPh, savePath):
    """
    检查输入文件是否存在, 并新建保存路径
    Check Input files are
    :param surveyExlPath:
    :param partyAnsExlPh:
    :param savePath:
    :return:
    """
    if surveyExlPath == partyAnsExlPh or surveyExlPath == savePath or partyAnsExlPh == savePath:
        raise FileExistsError("文件名输出重复,", surveyExlPath, partyAnsExlPh, savePath)
    fileDict = {
        "问卷模板文件": surveyExlPath,
        "党员答题文件": partyAnsExlPh,
        "群众答题文件": peopleAnsExlPh
    }
    for name, path in fileDict.items():
        if not os.path.exists(path):
            raise FileNotFoundError(f"{name} 不存在:")

    # make an output dir with current time
    outputDir = os.path.join(savePath, "output_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    os.makedirs(outputDir)

    return outputDir


def getColLtr(colNum: int) -> str:
    """0 -> A, 1 -> B, 2 -> C, ..., 26->AA, ..., 311 -> KZ
    :param colNum: the Column number of the Column Letter of Excel mappings
    :return the letter of Excel column
    """
    if colNum < 26:
        return chr(colNum + 65)
    else:
        return getColLtr(colNum // 26 - 1) + getColLtr(colNum % 26)


def getColNum(colLtr: str) -> int:
    """A -> 0, B -> 1, C -> 2, ..., AA->26, ..., KZ -> 311
    :param colLtr: the Column Letter of Excel
    :return the sequence number of Excel column
    """
    if len(colLtr) == 1:
        return ord(colLtr) - 65
    else:
        return (ord(colLtr[0]) - 64) * 26 + getColNum(colLtr[1:])


def getTltColRange(titleScope, offsite: int = 0):
    """titleScope : A1:B2, in other words is ColA to Col B
    return iterable Range
    :param titleScope:
    :param offsite: 偏移是为了在放置sht2值时，包含最后一列(默认不包含下界)
    """
    titleStart, titleEnd = titleScope.split(":")
    # get the letter of titleStart by regex
    titleStartLetter = re.findall(r"[A-Z]+", titleStart)[0]
    titleEndLetter = re.findall(r"[A-Z]+", titleEnd)[0]
    # convert to number
    titleStartLetterNum = getColNum(titleStartLetter)
    titleEndLetterNum = getColNum(titleEndLetter)
    titleEndLetterNum += offsite
    return range(titleStartLetterNum, titleEndLetterNum)


def getCurrentYear(userYear=None):
    # if userYear is a yearNum within 1970-2500, return year, otherwise return current year
    if not userYear or not userYear.isdigit():
        return datetime.datetime.now().year
    if 1970 <= int(userYear) <= 2500:
        return int(userYear)
    else:
        return datetime.datetime.now().year


def getLineData(allOrgCode):
    """
    获取所有的线数据
    :param allOrgCode:
    :return: {线条: [部门, 部门, ...]}
    """
    lineData = {}
    for orgName, orgInfo in allOrgCode.items():
        if orgInfo["line"] not in lineData:
            lineData.update({orgInfo["line"]: [orgName]})
            continue
        lineData[orgInfo["line"]] += [orgName]
    return lineData


def getAllOrgCode(orgSht):
    """返回所有的部门代码"""
    lastRow = orgSht.used_range.last_cell.row
    lastCol = orgSht.used_range.last_cell.column
    values = orgSht.range(f"A2:{getColLtr(lastCol)}{lastRow}").value
    allOrgCode = {}
    for row in values:
        allOrgCode.update({row[0]: {
            "departCode": row[1],
            "level": row[2],
            "line": row[3],
            "parent": row[4],
        }})
    return allOrgCode


def getSumSavePathNoSuffix(savePath, fileYear, fileName):
    fileYear = getCurrentYear(fileYear)
    return os.path.join(savePath, f"{fileYear}_{fileName}")


def getSht2DeleteCopiedRowScp(sht2_lv2Score, keywords: list) -> str:
    """
    获得需要删除的区间, keywords开始到结束的区间行
    :param keywords:  关键词列表
    :param sht2_lv2Score:
    :return:
    """
    row = 3
    while True:
        unit = sht2_lv2Score.range(f"A{row}").value
        if unit in keywords:
            break
        row += 1
    lastRow = sht2_lv2Score.used_range.last_cell.row
    return f"A{row}:A{lastRow}  "  # f"A32:A52"


def readLvDict(orgSht):
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


def saveDebugLogIfTrue(debugScoreLst, pathPre, debug, debugPath):
    """
    保存debug文件
    save debug file
    :param debug:
    :param debugPath:
    :param debugScoreLst:
    :param pathPre:
    :return:
    """
    if debug:
        print(f"正在保存Debug文件, {debugPath}")
        with open(f"{debugPath + pathPre}_{time.strftime('%Y%m%d%H%M%S')}.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows([["name", "questTitle", "quesType", "answer", "rule", "score"]])
            writer.writerows(debugScoreLst)


def paramsCheckSurvey(surveyExl, shtNameList: list):
    """
    调查问卷 文件名检查
    Survey Excel params check
    :param surveyExl:
    :param shtNameList:
    :return:
    """
    for shtName in shtNameList:
        try:
            surveyExl.sheets[shtName]
        except Exception as e:
            raise Exception(f"{shtName} 不存在于{surveyExl.name}中.\n ({e})")
    print(f"{surveyExl.name} Sheet 参数检查通过")


def chinizeBracket(s: str) -> str:
    """
    将英文括号转换为中文括号
    :param s:
    :return:
    """
    if not s:
        return s
    return s.replace("(", "（").replace(")", "）")


class Stuff:
    def __init__(self, name, lv2Depart, lv2Code, lv3Depart, lv3Code, ID, answerLst=None):
        self.name = name
        self.lv2Depart = chinizeBracket(lv2Depart)
        self.lv2Code = lv2Code
        self.lv3Depart = chinizeBracket(lv3Depart)
        self.lv3Code = lv3Code
        self.ID = ID
        self.answerLst = answerLst
        self.scoreLst = [0 for _ in range(len(answerLst))]

    def __str__(self):
        return f"{self.name} {self.lv2Depart} {self.lv2Code} {self.lv3Depart} {self.lv3Code} {self.ID} {self.answerLst}"

    def __repr__(self):
        return f"{self.name}, answers:{len(self.answerLst)}"  # lv2:{self.lv2Depart[:10]}, lv3:{self.lv3Depart[:10]},
