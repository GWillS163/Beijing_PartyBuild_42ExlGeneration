#  Author : Github: @GWillS163
#  Time: $(Date)

import sys
sys.path.append(r"D:\Project\python_scripts\forWorking\HuayunTechRPA\Exl_Opr_2022-8-18")
from main_xlwings import Excel_Operation

from shtOperation import *
import time
from shtDataCalc import *

# if result.xlsx is exist, resultExlPh named as result + time.xlsx
resultExlPh = "result" + time.strftime("%Y%m%d%H%M%S", time.localtime()) + ".xlsx"

surveyExlPh = "D:\work\考核RPA_Exl\Input\模板1：【测试问卷】标准模板示例（原文件修改）_2022-8-30.xlsx"
scoreExlPh = "D:\work\考核RPA_Exl\Input\模板2：党办调研问卷测试-8.15答题结果_（模板）_2022-8-30.xlsx"
moduleExlPh = r"D:\Project\python_scripts\forWorking\HuayunTechRPA\Exl_Opr_2022-8-18\origin\【RPA模板表(测试)】中国移动北京公司2021年度党建工作成效调研.xlsx"

# resultExlPh = ".\\result.xlsx"
test = Excel_Operation(surveyExlPh, scoreExlPh, moduleExlPh, resultExlPh)

# TODO: 1. 读取问卷表格，获取所有的单位名称


# TODO: get score 注意切换到正确的sheet
staffWithLv = test.getStuffDict()
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

# get current Lv2
# TODO: get ALL Sht score
sht1WithLv = getSht1WithLv(scoreWithLv)   # 2022-9-2 OK
orgDict = readOrgDict(test.surveyTestSht)
test.addSheet1_surveyResult(staffWithLv)
test.addSheet1_surveyResult(sht1WithLv)
time.sleep(2)
test.addSheet2_surveyGrade(staffWithLv, orgDict)
time.sleep(2)
test.addSheet3_surveyResultByYear(staffWithLv, orgDict)
time.sleep(2)
test.addSheet4_surveyGradeByYear(staffWithLv, orgDict)


# TODO: Sheet2 Test
# Step1: add new sheet and define module sheet
sht2_lv2Score = test.surveyExl.sheets[test.sht2NameGrade]


# TODO: step2: Get Data
# sht1_wgt = sht1_lv2Result.range("F3:F32").value
sht2WgtLst = sht2_lv2Score.range("C3:C13").value
lv2Unit = getSht2Lv2UnitScope(test.surveyTestSht)
sht2WithLv = getSht2WithLv(sht1WithLv, lv2Unit, sht2WgtLst)  # TODO: Round 3

# TODO: Step3: Set data
# iterate sheet2 each lv3 department
sht2SetData(sht2_lv2Score, sht2WithLv, "D:L", sht2WgtLst)




# Sht2 end ---------------



# Step3.1： get grade cells position department mapping
sht1_lv2Result = test.surveyExl.sheets[test.sht1NameRes]
sht1_moduleSht = test.sht1Module
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
titleStart, r = test.sht1MdlTltScope.split(":")
dataStart = r + str(int(test.sht1MdlTltScope.split(":")[1][-1]) + 1)
# Step1: add new sheet and define module sheet
sht1_lv2Result = test.surveyExl.sheets.add(test.sht1NameRes)
# sht1_lv2Result = test.moduleExl.sheets[test.sht1NameRes]

# Step2.1: copy left column the surveySht to sht1 partially with style
shtCopyTo(test.surveyTestSht, test.sht1ColScope,
          sht1_lv2Result, test.sht1ColScope.split(":")[0])
# Step2.2: copy title
shtCopyTo(test.sht1Module, test.sht1MdlTltScope,
          sht1_lv2Result, test.sht1TltStart)  # sht1_tltScope = "F1:KZ2"

# TODO: Step3: set data