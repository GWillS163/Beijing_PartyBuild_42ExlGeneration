# Github: GWillS163
# User: 駿清清 
# Date: 10/11/2022 
# Time: 15:48

import datetime
import os.path
import time
import warnings
import openpyxl
import xlrd

# 最终文件处理

def parasCheck(file1, file2, path, fileName):
    """
    参数检查
    parameters check
    :param file1:
    :param file2:
    :param path:
    :param fileName:
    :return:
    """
    if not os.path.exists(file1) or not os.path.exists(file2):
        raise FileNotFoundError("请检查前两个参数文件路径")
    if not os.path.exists(path):
        # mkdir recursion
        os.makedirs(path)
    if not fileName:
        raise ValueError("请检查第四个参数文件名")


def getFileData(file1):
    """
    读取表格文件内容 - read file content
    :param file1:
    :return:
    """
    try:
        # 使用openpyxl读取表格文件内容 - read file content by openpyxl
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("ignore")
            wb = openpyxl.load_workbook(file1)
            sheet = wb.active
            data = []
            for row in sheet.rows:
                data.append([cell.value for cell in row])
            wb.close()
        return data
    except KeyError:
        raise KeyError("文件可能已损坏，请检查文件")


def getData2(filePath):
    """
    修复了损坏文件打不开的问题
    :param filePath:
    :return:
    """
    # use xlrd print content
    wb = xlrd.open_workbook(filePath)
    sht = wb.sheets()[0]
    res = []
    for row in sht.get_rows():
        res.append([cell.value for cell in row])
    return res


def getTodayData(dateCol, data, today=""):
    """
    如果用户没有输入日期，就默认为今天；如果用户输入了日期，格式为2021-09-09
    :param dateCol:
    :param data:
    :param today:
    :return:
    """
    if not today:
        today = datetime.date.today()
        # format today with "%Y-%m-%d"
        today = today.strftime("%Y-%m-%d")

    res = []
    for row in data:
        if type(row[dateCol]) == datetime.datetime:
            row[dateCol] = row[dateCol].strftime("%Y-%m-%d")
        else:
            continue
        # 如果日期相同，就把这一行数据加入到res中 - if the date is the same, add the row to res
        if today == row[dateCol]:
            res.append(row)
    return res


def getData1DiffData2(currentData1: list, col1: int, data2: list, col2: int):
    """
    得到data1中不在data2中的数据 - get the data in data1 but not in data2
    :param col1:
    :param col2:
    :param currentData1:
    :param data2:
    :return:
    """
    beCompareData = [row[col1] for row in data2]
    diffData = []
    for row in currentData1:
        if row[col1] not in beCompareData:
            diffData.append(row)
    return diffData


def saveDiffData(diffData, path, fileName):
    """
    保存数据 - save data
    :param diffData:
    :param path:
    :param fileName:
    :return:
    """
    suffix = time.strftime("_%Y-%m-%d_%H-%M-%S", time.localtime())
    try:
        wb = openpyxl.Workbook()
        sheet = wb.active
        for row in diffData:
            sheet.append(row)
        wb.save(os.path.join(path, fileName + suffix) + ".xlsx")
        wb.close()
        return True
    except Exception as e:
        print(e)
        return False


def main(file1, file2, path, fileName, today=""):
    """
    主函数：1.拿到当天数据，2.file1 & file2对比，保存file1里当天不同的数据
    main function - 1.get today data, 2.compare file1 & file2, save the data in file1 but not in file2
    :param today: 如果用户没有输入日期，就默认为今天；如果用户输入了日期，格式为2021-09-09 - if the user does not enter the date, the default is today; if the user enters the date, the format is 2021-09-09
    :param file1:
    :param file2:
    :param path:
    :param fileName: 保存的文件名 - file name
    :return: True or False
    """
    file1DateCol = 5  # 3 is the column index of the date - 3是日期所在的列
    file1CodeCol = 4  # 4&2 is the column index of the name - 4&2是比对的单号所在的列
    file2CodeCol = 2
    parasCheck(file1, file2, path, fileName)
    # data1 = getFileData(file1)
    # data2 = getFileData(file2)
    data1 = getData2(file1)
    data2 = getData2(file2)

    # 通过条件筛选数据 - sift Data by condition
    currentData1 = getTodayData(file1DateCol, data1, today)
    diffData = getData1DiffData2(currentData1, file1CodeCol, data2, file2CodeCol)
    saveStatus = saveDiffData(diffData, path, fileName)

    print("Done" if saveStatus else "Failed")
    return saveStatus

# main(file1, file2, path, fileName)
# main(r"D:\Project\python_scripts\forWorking\HuayunTechRPA\maintain_2022-9-23\input\2022-11-10\20221110152654.xlsx",
#      r"D:\Project\python_scripts\forWorking\HuayunTechRPA\maintain_2022-9-23\input\2022-11-10\20221110152752.xlsx",
#      ".\\output", "result.xlsx")
