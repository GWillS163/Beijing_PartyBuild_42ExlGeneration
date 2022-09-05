#  Author : Github: @GWillS163
#  Time: $(Date)
import csv
import os.path
import re
import time
import xlwings as xw

from lib import *
from shtOpr import *
from shtDataCalc import *
from scoreJudge import *


class Excel_Operation:
    def __init__(self, surveyExlPath, scrExlPh, moduleExlPh, resultExlPh):

        self.scoreExlTitle = None
        self.surveyExlPath = surveyExlPath
        self.scoreExlPath = scrExlPh
        self.testExlPh = resultExlPh
        self.moduleExlPh = moduleExlPh

        self.app4Survey1 = xw.App(visible=True, add_book=False)
        self.app4Score2 = xw.App(visible=True, add_book=False)
        self.app4Module3 = xw.App(visible=True, add_book=False)
        self.app4Survey1.display_alerts = False
        self.app4Score2.display_alerts = False
        self.app4Module3.display_alerts = False
        self.app4Survey1.api.CutCopyMode = False
        self.app4Score2.api.CutCopyMode = False
        self.app4Module3.api.CutCopyMode = False

        # open the survey file with xlwings
        self.surveyExl = self.app4Survey1.books.open(surveyExlPath)
        self.scoreExl = self.app4Score2.books.open(scrExlPh)
        self.moduleExl = self.app4Module3.books.open(moduleExlPh)

        # public variable
        self.surveyTestSht = self.surveyExl.sheets["测试问卷"]
        self.departmentDict = {}
        self.sht1ScoreDct = {}
        self.sht2ScoreDct = {}

        # settings
        # save & module settings
        self.summarizeFileName = "汇总文件"  # without extension ".xlsx"
        self.savePath = ".\\"
        self.sht1NameRes = "调研结果"  # "调研问卷(未加权)"
        self.sht2NameGrade = "调研成绩"  # "调研问卷(加权)"
        self.sht3NameResYear = "调研结果（2022年）"
        self.sht4NameScoreYear = "调研成绩（2022年）"
        self.orgShtName = '行政机构组织'

        # survey settings
        self.surveyResultName = "调研结果"
        self.sht1ColScope = "A1:F32"
        self.sht1MdlTltScope = "F1:KZ2"
        self.sht1TltStart = "G1"

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

    def addSheet1_surveyResult(self, staffWithLv):
        """
        generate sheet1 of the surveyExl, which is the survey without weight
        :param staffWithLv:
        :return:
        """

        titleStart = self.sht1MdlTltScope.split(":")[0]
        dataStart = titleStart[:1] + str(int(self.sht1MdlTltScope.split(":")[1][-1]) + 1)
        # Step1: add new sheet and define module sheet
        sht1_lv2Result = self.surveyExl.sheets.add(self.sht1NameRes)
        sht1_moduleSht = self.moduleExl.sheets[self.surveyResultName]

        # Step2.1: copy left column the surveySht to sht1 partially with style
        shtCopyTo(self.surveyTestSht, self.sht1ColScope,
                  sht1_lv2Result, self.sht1ColScope.split(":")[0])
        # Step2.2: copy title
        shtCopyTo(sht1_moduleSht, self.sht1MdlTltScope,
                  sht1_lv2Result, self.sht1TltStart)  # sht1_tltScope = "F1:KZ2"

        # TODO: Step4: place score below title
        # TODO: need titleScope
        titleMatrix = self.moduleExl.sheets['调研结果'].range(self.sht1MdlTltScope).value
        # titleMatrix = sht1_lv2Result.range(self.sht1ModuleTltScope).value
        titleDf = pd.DataFrame(titleMatrix)
        sht1Value = sht1_calculate(staffWithLv, titleDf)
        sht1ValueDf = pd.DataFrame(sht1Value).transpose()
        # place sht1ValueDf to sht1_lv2Result at dataStart
        sht1_lv2Result.range(dataStart).value = sht1ValueDf
        # delete range G3:G6 and fill by right value
        sht1_lv2Result.range("G3:G33").api.Delete()
        sht1_lv2Result.range("G3:KZ3").api.Delete()

    def addSheet2_surveyScore(self, sht2WithLv, orgDict,
                              columnScope="A1:B32", titleStart="C1", dataStart="C3"):
        """
        generate sheet2 of the surveyExl, which is the survey with weight
        :return: None
        """

        sht2_lv2Score = self.surveyExl.sheets.add(self.sht2NameGrade)
        sht1_module = self.moduleExl.sheets["调研成绩"]
        sht2SetTitleIndex(self.surveyTestSht, sht2_lv2Score, sht1_module,
                          columnScope="A1:J32", titleStart="D1")

        wgtLst = sht2_lv2Score.range("C3:C13").value
        # iterate sheet2 each lv3 department
        for col in range(3, 10):
            colLtr = getColLtr(col)
            lv3 = sht2_lv2Score.range(f"{colLtr}2").value
            if lv3 in sht2WithLv:
                # place score list vertically
                wgtAnswer = listMultipy(sht2WithLv[lv3], wgtLst)
                sht2_lv2Score.range(f"{colLtr}3").options(transpose=True).value = wgtAnswer

        # TODO: 放到程序后面？Step2.3 add summary row
        sht2OprAddSummaryRows(sht2_lv2Score, sht2WithLv)

    def addSheet3_surveyResultByYear(self, departmentLst, scoreLst,
                                     columnScope="A1:J32", titleStart="K1", dataStart="K3"):
        """
        generate sheet3 of the surveyExl, which is the survey without weight
        :return: None
        """
        # Step1: add new sheet
        sht3_ResYear = self.surveyExl.sheets.add(self.sht3NameResYear, after=self.sht2NameGrade)
        sht3_module = self.moduleExl.sheets[self.sht3NameResYear]

        # Step2: copy left column the surveySht to sht1, with style
        shtCopyTo(self.surveyTestSht, columnScope, sht3_ResYear, columnScope.split(":")[0])
        shtCopyTo(sht3_module, "L1:BA2", sht3_ResYear, "K1")
        # Step2.1 delete the row of left column redundantly

        # Step3: copy title
        # insert new column
        sht3_ResYear.range("I1").api.EntireColumn.Insert()
        # TODO: insert Data

    def addSheet4_surveyScoreByYear(self, departmentLst, scoreLst,
                                    columnScope="A1:B32", titleStart="C1", dataStart="C3"):
        """
        generate sheet4 of the surveyExl, which is the survey with weight
        :return: None
        """
        # Step1: add new sheet
        sht4_WithWeight = self.surveyExl.sheets.add(self.sht4NameScoreYear, after=self.sht3NameResYear)

        # Step2: copy left column the surveySht to sht1, with style
        self.surveyTestSht.range(columnScope).api.Copy()
        sht4_WithWeight.range(columnScope.split(":")[0]).api.Select()
        sht4_WithWeight.api.Paste()
        self.app4Score2.api.CutCopyMode = False
        # Step2.1 delete the row of left column redundantly

        # Step3: copy title
        # TODO: insert Data

    def getStuffDict(self, departmentScope="A1:AM10"):
        """
        get the stuff list from the surveySht
        :param departmentScope: A:AM 是 题目scope 1:10是人数
        :return: stuffLst
        """
        stuffWithLv = {}
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
            if stu.lv2Depart not in stuffWithLv:
                stuffWithLv[stu.lv2Depart] = {}
                scoreWithLv[stu.lv2Depart] = {}
            if not stu.lv3Depart:
                stu.lv3Depart = self.otherTitle
            if stu.lv3Depart not in stuffWithLv[stu.lv2Depart]:
                stuffWithLv[stu.lv2Depart][stu.lv3Depart] = []
                scoreWithLv[stu.lv2Depart][stu.lv3Depart] = []
            stuffWithLv[stu.lv2Depart][stu.lv3Depart].append(stu)
            scoreWithLv[stu.lv2Depart][stu.lv3Depart].append(stu.scoreLst)
        return stuffWithLv, scoreWithLv

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
        self.addSheet2_surveyScore(stuffWithLv)
        self.addSheet3_surveyResultByYear(stuffWithLv)
        self.addSheet4_surveyScoreByYear(stuffWithLv)

        # save
        self.surveyExl.save("surveyResult.xlsx")

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

    def demo(self):
        orgSht = self.surveyExl.sheets[self.orgShtName]
        orgDict = readOrgDict(orgSht)

        # TODO: get score 注意切换到正确的sheet
        staffWithLv, scoreWithLv = self.getStuffDict()
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
        sht1WithLv = getSht1WithLv(scoreWithLv)  # 2022-9-2 OK
        lv2Unit = getSht2Lv2UnitScope(self.surveyTestSht)
        sht2WithLv = getSht2WithLv(sht1WithLv, lv2Unit)  # TODO: 找到所有lv3部门，求平均

        # Excel Process
        self.addSheet1_surveyResult(staffWithLv)
        self.addSheet2_surveyScore(staffWithLv, orgDict)
        self.addSheet3_surveyResultByYear(staffWithLv)
        self.addSheet4_surveyScoreByYear(staffWithLv)


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
