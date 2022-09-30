#  Author : Github: @GWillS163
#  Time: $(Date)

#  Author : Github: @GWillS163
#  Time: $(Date)
import datetime

from shtOperation import *
from shtDataCalc import *
from scoreJudge import *
import csv
import os.path
import time
import xlwings as xw


class Excel_Operation:
    def __init__(self, surveyExlPath, scrExlPh,
                 savePath, fileYear, fileName,
                 surveyTestShtName, sht1ModuleName, sht2ModuleName, sht3ModuleName, sht4ModuleName,
                 sht1Name, sht2Name, sht3Name, sht4Name,
                 sht4DataRowRange=[4, 53]
                 ):
        """
        :param surveyExlPath: the path of the survey excel
        :param surveyExlPath:
        :param scrExlPh:
        :param savePath:
        :param fileYear:
        :param fileName:
        """
        self.debugPath = "save\\debugScoreLst"
        self.sumSavePath = paramsCheckExist(surveyExlPath, scrExlPh,
                                            savePath, fileYear, fileName)

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

        # Saving File Settings
        # 保存的结果表 配置
        self.fileYear = getCurrentYear(fileYear)
        self.fileName = fileName

        self.orgShtName = '行政机构组织'
        self.otherTitle = "其他人员"
        self.lv2AvgTitle = "二级单位成绩"

        # 输入配置-分数表
        self.scoreExlTitle = None  # 存放scoreExl的标题

        # 输入配置-规则表 修改后请核对以下配置
        self.surveyQuesCol = "E"  # 题目列
        self.surveyRuleCol = "J"  # 赋分规则列
        self.surveyQuesTypeCol = "G"  # 题目类型列
        paramsCheckSurvey(self.surveyExl, [surveyTestShtName, sht2ModuleName, sht3ModuleName, sht4ModuleName])
        self.sht0TestSurvey = self.surveyExl.sheets[surveyTestShtName]  # "测试问卷"
        # module settings
        self.sht1Module = self.surveyExl.sheets[sht1ModuleName]  # "调研结果_输出模板"
        self.sht2Module = self.surveyExl.sheets[sht2ModuleName]  # "调研成绩_输出模板"
        self.sht3Module = self.surveyExl.sheets[sht3ModuleName]  # "调研结果（2022年）_输出模板"
        self.sht4Module = self.surveyExl.sheets[sht4ModuleName]  # "调研成绩（2022年）_输出模板"

        self.deptCopyHeight = 35  # 从总表复制到 各个部门表时的高度
        self.lv1Name = "北京公司"
        # Sheet1: survey settings
        self.sht1NameRes = sht1Name
        self.sht1IndexCopyFromMdlScp = "A1:F32"
        self.sht1TitleCopyFromMdlScp = "F1:KZ2"
        self.sht1TitleCopyTo = "G1"
        self.sht1DataColRan = "G:KZ"
        # Sheet2:
        self.sht2NameGrade = sht2Name
        self.sht2TitleCopyFromMdlScp = "D1:L2"
        self.sht2TitleCopyTo = "D1"
        self.sht2IndexCopyFromSvyScp = "A1:K32"
        self.sht2IndexCopyTo = "A1"
        self.sht2WgtLstScp = "C3:C13"
        self.sht2DeleteRowLst = [4, 5, 8, 9, 10, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 25, 27]
        self.sht2DeleteCopiedRowScp = "A32:A55"  # TODO: 要删除的部分需要动态获取 党廉&纪检 的区间
        self.sht2DeleteCopiedColScp = "C1:J1"
        # Sheet3:
        self.sht3NameResYear = sht3Name
        self.sht3IndexCopyFromSvyScp = "A1:J32"
        self.sht3DataColRan = "K:AZ"
        self.sht3TitleCopyFromMdlScp = "L1:BA2"
        self.sht3TitleCopyTo = "K1"
        # Sheet4:
        self.sht4NameScoreYear = sht4Name
        self.sht4IndexFromSht2Scp = 'A4:B52'
        self.sht4TitleFromSht2Scp = 'A1:C17'
        self.sht4TitleCopyTo = 'A1'
        self.sht4SumTitleFromMdlScp = "P1:R3"
        self.sht4SumTitleCopyTo = "P1"
        self.sht4DataRowRan = range(sht4DataRowRange[0],
                                    sht4DataRowRange[1])

    def close_excel(self):
        self.surveyExl.close()
        self.scoreExl.close()
        self.app4Survey1.quit()
        self.app4Score2.quit()

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
        shtCopyTo(self.sht0TestSurvey, self.sht1IndexCopyFromMdlScp,
                  sht1_lv2Result, self.sht1IndexCopyFromMdlScp.split(":")[0])
        # Step2.2: copy title
        shtCopyTo(self.sht1Module, self.sht1TitleCopyFromMdlScp,
                  sht1_lv2Result, self.sht1TitleCopyTo)  # sht1_tltScope = "F1:KZ2"
        return sht1_lv2Result

    # def addSheet1_singleDepartment(self, deptUnitScp):
    #     """
    #     add a single department to the sht1_lv2Result
    #     :param deptUnitScp:
    #     :return:
    #     """
    #     sht1_lv2Result = self.deptResultExl.sheets.add(self.sht1NameRes)
    #
    #     # Step2.1: copy left column the surveySht to sht1 partially with style
    #     shtCopyTo(self.surveyTestSht, self.sht1CopyFromMdlColScp,
    #               sht1_lv2Result, self.sht1CopyFromMdlColScp.split(":")[0])
    #     shtCopyTo(self.sht1Module, deptUnitScp,
    #               sht1_lv2Result, self.sht1TitleCopyTo)  # sht1_tltScope = "F1:KZ2"
    #
    #     return sht1_lv2Result

    def addSheet2_surveyGrade(self):
        """
        generate sheet2 of the surveyExl, which is the survey with weight
        :return: None
        """

        # Step1: 新增Sheet2 - add new sheet and define module sheet
        sht2_lv2Score = self.resultExl.sheets.add(self.sht2NameGrade, after=self.sht1NameRes)

        print("Sheet2 表头和侧栏部分处理 - header and sidebar section")
        sht2_lv2Score.range("B1").column_width = 18.8
        print("Step2: 整体复制侧栏 - copy left column the surveySht to sht1, with style")
        shtCopyTo(self.sht0TestSurvey, self.sht2IndexCopyFromSvyScp, sht2_lv2Score, self.sht2IndexCopyTo)
        print("Step2.1 删除多余行(党廉&纪检) - delete the row of left column redundant")
        sht2_lv2Score.range(self.sht2DeleteCopiedRowScp).api.EntireRow.Delete()
        print("Step2.2: 删除左侧多余单元行 - delete the row of left column redundant")
        lv2UnitColLtr = "B"
        weightColLtr = "K"
        startRow = 3
        print("Step2.2.1: 删除多余行 - delete the row of left column redundant")
        sht2UnitScp = getShtUnitScp(sht2_lv2Score, startRow, 40, lv2UnitColLtr, "D")
        print("Step2.2.2: 为单元格重新计算权重 - recalculate the weight to the cell")
        # 给所有单元格边缘增加偏移 - add offset to all cells edge
        sht2UnitScpOffsite = [[edge + startRow for edge in eachUnit] for eachUnit in sht2UnitScp]
        resetUnitSum(sht2_lv2Score, sht2UnitScpOffsite, weightColLtr)
        sht2DeleteRowLst = getSht2DeleteRowLst(sht2UnitScpOffsite)
        for _ in range(len(sht2DeleteRowLst)):
            row = sht2DeleteRowLst.pop()
            sht2_lv2Score.range(f"{lv2UnitColLtr}{row}").api.EntireRow.Delete()
        print("Step2.3 删除多余列 - delete the column C to I")
        sht2_lv2Score.range(self.sht2DeleteCopiedColScp).api.EntireColumn.Delete()

        print("Step3: 整体复制title - copy title")
        shtCopyTo(self.sht2Module, self.sht2TitleCopyFromMdlScp, sht2_lv2Score, self.sht2TitleCopyTo)
        # Step2.3 增加合计行 -  add summary row
        sht2OprAddSummaryRows(sht2_lv2Score)

        return sht2_lv2Score

    # def addSheet2_singleDepartment(self, deptUnitScp):
    #     """
    #     add a single department to the sht2_lv2Score
    #     重复操作，可以考虑合并
    #     :param deptUnitScp:
    #     :return:
    #     """
    #     sht2_lv2Score = self.deptResultExl.sheets.add(self.sht2NameGrade, after=self.sht1NameRes)
    #
    #     """Sheet2 表头和侧栏部分处理"""
    #     # Step2: copy left column the surveySht to sht1, with style
    #     shtCopyTo(self.surveyTestSht, self.sht2IndexCopyFromColScp, sht2_lv2Score, self.sht2IndexCopyTo)
    #     # Step2.1: delete the row of left column redundant
    #     for row in self.sht2DeleteRowLst:
    #         sht2_lv2Score.range(f"B{row}").api.EntireRow.Delete()
    #     sht2_lv2Score.range("B1").column_width = 18.8
    #     # Step2.2 delete the column C to I
    #     sht2_lv2Score.range(self.sht2DeleteCopiedColScp).api.EntireColumn.Delete()
    #     sht2_lv2Score.range(self.sht2DeleteCopiedRowScp).api.EntireRow.Delete()
    #
    #     # Step3: copy title
    #     shtCopyTo(self.sht2Module, deptUnitScp, sht2_lv2Score, self.sht2TitleCopyTo)
    #     # Step2.3 add summary row
    #     sht2OprAddSummaryRows(sht2_lv2Score)
    #
    #     return sht2_lv2Score

    def clacSheet2_surveyGrade(self, sht2_lv2Score, sht1WithLv):
        # 通过权重计算得到sht2WithLv TODO: 把参数抽调上去
        # TODO: 权重列表不是动态
        sht2WgtLstScp = "C3:C" + str(sht2_lv2Score.used_range.last_cell.row)
        sht2WgtLst = sht2_lv2Score.range(sht2WgtLstScp).value
        assert None not in sht2WgtLst, "权重列表中存在空值"
        lv2UnitSpan = getShtUnitScp(self.sht0TestSurvey, startRow=3, endRow=40,
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
        shtCopyTo(self.sht0TestSurvey, self.sht3IndexCopyFromSvyScp, sht3_ResYear, self.sht3IndexCopyFromSvyScp.split(":")[0])
        shtCopyTo(self.sht3Module, self.sht3TitleCopyFromMdlScp, sht3_ResYear, self.sht3TitleCopyTo)

        return sht3_ResYear

    def addSheet4_surveyGradeByYear(self):
        """
        generate sheet4 of the surveyExl, which is the survey with weight
        :return: None
        """
        print("Step1: 新增Sheet4 - add new sheet")
        sht4_surveyGradeByYear = self.resultExl.sheets.add(self.sht4NameScoreYear, after=self.sht3NameResYear)
        sht2_lv2Score = self.resultExl.sheets[self.sht2NameGrade]

        print("Step2: 复制左侧栏 - copy left column the surveySht to sht1, with style")
        sht2_lv2Score.api.Range(self.sht4TitleFromSht2Scp).Copy()
        sht4_surveyGradeByYear.api.Range(self.sht4TitleCopyTo).PasteSpecial(Transpose=True)
        shtCopyTo(self.sht4Module, self.sht4IndexFromSht2Scp,
                  sht4_surveyGradeByYear, self.sht4IndexFromSht2Scp.split(":")[0])

        print("Step3: 粘贴汇总title - summarize Title patch")
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

    def getStaffScoreLst(self, staffScoreList):
        """
        通过所有员工列表获得员工的分数列表 {二级部门:{三级部门: [[分数, 分数], [分数, 分数]]}}
        from the staffWithLv, get the scoreLst

        get the staff score list from the surveySht
        :param staffScoreList: {lv2Depart:{lv3Depart: [stuff, stuff]}}
        :return: {lv2Depart:{lv3Depart: [[score], [score]]}}
        """
        debugScoreLst = []
        # get the score of each stuff
        for stuff in staffScoreList:
            # every stuff need to get the all score
            for questionNum in range(len(self.scoreExlTitle.answerLst)):
                if not stuff.answerLst[questionNum]:
                    continue
                # 得到每个问题的序号 - get every questTitle by questTitle num
                questTitle = self.scoreExlTitle.answerLst[questionNum]
                # 得到员工答案 - get stuff answer
                answer = stuff.answerLst[questionNum]
                if not answer:
                    stuff.scoreLst[questionNum] = None
                    continue
                # 找到问题所属判分规则 - locate which row is rule by questTitle in scoreExl
                (answerRow, rule) = getRuleByQuestion(questTitle, self.sht0TestSurvey,
                                                      self.surveyQuesCol, self.surveyRuleCol)
                if rule is None:
                    continue
                quesType = self.sht0TestSurvey.range(f"{self.surveyQuesTypeCol}{answerRow}").value
                stuff.scoreLst[questionNum] = judgeAnswerGrade(answer, rule, quesType)

                if stuff.scoreLst[questionNum] == -1:
                    print(f"answer: {answer}\n"
                          f"rule: {rule}\n"
                          f"questTitle: {questTitle}\n"
                          f"answerRow: {answerRow}\n"
                          f"quesType: {quesType}\n"
                          f"score: {stuff.scoreLst[questionNum]}")
                debugScoreLst.append([stuff.name, questTitle, quesType, answer, rule, stuff.scoreLst[questionNum]])
        return staffScoreList, debugScoreLst

    def getStaffScoreWithLv(self, staffScoreWithLv, debug=True):
        """
        给每个人打分 得到stuffScoreWithLv Dict:
        :param staffScoreWithLv:
        :param debug: whether save to debug csv
        :return:{lv2Depart: {lv3Depart: [stuff1, stuff2, ...]}}
        """
        print("getScore function Start")
        debugScoreLst = []  # store [name, questTitle, answer, rule, score] for debug
        # iterate all lv2 as key
        for lv2 in staffScoreWithLv:
            # iterate all lv3 as key
            for lv3 in staffScoreWithLv[lv2]:
                stuffScoreList, debugScoreLst = self.getStaffScoreLst(staffScoreWithLv[lv2][lv3])
                staffScoreWithLv[lv2][lv3] = stuffScoreList
                debugScoreLst += debugScoreLst
        # if debug on, save the debugScoreLst to csv with current time
        if debug:
            saveDebugFile(debugScoreLst, self.debugPath)
        return staffScoreWithLv

    def genSummaryFile(self, summaryFileSavePath):
        """获得汇总的一个文件
        generate the summary file of the surveyExl
        :return: sht2WithLv
        """
        # Add Title & column
        sht1_lv2Result = self.addSheet1_surveyResult()
        print("sheet1 无数据页面生成完成")
        sht2_lv2Score = self.addSheet2_surveyGrade()
        print("sheet2 无数据页面生成完成")
        sht3_ResYear = self.addSheet3_surveyResultByYear()
        print("sheet3 无数据页面生成完成")
        sht4_surveyGradeByYear = self.addSheet4_surveyGradeByYear()
        print("sheet4 无数据页面生成完成")

        # Excel Data Process
        # Sheet 1
        # two Methods to set data
        # sht1PlcScoreByPD(self.sht1Module, sht1_lv2Result, staffWithLv, self.sht1MdlTltScope, dataStart)
        sht1SetData(sht1_lv2Result, self.sht1WithLv, getTltColRange(self.sht1DataColRan))

        # Sheet 2
        # TODO: 这里放置Data真的没问题吗？
        self.sht2WithLv = self.clacSheet2_surveyGrade(sht2_lv2Score, self.sht1WithLv)
        sht2SetData(sht2_lv2Score, self.sht2WithLv, getTltColRange(self.sht2IndexCopyFromSvyScp))

        # Sheet 3
        sht3WithLv = getSht3WithLv(self.sht1WithLv, self.lv1Name)
        sht3SetData(sht3_ResYear, sht3WithLv, self.sht3DataColRan, self.lv1Name)

        # Sheet 4
        sht4Hie = getSht4Hierarchy(sht4_surveyGradeByYear)
        sht4WithLv = getSht4WithLv(self.sht2WithLv, sht4Hie, self.lv1Name)
        sht4SetData(sht4_surveyGradeByYear, sht4WithLv, self.sht4DataRowRan, self.lv1Name)

        # Save Excel
        self.resultExl.save(summaryFileSavePath)

    def genDepartmentFile(self, fileNamePathPrefix):
        """ 通过汇总表生成所有部门文件, 生成固定的标题侧栏，然后填充数据-保存-清空数据
        generate the department file of the surveyExl， generate the fixed title sidebar, then fill data-save-clear data
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

        # 填充数据 - 保存 - 删除
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

            # Method1: Clear the sheet for next loop dynamically
            # sht1Dept.activate()
            # dltOneDptData(sht1Dept, self.sht1TitleCopyTo, self.deptCopyHeight,
            #               sht1BorderR, sht1BorderL)
            # if deptName in deptUnitSht2:
            #     sht2Dept.activate()
            #     dltOneDptData(sht2Dept, self.sht2TitleCopyTo, self.deptCopyHeight,
            #                   sht2BorderL, sht2BorderR)

            # Method2
            borderWidth = getColNum(sht1BorderR) - getColNum(sht1BorderL)
            borderStart = getColNum(self.sht1TitleCopyTo[0])
            borderEnd = getColLtr(borderStart + borderWidth)
            sht1Dept.activate()
            sht1Dept.range(f"{self.sht1TitleCopyTo}:{borderEnd}{self.deptCopyHeight}").api.Delete()
            if deptName in deptUnitSht2:
                borderWidth = getColNum(sht2BorderR) - getColNum(sht2BorderL)
                borderStart = getColNum(self.sht2TitleCopyTo[0])
                borderEnd = getColLtr(borderStart + borderWidth)
                sht2Dept.activate()
                sht2Dept.range(f"{self.sht2TitleCopyTo}:{borderEnd}{self.deptCopyHeight}").api.Delete()

        deptResultExl.close()

    def getData(self):
        # orgSht = self.surveyExl.sheets[self.orgShtName]
        # orgDict = readOrgDict(orgSht)

        staffWithLv = self.getStuffDict()
        for stu in staffWithLv:
            print(stu)
        print(self.scoreExlTitle)
        staffWithLv = self.getStaffScoreWithLv(staffWithLv)
        scoreWithLv = getScoreWithLv(staffWithLv)
        print("展示分数：")
        # print(stuffWithLv) all score
        for lv2 in staffWithLv:
            for lv3 in staffWithLv[lv2]:
                for stu in staffWithLv[lv2][lv3]:
                    print(stu.name, stu.scoreLst)

        sht1WithLv = getSht1WithLv(scoreWithLv)
        print("sht1WithLv: ", sht1WithLv)
        self.scoreExl.close()
        self.app4Score2.quit()
        return sht1WithLv

    def fillData(self, sht1WithLv):
        """
        使用sheet1的数据计算出来接下来的数据，然后填充到excel中
        use sheet1 data to calculate the data of the next sheet, then fill it into the excel
        :param sht1WithLv: 
        :return: 
        """""
        # Step3:    Set data
        if sht1WithLv:
            self.sht1WithLv = sht1WithLv  # mock data, will be deleted

        # get current year
        if not self.fileYear:
            self.fileYear = datetime.datetime.now().year

        # 生成两个文件 — 汇总表 和 部门表
        self.genSummaryFile(self.sumSavePath)
        self.surveyExl.close()
        self.app4Survey1.quit()
        # generate each department file
        self.genDepartmentFile(self.sumSavePath)
        self.resultExl.close()
        self.app4Result3.quit()

    def run(self):
        """
        run the whole process, the main function.
        :return:
        """
        self.getData()
        self.fillData(self.sht1WithLv)
        print("All done")
