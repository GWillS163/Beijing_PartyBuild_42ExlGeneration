# Github: GWillS163
# User: 駿清清 
# Date: 29/09/2022 
# Time: 11:04
surveyExlPath = r"D:\work\考核RPA_Exl\Input\模板：【测试问卷】标准模板示例_2022-9-14.xlsx"

surveyTestShtName = "测试问卷"
import xlwings as xw

app4Survey1 = xw.App(visible=True, add_book=False)

app4Survey1.display_alerts = False
# surveyExl = app4Survey1.books.open(surveyExlPath)
surveyExl = app4Survey1.books.add()
surveyTestSht = surveyExl.sheets[surveyTestShtName]  # "测试问卷"

print(surveyExl.name)