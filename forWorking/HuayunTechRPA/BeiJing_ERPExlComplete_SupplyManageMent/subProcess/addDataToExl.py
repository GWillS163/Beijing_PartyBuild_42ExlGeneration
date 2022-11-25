# Github: GWillS163
# User: 駿清清 
# Date: 23/11/2022 
# Time: 13:26
import time
# import openpyxl
import xlwings as xw
# open the exl file and insert the data as column in designed position
from typing import List


def getNewExlPath(exlPath):
    timeStr = time.strftime("%Y%m%d%H%M%S", time.localtime())
    return exlPath.replace(".xlsx", f"_{timeStr}.xlsx")


def insertDataAsColumn(exlPath, data: List[list], colNum):
    wb = openpyxl.load_workbook(exlPath)
    sheet = wb.active
    # add some columns
    sheet.insert_cols(colNum, amount=len(data))
    # insert data
    for row in range(max([len(row) for row in data])):
        for col in range(len(data[row])):
            sheet.cell(row=row + 1, column=col + colNum).value = data[row][col]
    wb.save(getNewExlPath(exlPath))
    wb.close()


def insertDataAsColumn_xw(exlPath, data: List[list], colNum):

    app = xw.App(visible=False, add_book=False)
    wb = app.books.open(exlPath)
    sheet = wb.sheets[0]
    # add some columns
    sheet.range((1, colNum)).api.EntireColumn.Insert(max([len(row) for row in data]))
    # insert data
    for row in range(len(data)):
        sheet.range((row + 1, colNum)).value = data[row]
    wb.close()
    app.quit()

# insertDataAsColumn(filePath, sumDataList, insertCol)
insertDataAsColumn_xw(filePath, sumDataList, insertCol)

# insertDataAsColumn_xw("..\\test\\BJ未接收订单1103.xlsx",
#                    [[1, 2, 3], [1, 2, 3], [1, 2, 3]],
#                    4)
