# Github: GWillS163
# User: 駿清清 
# Date: 28/09/2022 
# Time: 16:06

ph = r"D:\work\9.8_maintain\20220928144453.xlsx"


# import pandas as pd
#
# df = pd.read_excel(ph, sheet_name="sheet1")
# df = df.dropna(axis=0, how='all')


# import xlwings as xw
# app = xw.App(add_book=False, visible=True)
# wb = app.books.open(ph)
# sht = wb.sheets["sheet1"]
# print(sht.range("A1").value)


import xlrd
# use xlrd print content
wb = xlrd.open_workbook(ph)
sht = wb.sheets()[0]
res = []
for row in sht.get_rows():
    res.append([cell.value for cell in row])
print(res)
