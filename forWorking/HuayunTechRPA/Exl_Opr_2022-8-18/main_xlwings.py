#  Author : Github: @GWillS163
#  Time: $(Date)

import xlwings as xw
import pandas as pd


class Excel_Operation():
    def __init__(self, surveyExlPath, scoreExlPath):
        self.surveyExlPath = surveyExlPath
        self.scoreExlPath = scoreExlPath

        self.app4Attach1 = xw.App(visible=True, add_book=False)
        self.app4Attach2 = xw.App(visible=True, add_book=False)

        # open the survey file with xlwings
        self.surveyExl = self.app4Attach1.books.open(surveyExlPath)
        self.scoreExl = self.app4Attach2.books.open(scoreExlPath)

    def close_excel(self):
        self.surveyExl.close()
        self.scoreExl.close()
        self.app4Attach1.quit()
        self.app4Attach2.quit()

    def create_depart3_sheet(self, newSheetName, surveySheet='测试问卷', copy_scope="A1:J32", titleStart="K1"):
        # open the sheet named "测试问卷" of surveyPath
        surveySht = self.surveyExl.sheets[surveySheet]
        newSht = self.surveyExl.sheets.add(newSheetName)

        # Step1: copy the surveySht to newSht totally
        newSht.range(copy_scope).options(transpose=True).value = \
            surveySht.range(copy_scope).options(transpose=True).value

        # Step2: cope the other title at H1 to H32
        department = [["总公司", "", "", "北分公司", ""],
                      ["办公室", "党工会", "其他", "工作", "其他"]]
        # write department to newSht at H1 to H32
        newSht.range(titleStart).value = department

        # save
        self.surveyExl.save("test.xlsx")


if __name__ == '__main__':
    surveyExlPh = r"D:\work\考核RPA_Exl\附件1：【测试问卷】中国移动北京公司2021年度党建工作成效调研—20220816.xlsx"
    scoreExlPh = r"D:\work\考核RPA_Exl\附件2：党办调研问卷测试-8.15答题结果_20220815.xlsx"
    exOpr = Excel_Operation(surveyExlPh, scoreExlPh)
    exOpr.create_depart3_sheet("department3_sheet", "测试问卷", "A1:J32")

    exOpr.close_excel()
