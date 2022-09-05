#  Author : Github: @GWillS163
#  Time: $(Date)

from shtOperation import *
from shtDataCalc import *
from scoreJudge import *

import csv
import os.path
import re
import time
import xlwings as xw


class Excel_Operation:
    def __init__(self, surveyExlPath, scrExlPh, moduleExlPh, resultExlPh):

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
        self.summarizeFileName = "汇总文件"  # without extension ".xlsx"
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
        self.sht1ColScope = "A1:F32"
        self.sht1MdlTltScope = "F1:KZ2"
        self.sht1TltStart = "G1"
        # Sheet2:
        self.sht2NameGrade = "调研成绩"  # "调研问卷(加权)"
        self.sht3ColRan = "A1:J32"
        # Sheet3:
        self.sht3NameResYear = "调研结果（2022年）"
        self.sht2ColRan = "A1:K32"
        self.sht2TltStart = "D1"
        # Sheet4:
        self.sht4NameScoreYear = "调研成绩（2022年）"


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

    def addSheet1_surveyResult(self, sht1WithLv):
        """
        generate sheet1 of the surveyExl, which is the survey without weight
        :param staffWithLv:
        :return:
        """
        titleStart, r = self.sht1MdlTltScope.split(":")
        dataStart = r + str(int(self.sht1MdlTltScope.split(":")[1][-1]) + 1)
        # Step1: add new sheet and define module sheet
        sht1_lv2Result = self.resultExl.sheets.add(self.sht1NameRes)

        # Step2.1: copy left column the surveySht to sht1 partially with style
        shtCopyTo(self.surveyTestSht, self.sht1ColScope,
                  sht1_lv2Result, self.sht1ColScope.split(":")[0])
        # Step2.2: copy title
        shtCopyTo(self.sht1Module, self.sht1MdlTltScope,
                  sht1_lv2Result, self.sht1TltStart)  # sht1_tltScope = "F1:KZ2"

        # Step4: place score below title
        # sht1PlcScoreByPD(self.sht1Module, sht1_lv2Result, staffWithLv, self.sht1MdlTltScope, dataStart)
        # TODO: need 需要另一种方式 遍历放置
        titleRan = getTltColRange("G:KZ")
        lv2 = None
        for colNum in titleRan:
            colLtr = getColLtr(colNum)
            curLv2 = sht1_lv2Result.range(colLtr + "1").value
            lv3 = sht1_lv2Result.range(colLtr + "2").value
            if lv2:
                lv2 = curLv2
            if not lv3:
                continue
            # print(lastLv2, lv3)
            if lv2 not in sht1WithLv:
                continue
            if lv3 not in sht1WithLv[lv2]:
                continue
            sht1_lv2Result.range(f"{colLtr}3").\
                options(Transpose=True).value = sht1WithLv[lv2][lv3]


    def addSheet2_surveyGrade(self, sht2WithLv, orgDict,
                               titleStart="C1", dataStart="C3"):
        """
        generate sheet2 of the surveyExl, which is the survey with weight
        :return: None
        """

        # Step1: add new sheet and define module sheet
        sht2_lv2Score = self.resultExl.sheets.add(self.sht2NameGrade, after=self.sht1NameRes)

        # Step2: Set title
        sht2SetColumnTitle(self.surveyTestSht, sht2_lv2Score, self.sht2Module,
                           self.sht2ColRan, self.sht2TltStart)

        # TODO: Step3: Set data
        # 纵向遍历每个(二)三级部门
        for col in range(3, 10):
            colLtr = getColLtr(col)
            lv3 = sht2_lv2Score.range(f"{colLtr}2").value
            if lv3 in sht2WithLv:
                # place score list vertically
                sht2_lv2Score.range(f"{colLtr}3").options(transpose=True).value = sht2WithLv[lv3]

        # Step2.3 add summary row
        # TODO: 计算C单元的总和， 其他列的总和
        sht2OprAddSummaryRows(sht2_lv2Score)

    def addSheet3_surveyResultByYear(self, sht2WithLv, orgDict,
                                     titleStart="K1", dataStart="K3"):
        """
        generate sheet3 of the surveyExl, which is the survey without weight
        :return: None
        """

        # Step1: add new sheet and define module sheet
        sht3_ResYear = self.resultExl.sheets.add(self.sht3NameResYear, after=self.sht2NameGrade)

        # Step2: Set title
        shtCopyTo(self.surveyTestSht, self.sht3ColRan, sht3_ResYear, self.sht3ColRan.split(":")[0])
        shtCopyTo(self.sht3Module, "L1:BA2", sht3_ResYear, "K1")
        # Step2.1 delete the row of left column redundantly

        # Step3: copy title
        # insert new column
        # sht3_ResYear.range("I1").api.EntireColumn.Insert()
        # TODO: insert Data

        #pass

    def addSheet4_surveyGradeByYear(self, departmentLst, scoreLst,
                                    columnScope="A1:B32", titleStart="C1", dataStart="C3"):
        """
        generate sheet4 of the surveyExl, which is the survey with weight
        :return: None
        """
        time.sleep(2)
        # Step1: add new sheet
        sht4_surveyGradeByYear = self.resultExl.sheets.add(self.sht4NameScoreYear, after=self.sht3NameResYear)
        sht2_lv2Score = self.resultExl.sheets[self.sht2NameGrade]

        # Step2: copy left column the surveySht to sht1, with style
        sht2_lv2Score.api.Range('A1:C15').Copy()
        sht4_surveyGradeByYear.api.Range('A1').PasteSpecial(Transpose=True)
        shtCopyTo(self.sht4Module, 'A4:B52', sht4_surveyGradeByYear, 'A4')

        # Step2.1 delete the row of left column redundantly
        # Step3: copy title
        # TODO: insert Data

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
        return staffWithLv  #, scoreWithLv

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

    def genSummaryFile(self):
        """
        generate the summary file of the surveyExl
        :return: None
        """
        # # Step1: get the department dict
        # self.__setAllDepartmentDict()

        # Step1: get ScoreData
        stuffWithLv, scoreWithLv = self.getStuffDict()  # TODO: 也许不需要scoreWithLv
        # for stu in stuffLst:
        #     print(stu)
        # print(self.scoreExlTitle)
        stuffWithLv = self.getStuffAllScore(stuffWithLv)
        # scoreWithLv[lv2][lv3] - > [[], [], ...]
        # stuffWithLv[lv2][lv3] - > [stu1, stu2, ...]  -> [stu.scoreLst for stu in stuffWithLv[lv2][lv3]]
        # Step2: generate the summary file
        self.addSheet1_surveyResult(stuffWithLv)
        self.addSheet2_surveyGrade(stuffWithLv, [])
        self.addSheet3_surveyResultByYear(stuffWithLv)
        self.addSheet4_surveyGradeByYear(stuffWithLv)

        # save
        self.surveyExl.save("surveyResult.xlsx")

    def genDepartmentFile(self):
        # TODO: 日后再写
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

    def demo(self):
        orgSht = self.surveyExl.sheets[self.orgShtName]
        orgDict = readOrgDict(orgSht)

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

        # Data Process
        scoreWithLv = getScoreWithLv(staffWithLv)
        sht1WithLv = getSht1WithLv(scoreWithLv)  # TODO:2022-9-5 数据填充方式改变
        lv2Unit = getSht2Lv2UnitScope(self.surveyTestSht)
        sht2WithLv = getSht2WithLv(sht1WithLv, lv2Unit)  # TODO: 找到所有lv3部门，求平均
        sht3WithLv = getSht3WithLv(sht1WithLv)
        sht4WithLv = getSht4WithLv(sht1WithLv)

        # Excel Process
        self.addSheet1_surveyResult(sht1WithLv)
        self.addSheet2_surveyGrade(sht2WithLv, orgDict)
        self.addSheet3_surveyResultByYear(sht3WithLv, orgDict)
        self.addSheet4_surveyGradeByYear(sht4WithLv, orgDict)

    def mockDataDemo(self):
        import mockData
        orgDict = {}
        # Excel Process
        self.addSheet1_surveyResult(mockData.sht1WithLv)
        self.addSheet2_surveyGrade(mockData.sht2WithLv, orgDict)
        self.addSheet3_surveyResultByYear(mockData.sht3WithLv, orgDict)
        self.addSheet4_surveyGradeByYear(mockData.sht4WithLv, orgDict)

    def run(self):
        """
        run the whole process, the main function.
        :return:
        """
        print("All done")
