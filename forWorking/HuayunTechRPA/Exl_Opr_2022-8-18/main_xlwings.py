#  Author : Github: @GWillS163
#  Time: $(Date)
import csv
import os.path
import re
import time

import xlwings as xw

from lib import *


class Excel_Operation():
    def __init__(self, surveyExlPath, scrExlPh, resultExlPh):
        self.scoreExlTitle = None
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
        self.sht1SurveyRes = "调研结果"  # "调研问卷(未加权)"
        self.sht2SurveyGrade = "调研成绩"  # "调研问卷(加权)"
        self.sht3SurveyResYear = "调研结果（2022年）"
        self.sht4SurveyScoreYear = "调研成绩（2022年）"
        self.otherTitle = "其他人员"
        self.lv2AvgTitle = "二级单位成绩"
        self.ruleCol = "I"  # 赋分规则列
        self.ruleTypeCol = "G"  # 题目类型列

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

    def __getRawScoreTb(self, scope="A1:M10"):
        # get all scoreExl sheet0 content
        return self.scoreExl.sheets[0].range(scope).value

    def genSheet2_surveyWithWeight__obsolete(self, departmentLst, scoreLst,
                                   columnScope="A1:B32", titleStart="C1", dataStart="C3"):
        """
        unUsed. generate sheet2 of the surveyExl, which is the survey with weight
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

    def addSheet1_surveyResult(self, departmentLst, scoreLst,
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
        sht1_NoWeight = self.surveyExl.sheets.add(self.sht1SurveyRes)

        # Step2: copy left column the surveySht to sht1 partially with style
        self.surveyTestSht.range(columnScope).api.Copy()
        sht1_NoWeight.range(columnScope.split(":")[0]).api.Select()
        sht1_NoWeight.api.Paste()
        self.app4Survey1.api.CutCopyMode = False

        # TODO: Step3: copy title

        # TODO: Step4: place score below title

    def addSheet2_surveyScore(self, departmentLst, scoreLst,
                              columnScope="A1:B32", titleStart="C1", dataStart="C3"):
        """
        generate sheet2 of the surveyExl, which is the survey with weight
        :return: None
        """
        # Step1: add new sheet
        sht2_WithWeight = self.surveyExl.sheets.add(self.sht2SurveyGrade, after=self.sht1Name)

        # Step2: copy left column the surveySht to sht1, with style
        self.surveyTestSht.range(columnScope).api.Copy()
        sht2_WithWeight.range(columnScope.split(":")[0]).api.Select()
        sht2_WithWeight.api.Paste()
        self.app4Score2.api.CutCopyMode = False

        # Step2.1: delete the row of left column redundantly
        deleteRowLst = [31, 29, 27, 24, 18, 17, 15, 14, 13, 12, 11, 8, 5]
        for row in deleteRowLst:
            sht2_WithWeight.range(f"B{row}").api.EntireRow.Delete()
        sht2_WithWeight.range("B1").column_width = 18.8

        # Step3: copy title
        placeDepartmentTitle(sht2_WithWeight, departmentLst, titleStart)
        # Step3.1： get grade cells position department mapping

        # Step4: place score below title

    def addSheet3_surveyResultByYear(self, departmentLst, scoreLst,
                                     columnScope="A1:J32", titleStart="K1", dataStart="K3"):
        """
        generate sheet3 of the surveyExl, which is the survey without weight
        :return: None
        """
        # Step1: add new sheet
        sht3_NoWeight = self.surveyExl.sheets.add(self.sht3Name, after=self.sht2Name)

        # Step2: copy left column the surveySht to sht1, with style
        self.surveyTestSht.range(columnScope).api.Copy()
        sht3_NoWeight.range(columnScope.split(":")[0]).api.Select()
        sht3_NoWeight.api.Paste()
        self.app4Survey1.api.CutCopyMode = False
        # Step2.1 delete the row of left column redundantly

        # Step3: copy title

    def addSheet4_surveyScoreByYear(self, departmentLst, scoreLst,
                                    columnScope="A1:B32", titleStart="C1", dataStart="C3"):
        """
        generate sheet4 of the surveyExl, which is the survey with weight
        :return: None
        """
        # Step1: add new sheet
        sht4_WithWeight = self.surveyExl.sheets.add(self.sht4Name, after=self.sht3Name)

        # Step2: copy left column the surveySht to sht1, with style
        self.surveyTestSht.range(columnScope).api.Copy()
        sht4_WithWeight.range(columnScope.split(":")[0]).api.Select()
        sht4_WithWeight.api.Paste()
        self.app4Score2.api.CutCopyMode = False
        # Step2.1 delete the row of left column redundantly

        # Step3: copy title

    def getStuffLst(self, departmentScope="A1:AM10"):
        """
        """
        stuffLst = []
        content = self.app4Score2.range(departmentScope).value
        for i in content:
            if not all(i):
                continue
            if i[0] == "序号":
                self.scoreExlTitle = Stuff(i[1], i[2], i[3], i[4], i[5], i[6], i[9:])
                continue
            stu = Stuff(i[1], i[2], i[3], i[4], i[5], i[6], i[9:])
            # print(stu)
            stuffLst.append(stu)
        return stuffLst

    @staticmethod
    def test():
        ans4 = """
        4.每季度3次及以上"""
        rule4 = """10分：3或4
        9分：2
        0分：1"""
        print(judgeAnswerGrade(ans4, rule4, "不定项选择题"), 10)

    def getStuffAllScore(self, stuffLst, debug=True):
        print("getScore function Start ------------------------------")

        debugScoreLst = []  # store [name, questTitle, answer, rule, score] for debug
        # get the score of each stuff
        for stuff in stuffLst:
            # every stuff need to get the all score
            for questionNum in range(len(self.scoreExlTitle.answerLst)):
                if not stuff.answerLst[questionNum]:
                    continue
                # get every questTitle by questTitle num
                questTitle = self.scoreExlTitle.answerLst[questionNum]
                # get stuff answer
                answer = stuff.answerLst[questionNum]
                # locate which row is rule by questTitle in scoreExl
                answerRow = -1
                for row in range(3, 40):
                    # find the cell in the surveyExl by answer
                    ruleQuest = self.surveyTestSht.range(f"E{row}").value
                    if ruleQuest is None:
                        continue
                    if ruleQuest in questTitle:
                        # print("Check_cellQuestion: ", ruleQuest)
                        answerRow = row
                        break
                if answerRow == -1:
                    print(f"{questTitle} not found in surveyExl")
                    continue

                # get rule in the surveyExl App
                rule = self.app4Survey1.range(f"{self.ruleCol}{answerRow}").value
                quesType = self.app4Survey1.range(f"{self.ruleTypeCol}{answerRow}").value
                # TODO: 判分的时候总是用旧数据
                stuff.scoreLst[questionNum] = judgeAnswerGrade(answer, rule, quesType)

                if stuff.scoreLst[questionNum] == -1:
                    print(f"answer: {answer}\n"
                          f"rule: {rule}\n"
                          f"questTitle: {questTitle}\n"
                          f"answerRow: {answerRow}\n"
                          f"quesType: {quesType}\n"
                          f"score: {stuff.scoreLst[questionNum]}")

                debugScoreLst.append([stuff.name, questTitle, quesType, answer, rule, stuff.scoreLst[questionNum]])

        # if debug on, save the debugScoreLst to csv with current time
        if debug:
            with open(f"debugScoreLst_{time.strftime('%Y%m%d%H%M%S')}.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerows([["name", "questTitle", "quesType", "answer", "rule", "score"]])
                writer.writerows(debugScoreLst)

        return stuffLst

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

    def genSummaryFile(self):
        """
        generate the summary file of the surveyExl
        :return: None
        """
        # Step1: get the department dict
        self.__setAllDepartmentDict()
        # Step2: generate the summary file
        self.addSheet1_surveyResult()
        self.addSheet2_surveyScore()
        self.addSheet3_surveyResultByYear()
        self.addSheet4_surveyScoreByYear()

        # save
        self.surveyExl.save(savePath)

    def genDepartmentFile(self):
        """
        generate the department file of the surveyExl
        :return: None
        """
        # Step1: get the department dict
        self.__setAllDepartmentDict()
        # Step2: generate the department file

    def genAllFile(self):
        """
        generate all file, include Summarization and Single Department
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

