#  Author : Github: @GWillS163
#  Time: $(Date)

#  Author : Github: @GWillS163
#  Time: $(Date)

#  Author : Github: @GWillS163
#  Time: $(Date)

import sys
sys.path.append(r"D:\Project\python_scripts\forWorking\HuayunTechRPA\Exl_Opr_2022-8-18")
from coreCode.main_xlwings import Excel_Operation

from coreCode.shtOperation import *
import time
from coreCode.shtDataCalc import *

# if result.xlsx is exist, resultExlPh named as result + time.xlsx
resultExlPh = "result" + time.strftime("%Y%m%d%H%M%S", time.localtime()) + ".xlsx"

# surveyExlPh = "D:\work\考核RPA_Exl\Input\模板1：【测试问卷】标准模板示例（原文件修改）_2022-8-30.xlsx"
surveyExlPh = "D:\work\考核RPA_Exl\Input\模板：【测试问卷】标准模板示例_2022-9-14.xlsx"
scoreExlPh = "D:\work\考核RPA_Exl\Input\模板2：党办调研问卷测试-8.15答题结果_（模板）_2022-8-30.xlsx"

# resultExlPh = ".\\result.xlsx"
test = Excel_Operation(surveyExlPh, scoreExlPh,
                       "D:\\", "2022", "PartyBuildingSurvey", "20002100",
                       )
test.fillAllData(,

#


import xlwings as xw
# departments Tets
# 从汇总表 获取 部门分类区间
sht1Sum = test.resultExl.sheets[test.sht1NameRes]
sht2Sum = test.resultExl.sheets[test.sht2NameGrade]
deptUnitSht1 = getDeptUnit(sht1Sum, "G:KZ")
deptUnitSht2 = getDeptUnit(sht2Sum, "D:L")
# create new excel with xlwings
deptResultExl = xw.Book()
sht1Dept = deptResultExl.sheets.add(test.sht1NameRes)
sht2Dept = deptResultExl.sheets.add(test.sht2NameGrade, after=sht1Dept)

# 从汇总表 复制 边栏
sht1Dept.activate()
shtCopyTo(sht1Sum, "A1:F32", sht1Dept, "A1")
sht2Dept.activate()
shtCopyTo(sht2Sum, "A1:C20", sht2Dept, "A1")
# for sht1DeptName, sht2DeptName in zip(deptUnitSht1, deptUnitSht2):

# for deptName, sht2DeptName in zip(deptUnitSht1, deptUnitSht2):
sht2BorderL, sht2BorderR = "G", "Z"

for deptName in deptUnitSht1:
    # add department data
    sht1BorderL, sht1BorderR = addOneDptData(sht1Sum, deptUnitSht1[deptName], test.deptCopyHeight,
                                             sht1Dept, test.sht1TitleCopyTo)
    if deptName in deptUnitSht2:
        sht2BorderL, sht2BorderR = addOneDptData(sht2Sum, deptUnitSht2[deptName], test.deptCopyHeight,
                                                 sht2Dept, test.sht2TitleCopyTo)

    # Save Excel
    # get current time
    timeNow = time.strftime("%Y%m%d%H%M", time.localtime())
    deptResultExl.save(f"2022_PartyBuildingResultSurvey_{timeNow}_{deptName}.xlsx")

    # Clear the sheet for next loop dynamically
    print(sht1Dept, test.sht1TitleCopyTo, test.deptCopyHeight,
                  sht1BorderR, sht1BorderL)
    sht1Dept.activate()
    dltOneDptData(sht1Dept, test.sht1TitleCopyTo, test.deptCopyHeight,
                  sht1BorderR, sht1BorderL)
    if deptName in deptUnitSht2:
        sht2Dept.activate()
        dltOneDptData(sht2Dept, test.sht2TitleCopyTo, test.deptCopyHeight,
                      sht2BorderL, sht2BorderR)

deptResultExl.close()
test.resultExl.close()

