#  Author : Github: @GWillS163
#  Time: $(Date)
import csv
import os.path
import re
import time

import xlwings as xw

from lib import *

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
print("展示分数：")
# print(stuffWithLv) all score
for lv2 in staffWithLv:
    for lv3 in staffWithLv[lv2]:
        for stu in staffWithLv[lv2][lv3]:
            print(stu.name, stu.scoreLst)


# TODO: add Sheet2# Step1: add new sheet
columnScope="A1:J32"  # but at soon , C to I will be deleted
titleStart="C1"
dataStart="C3"
sht2_lv2Score = test.surveyExl.sheets.add(test.sht2NameGrade, after=test.sht1NameRes)

# Step2: copy left column the surveySht to sht1, with style
test.surveyTestSht.range(columnScope).api.Copy()
sht2_lv2Score.range(columnScope.split(":")[0]).api.Select()
sht2_lv2Score.api.Paste()
test.app4Score2.api.CutCopyMode = False

# Step2.1: delete the row of left column redundantly
deleteRowLst = [31, 29, 27, 24, 18, 17, 15, 14, 13, 12, 11, 8, 5]
for row in deleteRowLst:
    sht2_lv2Score.range(f"B{row}").api.EntireRow.Delete()
sht2_lv2Score.range("B1").column_width = 18.8
# Step2.2 delete the C to I column
sht2_lv2Score.range("C1:I1").api.EntireColumn.Delete()
sht2_lv2Score.range("A14:A19").api.EntireRow.Delete()
# TODO: 放到程序后面？Step2.3 add summary row
sht2OprAddSummaryRows(sht2_lv2Score)

# Step3: copy title
sht1_moduleSht = test.moduleExl.sheets["调研成绩"]
sht1_moduleSht.range("D1:L2").api.Copy()
sht2_lv2Score.range(titleStart).api.Select()
sht2_lv2Score.api.Paste()
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


