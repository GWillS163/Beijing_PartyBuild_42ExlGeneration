#  Author : Github: @GWillS163
#  Time: $(Date)

import xlwings as xw

surveyExlPath = "D:\work\考核RPA_Exl\附件1：【测试问卷】中国移动北京公司2021年度党建工作成效调研—20220816.xlsx"
scoreExlPath = "D:\work\考核RPA_Exl\附件2：党办调研问卷测试-8.15答题结果_20220815.xlsx"

# use xlwings to open excel file

# app4Attach1 = xw.App(visible=True, add_book=False)
# wb4Attach1 = app4Attach1.books.open(surveyExlPath)
app4Attach2 = xw.App(visible=True, add_book=False)
wb4Attach2 = app4Attach2.books.open(scoreExlPath)

# open the survey file with xlwings
surveyExl = wb4Attach2.sheets[0]

# print the content of the surveyExl
print(surveyExl.range("A1:F10").options(transpose=True).value)


