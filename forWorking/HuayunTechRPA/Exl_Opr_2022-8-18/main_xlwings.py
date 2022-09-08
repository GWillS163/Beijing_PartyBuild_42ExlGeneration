#  Author : Github: @GWillS163
#  Time: $(Date)
import datetime

from shtOperation import *
from shtDataCalc import *
from scoreJudge import *

import csv
import os.path
import re
import time
import xlwings as xw


class Excel_Operation:
    def __init__(self, surveyExlPath, scrExlPh,
                 savePath, fileYear, fileName, fileOrgCode,
                 ):
        """
        :param surveyExlPath: the path of the survey excel
        :param surveyExlPath:
        :param scrExlPh:
        :param savePath:
        :param fileYear:
        :param fileName:
        :param fileOrgCode:
        """

        self.deptCopyHeight = 35  # 从总表复制到 各个部门表时的高度
        self.lv1Name = "北京公司"
        self.sht2WgtLstScp = "C3:C13"
        self.sht2DeleteRowLst = [31, 29, 27, 24, 18, 17, 15, 14, 13, 12, 11, 8, 5]
        self.sht2DeleteCopiedRowScp = "A14:A19"
        self.sht2DeleteCopiedColScp = "C1:J1"
        self.surveyExlPath = surveyExlPath
        self.scoreExlPath = scrExlPh

        self.app4Survey1 = xw.App(visible=True, add_book=False)
        self.app4Score2 = xw.App(visible=True, add_book=False)
        self.app4Result3 = xw.App(visible=True, add_book=False)

        self.app4Survey1.display_alerts = False
        self.app4Score2.display_alerts = False
        self.app4Result3.display_alerts = False
        self.app4Survey1.api.CutCopyMode = False
        self.app4Score2.api.CutCopyMode = False
        self.app4Result3.api.CutCopyMode = False

        # open the survey file with xlwings
        self.surveyExl = self.app4Survey1.books.open(surveyExlPath)
        self.scoreExl = self.app4Score2.books.open(scrExlPh)
        self.resultExl = self.app4Result3.books.add()

        # public variable
        self.departmentDict = {}

        # File Settings
        # 保存的表 配置
        self.fileYear = getCurrentYear(fileYear)
        self.fileName = "PartyBuildingResultSurvey"
        self.orgCode = "20900000"

        self.savePath = ".\\"
        self.orgShtName = '行政机构组织'

        self.otherTitle = "其他人员"
        self.lv2AvgTitle = "二级单位成绩"

        # 输入配置-分数表
        self.scoreExlTitle = None  # 存放scoreExl的标题

        # 输入配置-规则表 修改后请核对以下配置
        self.surveyQuesCol = "E"  # 题目列
        self.surveyRuleCol = "J"  # 赋分规则列
        self.surveyQuesTypeCol = "G"  # 题目类型列
        self.surveyTestSht = self.surveyExl.sheets["测试问卷"]
        # module settings
        self.sht1Module = self.surveyExl.sheets["调研结果_输出模板"]
        self.sht2Module = self.surveyExl.sheets["调研成绩_输出模板"]
        self.sht3Module = self.surveyExl.sheets["调研结果（2022年）_输出模板"]
        self.sht4Module = self.surveyExl.sheets["调研成绩（2022年）_输出模板"]

        # Sheet1: survey settings
        self.sht1NameRes = "调研结果"  # "调研问卷(未加权)"
        self.sht1CopyFromMdlColScp = "A1:F32"
        self.sht1TitleCopyFromMdlScp = "F1:KZ2"
        self.sht1TitleCopyTo = "G1"
        self.sht1DataColRan = "G:KZ"
        # Sheet2:
        self.sht2NameGrade = "调研成绩"  # "调研问卷(加权)"
        self.sht2TitleCopyFromMdlScp = "D1:L2"
        self.sht2TitleCopyTo = "D1"
        self.sht2IndexCopyFromColScp = "A1:K32"
        self.sht2IndexCopyTo = "A1"
        # Sheet3:
        self.sht3NameResYear = "调研结果（2022年）"
        self.sht3ColRan = "A1:J32"
        self.sht3DataCol = "K:AZ"
        self.sht3TitleCopyFromScp = "L1:BA2"
        self.sht3TitleCopyTo = "K1"
        # Sheet4:
        self.sht4NameScoreYear = "调研成绩（2022年）"
        self.sht4IndexFromSht2Scp = 'A4:B52'
        self.sht4TitleFromSht2Scp = 'A1:C17'
        self.sht4TitleCopyTo = 'A1'
        self.sht4SumTitleFromMdlScp = "P1:R3"
        self.sht4SumTitleCopyTo = "P1"
        self.sht4DataRowRan = range(4, 53)

    def close_excel(self):
        self.surveyExl.close()
        self.scoreExl.close()
        self.app4Survey1.quit()
        self.app4Score2.quit()

    # def __convertDict2Lst(self, departmentDict):
    #     """
    #     convert Dict 2 List
    #     :param departmentDict:
    #     :param department: dict
    #     :return: [["二级部门", "二级部门", "二级部门"],
    #              ["三级部门1","三级部门2"]]
    #     """
    #     # Step2: convertDict2Lst
    #     result_lst = [[], []]
    #     for layer2 in departmentDict:
    #         for layer3 in departmentDict[layer2]:
    #             if not layer3:
    #                 continue
    #             result_lst[0].append(layer2)
    #             result_lst[1].append(layer3)
    #         # add other items
    #         result_lst[0].append("")
    #         result_lst[1].append(self.otherTitle)
    #         result_lst[0].append("")
    #         result_lst[1].append(self.lv2AvgTitle)
    #     return result_lst
    #
    # def __getRawScoreTb(self, scope="A1:M10"):
    #     # get all scoreExl sheet0 content
    #     return self.scoreExl.sheets[0].range(scope).value

    def addSheet1_surveyResult(self):
        """
        generate sheet1 of the surveyExl, which is the survey without weight
        :return:
        """
        # titleStart, r = self.sht1MdlTltScope.split(":")
        # dataStart = r + str(int(self.sht1MdlTltScope.split(":")[1][-1]) + 1)
        # Step1: add new sheet and define module sheet
        sht1_lv2Result = self.resultExl.sheets.add(self.sht1NameRes)

        # Step2.1: copy left column the surveySht to sht1 partially with style
        shtCopyTo(self.surveyTestSht, self.sht1CopyFromMdlColScp,
                  sht1_lv2Result, self.sht1CopyFromMdlColScp.split(":")[0])
        # Step2.2: copy title
        shtCopyTo(self.sht1Module, self.sht1TitleCopyFromMdlScp,
                  sht1_lv2Result, self.sht1TitleCopyTo)  # sht1_tltScope = "F1:KZ2"

        return sht1_lv2Result

    def addSheet1_singleDepartment(self, deptUnitScp):
        """
        add a single department to the sht1_lv2Result
        :param deptUnitScp:
        :return:
        """
        sht1_lv2Result = self.deptResultExl.sheets.add(self.sht1NameRes)

        # Step2.1: copy left column the surveySht to sht1 partially with style
        shtCopyTo(self.surveyTestSht, self.sht1CopyFromMdlColScp,
                  sht1_lv2Result, self.sht1CopyFromMdlColScp.split(":")[0])
        # TODO:Step2.2: copy partial title
        shtCopyTo(self.sht1Module, deptUnitScp,
                  sht1_lv2Result, self.sht1TitleCopyTo)  # sht1_tltScope = "F1:KZ2"

        return sht1_lv2Result

    def addSheet2_surveyGrade(self):
        """
        generate sheet2 of the surveyExl, which is the survey with weight
        :return: None
        """

        # Step1: add new sheet and define module sheet
        sht2_lv2Score = self.resultExl.sheets.add(self.sht2NameGrade, after=self.sht1NameRes)

        """Sheet2 表头和侧栏部分处理"""
        # Step2: copy left column the surveySht to sht1, with style
        shtCopyTo(self.surveyTestSht, self.sht2IndexCopyFromColScp, sht2_lv2Score, self.sht2IndexCopyTo)
        # Step2.1: delete the row of left column redundant
        for row in self.sht2DeleteRowLst:
            sht2_lv2Score.range(f"B{row}").api.EntireRow.Delete()
        sht2_lv2Score.range("B1").column_width = 18.8
        # Step2.2 delete the column C to I
        sht2_lv2Score.range(self.sht2DeleteCopiedColScp).api.EntireColumn.Delete()
        sht2_lv2Score.range(self.sht2DeleteCopiedRowScp).api.EntireRow.Delete()

        # Step3: copy title
        shtCopyTo(self.sht2Module, self.sht2TitleCopyFromMdlScp, sht2_lv2Score, self.sht2TitleCopyTo)
        # Step2.3 add summary row
        sht2OprAddSummaryRows(sht2_lv2Score)

        return sht2_lv2Score

    def addSheet2_singleDepartment(self, deptUnitScp):
        """
        add a single department to the sht2_lv2Score
        重复操作，可以考虑合并
        :param deptUnitScp:
        :return:
        """
        sht2_lv2Score = self.deptResultExl.sheets.add(self.sht2NameGrade, after=self.sht1NameRes)

        """Sheet2 表头和侧栏部分处理"""
        # Step2: copy left column the surveySht to sht1, with style
        shtCopyTo(self.surveyTestSht, self.sht2IndexCopyFromColScp, sht2_lv2Score, self.sht2IndexCopyTo)
        # Step2.1: delete the row of left column redundant
        for row in self.sht2DeleteRowLst:
            sht2_lv2Score.range(f"B{row}").api.EntireRow.Delete()
        sht2_lv2Score.range("B1").column_width = 18.8
        # Step2.2 delete the column C to I
        sht2_lv2Score.range(self.sht2DeleteCopiedColScp).api.EntireColumn.Delete()
        sht2_lv2Score.range(self.sht2DeleteCopiedRowScp).api.EntireRow.Delete()

        # Step3: copy title
        shtCopyTo(self.sht2Module, deptUnitScp, sht2_lv2Score, self.sht2TitleCopyTo)
        # Step2.3 add summary row
        sht2OprAddSummaryRows(sht2_lv2Score)

        return sht2_lv2Score

    def clacSheet2_surveyGrade(self, sht2_lv2Score, sht1WithLv):
        # 通过权重计算得到sht2WithLv
        sht2WgtLst = sht2_lv2Score.range(self.sht2WgtLstScp).value
        lv2UnitSpan = getShtUnitScp(self.surveyTestSht, startRow=3, endRow=40,
                                    unitCol="B", contentCol="D",
                                    skipCol="A", skipWords=["党廉", "纪检"])
        lv1UnitSpan = getShtUnitScp(sht2_lv2Score, startRow=3, endRow=40,
                                    unitCol="A", contentCol="B")
        sht2WithLv = getSht2WithLv(sht1WithLv, lv2UnitSpan, lv1UnitSpan, sht2WgtLst)

        return sht2WithLv

    def addSheet3_surveyResultByYear(self):
        """
        generate sheet3 of the surveyExl, which is the survey without weight
        :return: None
        """

        # Step1: add new sheet and define module sheet
        sht3_ResYear = self.resultExl.sheets.add(self.sht3NameResYear, after=self.sht2NameGrade)

        # Step2: Set title

        shtCopyTo(self.surveyTestSht, self.sht3ColRan, sht3_ResYear, self.sht3ColRan.split(":")[0])
        shtCopyTo(self.sht3Module, self.sht3TitleCopyFromScp, sht3_ResYear, self.sht3TitleCopyTo)

        return sht3_ResYear

    def addSheet4_surveyGradeByYear(self):
        """
        generate sheet4 of the surveyExl, which is the survey with weight
        :return: None
        """
        # Step1: add new sheet
        sht4_surveyGradeByYear = self.resultExl.sheets.add(self.sht4NameScoreYear, after=self.sht3NameResYear)
        sht2_lv2Score = self.resultExl.sheets[self.sht2NameGrade]

        # Step2: copy left column the surveySht to sht1, with style
        sht2_lv2Score.api.Range(self.sht4TitleFromSht2Scp).Copy()
        sht4_surveyGradeByYear.api.Range(self.sht4TitleCopyTo).PasteSpecial(Transpose=True)
        shtCopyTo(self.sht4Module, self.sht4IndexFromSht2Scp,
                  sht4_surveyGradeByYear, self.sht4IndexFromSht2Scp.split(":")[0])

        # summarize Title patch
        shtCopyTo(self.sht4Module, self.sht4SumTitleFromMdlScp,
                  sht4_surveyGradeByYear, self.sht4SumTitleCopyTo)

        return sht4_surveyGradeByYear

    def getStuffDict(self, departmentScope="A1:AM10"):
        """
        get the stuff list from the surveySht
        :param departmentScope: A:AM 是 题目scope 1:10是人数
        :return: stuffLst
        """
        staffWithLv = {}
        scoreWithLv = {}
        content = self.app4Score2.range(departmentScope).value
        for i in content:
            if not all(i):
                continue
            if i[0] == "序号":
                self.scoreExlTitle = Stuff(i[1], i[2], i[3], i[4], i[5], i[6], i[9:])
                continue
            stu = Stuff(i[1], i[2], i[3], i[4], i[5], i[6], i[9:])
            # print(stu)
            if stu.lv2Depart not in staffWithLv:
                staffWithLv[stu.lv2Depart] = {}
                scoreWithLv[stu.lv2Depart] = {}
            if not stu.lv3Depart:
                stu.lv3Depart = self.otherTitle
            if stu.lv3Depart not in staffWithLv[stu.lv2Depart]:
                staffWithLv[stu.lv2Depart][stu.lv3Depart] = []
                scoreWithLv[stu.lv2Depart][stu.lv3Depart] = []
            staffWithLv[stu.lv2Depart][stu.lv3Depart].append(stu)
            scoreWithLv[stu.lv2Depart][stu.lv3Depart].append(stu.scoreLst)
        return staffWithLv  # , scoreWithLv

    def getStuffScoreLst(self, stuffScoreList):
        debugScoreLst = []
        # get the score of each stuff
        for stuff in stuffScoreList:
            # every stuff need to get the all score
            for questionNum in range(len(self.scoreExlTitle.answerLst)):
                if not stuff.answerLst[questionNum]:
                    continue
                # get every questTitle by questTitle num
                questTitle = self.scoreExlTitle.answerLst[questionNum]
                # get stuff answer
                answer = stuff.answerLst[questionNum]
                if not answer:
                    stuff.scoreLst[questionNum] = None
                    continue
                # locate which row is rule by questTitle in scoreExl
                answerRow = -1
                for row in range(3, 40):
                    # find the cell in the surveyExl by Question column
                    ruleQuest = self.surveyTestSht.range(f"{self.surveyQuesCol}{row}").value
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
                rule = self.app4Survey1.range(f"{self.surveyRuleCol}{answerRow}").value
                quesType = self.app4Survey1.range(f"{self.surveyQuesTypeCol}{answerRow}").value
                stuff.scoreLst[questionNum] = judgeAnswerGrade(answer, rule, quesType)

                if stuff.scoreLst[questionNum] == -1:
                    print(f"answer: {answer}\n"
                          f"rule: {rule}\n"
                          f"questTitle: {questTitle}\n"
                          f"answerRow: {answerRow}\n"
                          f"quesType: {quesType}\n"
                          f"score: {stuff.scoreLst[questionNum]}")
                debugScoreLst.append([stuff.name, questTitle, quesType, answer, rule, stuff.scoreLst[questionNum]])
        return stuffScoreList, debugScoreLst

    def getStuffAllScore(self, stuffScoreWithLv, debug=True):
        """给每个人打分
        {lv2Depart: {lv3Depart: [stuff1, stuff2, ...]}}
        :param stuffScoreWithLv:
        :param debug: save debug csv
        :return:
        """
        print("getScore function Start")
        debugScoreLst = []  # store [name, questTitle, answer, rule, score] for debug
        # iterate all lv2 as key
        for lv2 in stuffScoreWithLv:
            # iterate all lv3 as key
            for lv3 in stuffScoreWithLv[lv2]:
                stuffScoreList, debugScoreLst = self.getStuffScoreLst(stuffScoreWithLv[lv2][lv3])
                stuffScoreWithLv[lv2][lv3] = stuffScoreList
                debugScoreLst += debugScoreLst

        # if debug on, save the debugScoreLst to csv with current time
        if debug:
            with open(f"debugScoreLst_{time.strftime('%Y%m%d%H%M%S')}.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerows([["name", "questTitle", "quesType", "answer", "rule", "score"]])
                writer.writerows(debugScoreLst)

        return stuffScoreWithLv

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

    def genSummaryFile(self, sht1WithLv, summaryFileSavePath):
        """
        generate the summary file of the surveyExl
        :return: sht2WithLv
        """
        # Add Title & column
        sht1_lv2Result = self.addSheet1_surveyResult()
        sht2_lv2Score = self.addSheet2_surveyGrade()
        sht3_ResYear = self.addSheet3_surveyResultByYear()
        sht4_surveyGradeByYear = self.addSheet4_surveyGradeByYear()

        # Excel Data Process
        # Sheet 1
        # two Methods to set data
        # sht1PlcScoreByPD(self.sht1Module, sht1_lv2Result, staffWithLv, self.sht1MdlTltScope, dataStart)
        sht1SetData(sht1_lv2Result, sht1WithLv, getTltColRange(self.sht1DataColRan))

        # Sheet 2
        sht2WithLv = self.clacSheet2_surveyGrade(sht2_lv2Score, sht1WithLv)
        sht2SetData(sht2_lv2Score, sht2WithLv, getTltColRange(self.sht2IndexCopyFromColScp))

        # Sheet 3
        sht3WithLv = getSht3WithLv(sht1WithLv, self.lv1Name)
        sht3SetData(sht3_ResYear, sht3WithLv, self.sht3DataCol, self.lv1Name)

        # Sheet 4
        sht4Hie = getSht4Hierarchy(sht4_surveyGradeByYear)
        sht4WithLv = getSht4WithLv(sht2WithLv, sht4Hie, self.lv1Name)
        sht4SetData(sht4_surveyGradeByYear, sht4WithLv, self.sht4DataRowRan, self.lv1Name)

        # Save Excel
        self.resultExl.save(summaryFileSavePath)
        return sht2WithLv

    def genDepartmentFile(self, fileNamePathPrefix):
        """
        通过汇总表生成所有部门文件
        generate the department file of the surveyExl
        :return: None
        """

        # 从汇总表 获取 部门分类区间
        sht1Sum = self.resultExl.sheets[self.sht1NameRes]
        sht2Sum = self.resultExl.sheets[self.sht2NameGrade]
        deptUnitSht1 = getDeptUnit(sht1Sum, "F:KZ")
        deptUnitSht2 = getDeptUnit(sht2Sum, "D:P")
        # create new excel with xlwings
        deptResultExl = xw.Book()
        sht1Dept = deptResultExl.sheets.add(self.sht1NameRes)
        sht2Dept = deptResultExl.sheets.add(self.sht2NameGrade, after=sht1Dept)

        # 从汇总表 复制 边栏
        sht1Dept.activate()
        shtCopyTo(sht1Sum, "A1:F32", sht1Dept, "A1")
        sht2Dept.activate()
        shtCopyTo(sht2Sum, "A1:C20", sht2Dept, "A1")

        # for deptName, sht2DeptName in zip(deptUnitSht1, deptUnitSht2):
        sht2BorderL, sht2BorderR = "G", "Z"
        for deptName in deptUnitSht1:
            # add department data
            sht1BorderL, sht1BorderR = addOneDptData(sht1Sum, deptUnitSht1[deptName], self.deptCopyHeight,
                                                     sht1Dept, self.sht1TitleCopyTo)
            if deptName in deptUnitSht2:
                sht2BorderL, sht2BorderR = addOneDptData(sht2Sum, deptUnitSht2[deptName], self.deptCopyHeight,
                                                         sht2Dept, self.sht2TitleCopyTo)

            # Save Excel
            deptResultExl.save(f"{fileNamePathPrefix}_{deptName}.xlsx")

            # Clear the sheet for next loop dynamically
            borderWidth = getColNum(sht1BorderL) - getColNum(sht1BorderR)
            borderStart = getColNum(self.sht1TitleCopyTo[0])
            borderEnd = getColLtr(borderStart + borderWidth)
            sht1Dept.range(f"{self.sht1TitleCopyTo}:{borderEnd}{self.deptCopyHeight}").api.Delete()

            if deptName in deptUnitSht2:
                borderWidth = getColNum(sht2BorderL) - getColNum(sht2BorderR)
                borderStart = getColNum(self.sht2TitleCopyTo[0])
                borderEnd = getColLtr(borderStart + borderWidth)
                sht2Dept.range(f"{self.sht2TitleCopyTo}:{borderEnd}{self.deptCopyHeight}").api.Delete()

        deptResultExl.close()
        self.resultExl.close()

    def getDataDemo(self):
        # orgSht = self.surveyExl.sheets[self.orgShtName]
        # orgDict = readOrgDict(orgSht)

        # TODO: get score 注意切换到正确的sheet
        staffWithLv = self.getStuffDict()
        for stu in staffWithLv:
            print(stu)
        print(self.scoreExlTitle)
        staffWithLv = self.getStuffAllScore(staffWithLv)
        scoreWithLv = getScoreWithLv(staffWithLv)
        print("展示分数：")
        # print(stuffWithLv) all score
        for lv2 in staffWithLv:
            for lv3 in staffWithLv[lv2]:
                for stu in staffWithLv[lv2][lv3]:
                    print(stu.name, stu.scoreLst)

        sht1WithLv = getSht1WithLv(staffWithLv)
        print(sht1WithLv)

    def mockDataDemo(self):
        """without real data, just for demo"""
        # Step3:    Set data

        sht1WithLv = {'城区一分公司': {
            '建设中心': [9.0, 4.0, 4.0, 0.0, 6.0, 5.0, 10.0, 6.0, 8.0, 8.0, 8.0, 10.0, 6.0, 4.0, 7.0, 0.0, 4.0, 10.0, 10.0,
                     10.0, 7.0, 10.0, 4.0, 5.0, 8.0, 8.0, 4.0, 6.0, 8.0, 8.0],
            '市场部': [10.0, 10.0, 10.0, 0.0, 10.0, 8.0, 10.0, 10.0, 10.0, 10.0, 6.0, 10.0, 8.0, 10.0, 10.0, 0.0,
                    10.0, 8.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
            '二级单位': [9.5, 7.0, 7.0, 0.0, 8.0, 6.5, 10.0, 8.0, 9.0, 9.0, 7.0, 10.0, 7.0, 7.0, 8.5, 0.0, 7.0, 9.0, 10.0,
                     10.0, 8.5, 10.0, 7.0, 7.5, 9.0, 9.0, 7.0, 8.0, 9.0, 9.0]},
            '党委办公室（党群工作部、职能管理部党委）': {
                '党委工作室': [9.0, 4.0, 4.0, 0.0, 6.0, 5.0, 10.0, 6.0, 8.0, 8.0, 8.0, 10.0, 6.0, 4.0, 7.0, 0.0, 4.0, 10.0,
                          10.0,
                          10.0, 7.0, 10.0, 4.0, 5.0, 8.0, 8.0, 4.0, 6.0, 8.0, 8.0],
                '职能管理部党委办公室': [10.0, 10.0, 10.0, 0.0, 10.0, 8.0, 10.0, 10.0, 10.0, 10.0, 6.0, 10.0, 8.0, 10.0, 10.0,
                               0.0,
                               10.0, 8.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
                '二级单位': [9.5, 7.0, 7.0, 0.0, 8.0, 6.5, 10.0, 8.0, 9.0, 9.0, 7.0, 10.0, 7.0, 7.0, 8.5, 0.0, 7.0, 9.0,
                         10.0,
                         10.0, 8.5, 10.0, 7.0, 7.5, 9.0, 9.0, 7.0, 8.0, 9.0, 9.0]},
            '巡察工作办公室（党风廉政办公室）': {
                '主体责任支撑室': [10.0, 10.0, 10.0, 0.0, 10.0, 7.0, 10.0, 10.0, 10.0, 8.0, 4.0, 10.0, 10.0, 10.0, 10.0, 0.0,
                            10.0,
                            10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
                '二级单位': [10.0, 10.0, 10.0, 0.0, 10.0, 7.0, 10.0, 10.0, 10.0, 8.0, 4.0, 10.0, 10.0, 10.0, 10.0, 0.0,
                         10.0,
                         10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0]},
            '纪委办公室（职能管理部纪委）': {
                '综合组织室（职能管理部纪委办公室）': [10.0, 10.0, 10.0, 0.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0,
                                      10.0, 0.0, 4.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 8.0, 10.0,
                                      10.0,
                                      10.0],
                '二级单位': [10.0, 10.0, 10.0, 0.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 0.0,
                         4.0,
                         10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 8.0, 10.0, 10.0, 10.0]}}
        self.scoreExl.close()
        self.app4Score2.quit()
        # get current year
        if not self.fileYear:
            self.fileYear = datetime.datetime.now().year
        summaryFileName = f"{self.fileYear}_{self.fileName}_{self.orgCode}.xlsx"
        sumSavePath = os.path.join(self.savePath, summaryFileName)
        sht2WithLv = self.genSummaryFile(sht1WithLv, sumSavePath)
        self.surveyExl.close()
        self.app4Survey1.quit()
        # generate each department file
        self.genDepartmentFile(sumSavePath)

    def run(self):
        """
        run the whole process, the main function.
        :return:
        """
        print("All done")
