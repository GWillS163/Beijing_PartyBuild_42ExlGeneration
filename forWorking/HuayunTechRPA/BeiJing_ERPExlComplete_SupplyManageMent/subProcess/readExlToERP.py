# Github: GWillS163
# User: 駿清清 
# Date: 22/11/2022 
# Time: 17:25

# 仅读取ERP列
# import openpyxl
import xlwings as xw
import os


def readExlData(exlPath):
    """
    读取exl文件内容
    :param exlPath:
    :return:
    """
    # wb = openpyxl.load_workbook(exlPath)
    # sheet = wb.active
    # exlData = list(sheet.values)
    # wb.close()
    app = xw.App(visible=False, add_book=False)
    wb = app.books.open(exlPath)
    sheet = wb.sheets[0]
    exlData = sheet.range("A1").expand().value
    wb.close()
    app.quit()
    return exlData


def paramsCheck(exlPath):
    # check the exl file whether exist
    if not os.path.exists(exlPath):
        raise FileNotFoundError(f"exl file not found: {exlPath}")


def main(exlPath, erpCol):
    """
    仅读取ERP列
    :param erpCol:  + 1 是因为excel的列是从1开始的
    :param exlPath:
    :return:
    """
    # paramsCheck(exlPath)

    exlData = readExlData(exlPath)[1:]  # 去掉表头
    return [row[erpCol - 1] for row in exlData]


# print(main("..\\test\\BJ未接收订单1103.xlsx", 1))
# print(main("..\\test\\ERP_北京PO接收未开单-0906.xlsx", 1))
#
erpCodeList = main(filePath, erpCol)
