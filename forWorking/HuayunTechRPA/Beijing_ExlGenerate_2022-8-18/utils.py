#  Author : Github: @GWillS163
#  Time: $(Date)

#  Author : Github: @GWillS163
#  Time: $(Date)
import csv
import datetime
import os.path
import re
import time


def getColLtr(colNum: int) -> str:
    """0 -> A, 1 -> B, 2 -> C, ..., 26->AA, ..., 311 -> KZ
    :param colNum: the Column number of the Column Letter of Excel mappings
    :return the letter of Excel column
    """
    if colNum < 26:
        return chr(colNum + 65)
    else:
        return getColLtr(colNum // 26 - 1) + getColLtr(colNum % 26)


def paramsCheckExist(surveyExlPath, scrExlPh, savePath, fileYear, fileName):
    """
    检查输入文件是否存在, 并新建保存路径
    Check Input files are
    :param surveyExlPath:
    :param scrExlPh:
    :param savePath:
    :param fileYear:
    :param fileName:
    :return:
    """
    if surveyExlPath == scrExlPh or surveyExlPath == savePath or scrExlPh == savePath:
        raise FileExistsError("文件名输出重复,", surveyExlPath, scrExlPh, savePath)
    if not os.path.exists(surveyExlPath):
        raise FileNotFoundError("问卷模板文件不存在:")
    if not os.path.exists(scrExlPh):
        return FileNotFoundError("分数数据文件不存在:", scrExlPh)
    if not os.path.exists(savePath):
        return FileNotFoundError("指定的保存路径不存在")

    summaryFileName = f"{fileYear}_{fileName}.xlsx"
    # make an output dir with current time
    outputDir = os.path.join(savePath, "output_", datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    os.makedirs(outputDir)

    return os.path.join(outputDir, summaryFileName)


def getColNum(colLtr: str) -> int:
    """A -> 0, B -> 1, C -> 2, ..., AA->26, ..., KZ -> 311
    :param colLtr: the Column Letter of Excel
    :return the sequence number of Excel column
    """
    if len(colLtr) == 1:
        return ord(colLtr) - 65
    else:
        return (ord(colLtr[0]) - 64) * 26 + getColNum(colLtr[1:])


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


def getCurrentYear(userYear=None):
    # if userYear is a yearNum within 1970-2500, return year, otherwise return current year
    if not userYear or not userYear.isdigit():
        return datetime.datetime.now().year
    if 1970 <= int(userYear) <= 2500:
        return int(userYear)
    else:
        return datetime.datetime.now().year


def addRankForSht2():
    """为第二个sheet添加排名"""
    pass


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


def saveDebugFile(debugScoreLst, pathPre):
    """
    保存debug文件
    save debug file
    :param debugScoreLst:
    :param pathPre:
    :return:
    """
    with open(f"{pathPre}_{time.strftime('%Y%m%d%H%M%S')}.csv", "w", newline="") as f:
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
