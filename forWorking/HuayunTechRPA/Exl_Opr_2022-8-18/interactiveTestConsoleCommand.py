#  Author : Github: @GWillS163
#  Time: $(Date)
import csv
import os.path
import re
import time

import xlwings as xw

from lib import *
from shtOpr import *
from shtDataCalc import *
from scoreJudge import *

# if result.xlsx is exist, resultExlPh named as result + time.xlsx
resultExlPh = "result" + time.strftime("%Y%m%d%H%M%S", time.localtime()) + ".xlsx"

surveyExlPh = "D:\work\考核RPA_Exl\Input\模板1：【测试问卷】标准模板示例（原文件修改）_2022-8-30.xlsx"
scoreExlPh = "D:\work\考核RPA_Exl\Input\模板2：党办调研问卷测试-8.15答题结果_（模板）_2022-8-30.xlsx"
moduleExlPh = r"D:\Project\python_scripts\forWorking\HuayunTechRPA\Exl_Opr_2022-8-18\origin\【RPA模板表(测试)】中国移动北京公司2021年度党建工作成效调研.xlsx"

# resultExlPh = ".\\result.xlsx"
test = Excel_Operation(surveyExlPh, scoreExlPh, moduleExlPh, resultExlPh)

# TODO: get score 注意切换到正确的sheet
staffWithLv, scoreWithLv = test.getStuffDict()
for stu in staffWithLv:
    print(stu)
print(test.scoreExlTitle)
staffWithLv = test.getStuffAllScore(staffWithLv)
scoreWithLv = getScoreWithLv(staffWithLv)
print("展示分数：")
# print(stuffWithLv) all score
for lv2 in staffWithLv:
    for lv3 in staffWithLv[lv2]:
        for stu in staffWithLv[lv2][lv3]:
            print(stu.name, stu.scoreLst)

# TODO: get score
scoreWithLv = getScoreWithLv(staffWithLv)
sht1WithLv = getSht1WithLv(scoreWithLv)   # 2022-9-2 OK
lv2Unit = getSht2Lv2UnitScope(test.surveyTestSht)
sht2WithLv = getSht2WithLv(sht1WithLv, lv2Unit)  # TODO: 找到所有lv3部门，求平均

# get current Lv2
currLv2 = None
for lv2 in sht2WithLv:
# get all lv3 of lv2
# summarize score of lv3
# get mean score of lv2
sht3WithLv = getSht3WithLv(sht1WithLv)


# TODO: add Sheet2# Step1: add new sheet
sht2_lv2Score = test.surveyExl.sheets.add(test.sht2NameGrade )

sht1_moduleSht = test.moduleExl.sheets["调研成绩"]
sht2SetTitleIndex(test.surveyTestSht, sht2_lv2Score, sht1_moduleSht)

dataStart = "C3"
# TODO: 放到程序后面？Step2.3 add summary row
sht2OprAddSummaryRows(sht2_lv2Score, {})
test.app4Survey1.api.CutCopyMode = False

# Step3.1： get grade cells position department mapping
sht1_lv2Result = test.surveyExl.sheets[test.sht1NameRes]
sht1_moduleSht = test.moduleExl.sheets["调研成绩"]
# get Score
getSht1Col = "G"
unit = None
breakSign = 0
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

# Step4: place score below title
sht2UntCol = "B"
sht2WgtCol = "C"
sht2ScrCol = "D"
for row in range(3, 40):
    currUnit = sht2_lv2Score.range(f"{sht2UntCol}{row}").value
    if not currUnit:
        break
    if currUnit not in allUnitScore:
        continue
    wgt = sht2_lv2Score.range(f"{sht2WgtCol}{row}").value
    sht2_lv2Score.range(f"{sht2ScrCol}{row}").value = allUnitScore[currUnit]

# TODO: add Sheet1
titleStart = test.sht1MdlTltScope.split(":")[0]
dataStart = titleStart[:1] + str(int(test.sht1TltStart.split(":")[1][-1]) + 1)
# Step1: add new sheet
sht1_lv2Result = test.surveyExl.sheets.add(test.sht1NameRes)

# Step2: copy left column the surveySht to sht1 partially with style
test.surveyTestSht.range(test.sht1ColScope).api.Copy()
sht1_lv2Result.range(test.sht1ColScope.split(":")[0]).api.Select()
sht1_lv2Result.api.Paste()
test.app4Survey1.api.CutCopyMode = False

# Step3: copy title
# sht1_tltScope = "F1:KZ2"
sht1_moduleSht = test.moduleExl.sheets[test.surveyResultName]
sht1_moduleSht.range(test.sht1MdlTltScope).api.Copy()
sht1_lv2Result.range(test.sht1TltStart.split(":")[0]).api.Select()
sht1_lv2Result.api.Paste()
test.app4Survey1.api.CutCopyMode = False

# TODO: Step4: place score below title
# TODO: need titleScope
titleMatrix = test.moduleExl.sheets['调研结果'].range(test.sht1MdlTltScope).value
# titleMatrix = sht1_lv2Result.range(test.sht1MdlTltScope).value
titleDf = pd.DataFrame(titleMatrix)
sht1Value = sht1_calculate(staffWithLv, titleDf)
sht1ValueDf = pd.DataFrame(sht1Value).transpose()
# place sht1ValueDf to sht1_lv2Result at dataStart
sht1_lv2Result.range(dataStart).value = sht1ValueDf
# delete range G3:G6 and fill by right value
sht1_lv2Result.range("G3:G33").api.Delete()
sht1_lv2Result.range("G3:KZ3").api.Delete()
