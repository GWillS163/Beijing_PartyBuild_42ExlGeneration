#  Author : Github: @GWillS163
#  Time: $(Date)
import os.path
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


def placeDepartmentTitle(sht, departmentLst, titleStart="K1"):
    """
    place the department title in the sht
    :param sht:
    :param departmentLst:
    :param titleStart:
    :return:
    """
    sht.range(titleStart).value = departmentLst
    # get merge info
    startRow = titleStart[1]
    endLetter = chr(ord(titleStart[0]) + len(departmentLst[1]) - 1)
    # merge K1:L1 cells
    # TODO: record index position
    sht.range(f"{titleStart}:{endLetter}{startRow}").merge()


def getMergeZoneDynamically(sht2_WithWeight):
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


def mergeSht2Lv3Title(sht2_WithWeight, departmentLen, startLv2="C2"):
    """
    merge the title of the third level in the sht2.
    Need Concern about Multi-department situation.
    :param startLv2:
    :param sht2_WithWeight:
    :param departmentLen:
    :return:
    """
    startCol = startLv2[0]
    startRow = startLv2[1]
    for gap in range(0, departmentLen + 1, 2):
        startRowLetter = chr(ord(startCol) + gap)
        endRowLetter = chr(ord(startRowLetter) + 1)
        # print(f"{startRowLetter}{startRow}:"
        #       f"{endRowLetter}{startRow}")
        sht2_WithWeight.range(f"{startRowLetter}{startRow}:"
                              f"{endRowLetter}{startRow}").merge()


class Stuff:
    def __init__(self, name, lv2Depart, lv2Code, lv3Depart, lv3Code, ID, scoreLst=[]):
        self.name = name
        self.department = lv2Depart
        self.position = lv2Code
        self.weight = lv3Depart
        self.code = lv3Code
        self.ID = ID
        self.scoreLst = scoreLst

    def __str__(self):
        return f"{self.name} {self.department} {self.position} {self.weight}"



class Excel_Operation():
    def __init__(self, surveyExlPath, scrExlPh, resultExlPh):
        self.surveyExlPath = surveyExlPath
        self.scoreExlPath = scrExlPh
        self.testExlPh = resultExlPh

        self.app4Survey1 = xw.App(visible=True, add_book=False)
        self.app4Score2 = xw.App(visible=True, add_book=False)
        self.app4Survey1.display_alerts = False
        self.app4Score2.display_alerts = False

        # open the survey file with xlwings
        self.surveyExl = self.app4Survey1.books.open(surveyExlPath)
        self.scoreExl = self.app4Score2.books.open(scrExlPh)

        # public variable
        self.surveyTestSht = self.surveyExl.sheets["测试问卷"]
        self.departmentDict = {}
        self.sht1ScoreDct = {}
        self.sht2ScoreDct = {}

        # settings
        self.summarizeFileName = "汇总文件"  # without extension ".xlsx"
        self.savePath = ".\\"
        self.sht1Name = "调研结果"  # "调研问卷(未加权)"
        self.sht2Name = "调研成绩"  # "调研问卷(加权)"
        self.sht3Name = "调研结果（2022年）"
        self.sht4Name = "调研成绩（2022年）"
        self.otherTitle = "其他人员"
        self.lv2AvgTitle = "二级单位成绩"

    def close_excel(self):
        self.surveyExl.close()
        self.scoreExl.close()
        self.app4Survey1.quit()
        self.app4Score2.quit()

    def __convertDict2Lst(self, departmentDict):
        """
        convert Dict 2 List
        :param avg:
        :param other:
        :param departmentDict:
        :param department: dict
        :return: [["二级部门", "二级部门", "二级部门"],
                 ["三级部门1","三级部门2"]]
        """
        # Step2: convertDict2Lst
        result_lst = [[], []]
        for layer2 in departmentDict:
            for layer3 in departmentDict[layer2]:
                if not layer3:
                    continue
                result_lst[0].append(layer2)
                result_lst[1].append(layer3)
            # add other items
            result_lst[0].append("")
            result_lst[1].append(self.otherTitle)
            result_lst[0].append("")
            result_lst[1].append(self.lv2AvgTitle)
        return result_lst

    def genSheet1_surveyWithoutWeight(self, departmentLst, scoreLst,
                                      columnScope="A1:J32", titleStart="K1", dataStart="K3"):
        """
        generate sheet1 of the surveyExl, which is the survey without weight
        :param dataStart:
        :param scoreLst:
        :param columnScope:
        :param departmentLst:
        :param titleStart:
        :return:
        """
        # Step1: add new sheet
        sht1_NoWeight = self.surveyExl.sheets.add(self.sht1Name)

        # Step2: copy left column the surveySht to sht1 partially with style
        self.surveyTestSht.range(columnScope).api.Copy()
        sht1_NoWeight.range(columnScope.split(":")[0]).api.Select()
        sht1_NoWeight.api.Paste()
        self.app4Survey1.api.CutCopyMode = False

        # Step3: place title
        placeDepartmentTitle(sht1_NoWeight, departmentLst, titleStart)

        # Step4: place score below title
        sht1_NoWeight.range(dataStart).value = scoreLst

    def genSheet2_surveyWithWeight(self, departmentLst, scoreLst,
                                   columnScope="A1:B32", titleStart="C1", dataStart="C3"):
        """
        generate sheet2 of the surveyExl, which is the survey with weight
        :return: None
        """
        # Step1: add new sheet
        sht2_WithWeight = self.surveyExl.sheets.add(self.sht2Name, after=self.sht1Name)

        # Step2: copy left column the surveySht to sht1, with style
        self.surveyTestSht.range(columnScope).api.Copy()
        sht2_WithWeight.range(columnScope.split(":")[0]).api.Select()
        sht2_WithWeight.api.Paste()
        self.app4Score2.api.CutCopyMode = False

        # Step3: delete the row of left column redundantly
        deleteRowLst = [31, 29, 27, 24, 18, 17, 15, 14, 13, 12, 11, 8, 5]
        for row in deleteRowLst:
            sht2_WithWeight.range(f"B{row}").api.EntireRow.Delete()
        sht2_WithWeight.range("B1").column_width = 18.8

        # Step3.1: place basic title
        placeDepartmentTitle(sht2_WithWeight, departmentLst, titleStart)

        # Step3.2: merge the summary cell below title
        mergeScope = getMergeZoneDynamically(sht2_WithWeight)

        # Step3.3: insert the summarize column
        # Step3.3.1 Get insert Column index info
        # in order to get the summary column index letter after the department column, get index letter iteratively
        # the insert start position of department lv3 is column "C",
        # e.g. the department is ["1", "2", "3"] (C D E), so the gap insert column is ["D", "F", "H"]
        departLst = departmentLst[1]
        departLst.remove(self.otherTitle)
        departLst.remove(self.lv2AvgTitle)
        summaryGapColLst = [chr(ord(titleStart[0]) + i * 2 + 1) for i in range(len(departLst))]
        print("summaryGapColLst: ", summaryGapColLst)
        # Step3.3.2 Insert the summarize column bt summaryGapColLst
        for col in summaryGapColLst:
            sht2_WithWeight.range(f"{col}1").api.EntireColumn.Insert()
            # Step3.3.3 Merge the summary column
        print("mergeScope", mergeScope)
        mergeSht2SummarizeCells(sht2_WithWeight, mergeScope, summaryGapColLst)
        # Step3.4: merge the lv3 title
        lv2titleStart = titleStart[0] + str(int(titleStart[0]) + 1)
        mergeSht2Lv3Title(sht2_WithWeight, len(departmentLst[1]), lv2titleStart)

        # Step4: place score below title
        sht2_WithWeight.range(dataStart).value = scoreLst

    def __setAllDepartmentDict(self, departmentScope="A1:F10"):
        """
        set the departments title from the surveyExl, can be inserted
        :param departmentScope:
        :no return but set: {"二级部门": ["三级部门","三级部门"], ...}
        """
        self.departmentDict = {}
        content = self.app4Score2.range(departmentScope).value
        for i in content:
            # print the 0th, 1st, 2nd,4th elements of i with format inline
            print(i[2], i[4])
            if i[2] not in self.departmentDict:
                self.departmentDict.update({i[2]: [i[4]]})
                continue
            if i[4] not in self.departmentDict[i[2]]:
                self.departmentDict[i[2]].append(i[4])

    def genOneDepartFile(self, savePath, departTitleLst, sht1ScoreLst, sht2ScoreLst):
        """
        generate one department file, the summarize File Data is different from the single department data
        :param savePath:
        :param sht1ScoreLst: the score content list of sheet1
        :param sht2ScoreLst:  the score content list of sheet2
        :param departTitleLst: the department title list
        :return:
        """
        # TODO: 还需Score & Title 的样式
        self.genSheet1_surveyWithoutWeight(departTitleLst, sht1ScoreLst)

        # TODO: 汇总列
        self.genSheet2_surveyWithWeight(departTitleLst, sht2ScoreLst)

        # save
        self.surveyExl.save(savePath)

    def genAllDepartFile(self):
        """
        generate all department file, Summarization and Single Department
        :return:
        """
        allDepartmentLst = [[], []]
        allSht1ScoreTb = []  # many rows
        allSht2ScoreTb = []  # many rows
        summarizeFileName = os.path.join(self.savePath, self.summarizeFileName + ".xlsx")
        for department in self.departmentDict:
            departmentLst = self.__convertDict2Lst(department)
            fileName = os.path.join(self.savePath, departmentLst[0][0] + ".xlsx")
            sht1ScoreTb = self.__getSht1ScoreTb()
            sht2ScoreTb = self.__getSht2ScoreTb()
            self.genOneDepartFile(fileName, departmentLst, sht1ScoreTb, sht2ScoreTb)

            # merge single Data to all
            allDepartmentLst[0] += departmentLst[0]
            allDepartmentLst[1] += departmentLst[1]
            # merge sht1ScoreTb to allSht1ScoreTb
            for Tb in [allSht1ScoreTb, allSht2ScoreTb]:
                for row in range(len(Tb)):
                    Tb.append(sht1ScoreTb[row] + sht1ScoreTb[row])

        # use all Data to generate summarize File
        self.genOneDepartFile(summarizeFileName, allDepartmentLst, allSht1ScoreTb, allSht2ScoreTb)

    def run(self):
        """
        run the whole process, the main function.
        :return:
        """
        # fake data

        # self.genOneDepartFile([["二级部门", "二级部门"], ["三级部门", "三级部门"]],
        #                       [["1", "2"], ["3", "4"]],
        #                       [["5", "6"], ["7", "8"]])

        # # 1. get the all department title
        self.__setAllDepartmentDict()
        # 2. generate all sht score
        sht1ScoreTb = self.__getSht1ScoreTb()
        sht2ScoreTb = self.__getSht2ScoreTb()

        # test, 获得单个部门
        departmentLst = []
        for key in self.departmentDict:
            if "二级部门" in key:
                continue
            departmentLst = self.__convertDict2Lst({key: self.departmentDict[key]})
            break
        print("正在写入 单个文件，假分数，departmentLst:", departmentLst)
        self.genOneDepartFile(self.testExlPh, departmentLst, sht1ScoreTb, sht2ScoreTb)

        # self.close_excel()
        print("All done")

    def __getSht1ScoreTb(self, ):
        return [["1", "2"], ["3", "4"]]

    def __getSht2ScoreTb(self, ):
        return [["5", "6"], ["7", "8"]]


if __name__ == '__main__':
    # if result.xlsx is exist, resultExlPh named as result + time.xlsx
    resultExlPh = "result" + time.strftime("%Y%m%d%H%M%S", time.localtime()) + ".xlsx"

    surveyExlPh = "D:\work\考核RPA_Exl\Input\附件1：【测试问卷】中国移动北京公司2021年度党建工作成效调研—20220816.xlsx"
    scoreExlPh = "D:\work\考核RPA_Exl\Input\附件2：党办调研问卷测试-8.15答题结果_20220815.xlsx"
    # resultExlPh = ".\\result.xlsx"
    Excel_Operation(surveyExlPh, scoreExlPh, resultExlPh).run()
