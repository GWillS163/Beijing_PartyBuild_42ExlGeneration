#  Author : Github: @GWillS163
#  Time: $(Date)

#  Author : Github: @GWillS163
#  Time: $(Date)

#  Author : Github: @GWillS163
#  Time: $(Date)
import time

import xlwings as xw


def mergeSht2SummarizeCells(sht2_WithWeight, mergeCells, columns):
    columnLst = []
    if type(columns) == str:
        columnLst.append(columns)
    elif type(columns) == list:
        columnLst = columns
    else:
        raise Exception("the parameter columns type error, should be String or list")
    for column in columnLst:
        # show the merged cells gradually with step 2
        for i in range(0, len(mergeCells), 2):
            # print(mergeCells[i:i + 1])
            sht2_WithWeight.range(f"{column}{mergeCells[i]}:{column}{mergeCells[i + 1]}").merge()


class Test():
    def __init__(self):
        path = r"D:\Project\python_scripts\forWorking\HuayunTechRPA\Exl_Opr_2022-8-18\test - Copy.xlsx"
        surveyExlPh = "D:\work\考核RPA_Exl\Input\附件1：【测试问卷】中国移动北京公司2021年度党建工作成效调研—20220816.xlsx"

        app = xw.App(visible=True, add_book=False)
        app.display_alerts = False  # 警告关闭
        self.surveyWb = app.books.open(surveyExlPh)

        self.sht = self.surveyWb.sheets['测试问卷']
        self.sht2_WithWeight = self.surveyWb.sheets.add("Sht2")

    def close(self):
        pass
        # self.surveyWb.save("deleteTest.xlsx")
        # surveyWb.close()

    def addColumn4Sht2(self):
        columnScope = "A1:B32"

        self.sht.range(columnScope).api.Copy()
        self.sht2_WithWeight.range(columnScope.split(":")[0]).api.Select()
        self.sht2_WithWeight.api.Paste()
        self.surveyWb.app.api.CutCopyMode = False

    def deleteRow4Sht2(self, deleteRowLst):
        for row in deleteRowLst:
            self.sht2_WithWeight.range(f"B{row}").api.EntireRow.Delete()
            # set the width of the B column to 290
        print(self.sht2_WithWeight.range("B1:B2").column_width)
        print(self.sht2_WithWeight.range("B1:B2").row_height)
        self.sht2_WithWeight.range("B1").column_width = 18.8

        # show the merged cells scope
        print(self.sht2_WithWeight.range("A1:A20").merge_cells)

    def insertColumn4Sht(self):
        # insert column at C1
        self.sht2_WithWeight.range('A1').api.EntireColumn.Insert()

    def getMergeZoneDynamically(self, sht2_WithWeight):
        """
        for Sheet2
        :return:
        """
        # get merge cells scope dynamically
        mergeCells = []
        temp = None
        n = 3
        while True:
            if not sht2_WithWeight.range(f"B{n}").value:
                # print(temp)
                mergeCells.append(temp)
                break
            if sht2_WithWeight.range(f"A{n}").value:
                if temp:
                    # print(temp)
                    mergeCells.append(temp)
                # print(f"A{n}")
                mergeCells.append(n)
            else:
                temp = n
            n += 1
        return mergeCells


if __name__ == '__main__':
    test = Test()
    test.addColumn4Sht2()
    test.deleteRow4Sht2([31, 29, 27, 24, 18, 17, 15, 14, 13, 12, 11, 8, 5])
    mergeZoneSht2Lst = test.getMergeZoneDynamically(test.sht2_WithWeight)
    print(mergeZoneSht2Lst)
    mergeSht2SummarizeCells(test.sht2_WithWeight, mergeZoneSht2Lst, ["D", "F"])
