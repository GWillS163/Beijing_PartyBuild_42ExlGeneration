# GitHub: @GWillS163
# Start Time: 2022-08-18
# End Time:

from .getScoreData import *
from .shtDataCalc import *
from .shtOperation import *
from .userParamsProcess import *

lv1Name = "北京公司"
lv2MeanStr = "二级单位"


class Excel_Operation:
    surveyRuleCol: str
    surveyQuesCol: str
    surveyQuesTypeCol: str

    def __init__(self, surveyExlPath, partyAnsExlPh, peopleAnsExlPh,
                 surveyTestShtName, sht1ModuleName, sht2ModuleName, sht3ModuleName, sht4ModuleName,
                 # ResultExl 配置
                 sht1Name, sht2Name, sht3Name, sht4Name,
                 # Sheet1 配置 : "F", "G"
                 sht1TitleCopyFromSttCol, sht1TitleCopyToSttCol,
                 # Sheet2 配置:  "C1:J1", "D"
                 sht2DeleteCopiedColScp, sht2MdlTltStt,
                 # Sheet3 配置:  "L", "J", "K"
                 sht3MdlTltStt, sht0SurLastCol, sht3ResTltStt,
                 # Sheet4 配置:
                 sht4IndexFromMdl4Scp, sht4SumTitleFromMdlScp,  # ,sht4DataRowRan
                 # 是否生成部门文件

                 isGenDepartments, excludeSht0UnitLst, isOriginPlan
                 ):
        """
        param surveyExlPath: the path of the survey excel
        :param scrExlPh:
        """
        # Saving File Settings
        self.surveyWgtCol = "K"
        self.orgShtName = '行政机构组织'
        self.otherTitle = "其他人员"
        self.lv2AvgTitle = "二级单位成绩"
        paramsCheckExist(surveyExlPath, partyAnsExlPh, peopleAnsExlPh)

        # self.surveyExlPath = surveyExlPath
        # self.scoreExlPath = scrExlPh
        self.app4Survey1 = xw.App(visible=True, add_book=False)
        self.app4Result3 = xw.App(visible=True, add_book=False)
        self.app4Survey1.display_alerts = False
        self.app4Result3.display_alerts = False
        self.app4Survey1.api.CutCopyMode = False
        self.app4Result3.api.CutCopyMode = False
        # open the survey file with xlwings
        self.surveyExl = self.app4Survey1.books.open(surveyExlPath)
        self.resultExl = self.app4Result3.books.add()

        # 输入配置-规则表 修改后请核对以下配置
        paramsCheckSurvey(self.surveyExl, [surveyTestShtName, sht2ModuleName, sht3ModuleName, sht4ModuleName])
        self.sht0TestSurvey = self.surveyExl.sheets[surveyTestShtName]  # "测试问卷"
        # module settings
        self.sht1Mdl = self.surveyExl.sheets[sht1ModuleName]  # "调研结果_输出模板"
        self.sht2Mdl = self.surveyExl.sheets[sht2ModuleName]  # "调研成绩_输出模板"
        self.sht3Mdl = self.surveyExl.sheets[sht3ModuleName]  # "调研结果（2022年）_输出模板"
        self.sht4Mdl = self.surveyExl.sheets[sht4ModuleName]  # "调研成绩（2022年）_输出模板"
        # basic output settings 
        self.sht1NameRes = sht1Name
        self.sht2NameGrade = sht2Name
        self.sht3NameResYear = sht3Name
        self.sht4NameScoreYear = sht4Name

        # 通用配置
        self.skipUnitWords = excludeSht0UnitLst  # 删除的单位
        self.deptCopyHeight = 40  # 从总表复制到 各个部门表时的高度

        # Sheet0 survey表 数据获取 - Module Sheet 0 TestSurvey
        # 调查规则表中的问题列 规则列 问题类型列
        self.sht0DeleteCopiedRowScp, sht0LastValidRow = getSht0DeleteCopiedRowScp(
            self.sht0TestSurvey, self.skipUnitWords)
        self.surveyQuesCol, self.surveyRuleCol, \
            self.surveyQuesTypeCol, self.sht0QuestionScp = \
            autoGetSht0Params(self.sht0TestSurvey, sht0LastValidRow)

        # Sheet1  每次更改模板表后之后请留意
        self.sht1MdlPartRatioRowScp = "A3:D5"  # 新增的参与率区域 参与率粘贴的位置，一般不需要修改
        self.sht1PartitionInsertPoint = "A3"  # 插入，无法自动获取
        self.sht1TitleCopyFromMdlScp, self.sht1DeptTltRan, \
            self.sht1DataColRan, self.sht1IndexScpFromSht0 = \
            autoGetSht1Params(self.sht1Mdl,
                              sht1TitleCopyFromSttCol,
                              sht1TitleCopyToSttCol, sht0LastValidRow)
        # Sheet2:
        # When add Sheet 2
        self.Sht2Lv1UnitColLtr = "A"
        self.Sht2Lv2UnitColLtr = "B"
        self.sht2ContentColLtr = "D"
        self.sht2WeightColLtr = "C"
        self.sht2SttRow = 3
        self.sht2EndRow = 40

        # IndexColumns 设定
        self.sht2WgtColLtr = "D"

        self.sht2MdlPartRatioRowScp = "A3:C5"  # Sheet2 参与率部分的范围
        self.sht2PartitionInsertPoint = "A3"  # Sheet2 插入参与率的位置 无法自动获取

        self.sht2TitleCopyTo = None  # 自动获取sheet2 title 起始点
        self.sht2DeleteCopiedColScp, self.sht2TitleCopyFromMdlScp, \
            self.sht2DeptTltRan, self.sht2IndexCopyFromSvyScp, self.sht2IndexCopyTo = \
            autoGetSht2Params(self.sht2Mdl, self.sht0TestSurvey,
                              sht2DeleteCopiedColScp,  # ="C1:J1"
                              sht2MdlTltStt)  # ="D"

        # Sheet3:
        self.sht3MdlPartRatioRowScp = "A3:E5"
        self.sht3PartitionInsertPoint = "A3"
        self.sht3TitleCopyTo = None  # 自动获取sheet3 title 起始点
        self.sht3IndexCopyFromSvyScp, self.sht3DataColRan, self.sht3TitleCopyFromMdlScp = \
            autoGetSht3Params(self.sht3Mdl, self.sht0TestSurvey, sht3MdlTltStt, sht0SurLastCol,
                              sht3ResTltStt, sht0LastValidRow)  # "L", "J", "K"

        # Sheet4:
        self.sht4TitleCopyTo = None  # 自动获取sheet4 title 起始点
        self.sht4TitleFromSht2Scp = None  # 'A1:C17'  # Sht2模板中的index侧栏，长度是固定的
        self.sht4IndexFromMdl4Scp, self.sht4SumTitleFromMdlScp = \
            autoGetSht4Params(self.sht4Mdl, sht4IndexFromMdl4Scp, sht4SumTitleFromMdlScp)

        # When generate department file
        self.lv2UnitScp = []  # 二级单位范围，由addSheet1函数生成
        self.isOriginPlan = isOriginPlan
        self.isGenDepartments = isGenDepartments
        self.sht1IndexScp4Depart = None  # 生成侧标题后 自动获取"A1:F32"  # 生成部门文件时，需要复制的范围
        self.sht2IndexScp4Depart = None  # 生成侧标题后 自动获取"A1:C20"  # 生成部门文件用，复制左侧栏
        self.sht1TitleCopyTo = None

        # 新增参与率统计 - 2022-11-11
        self.allPartsStaffNum = {}
        # self.allStaffNum = {
        #     '党委办公室（党群工作部、职能管理部党委）': {'党委工作室': 5, '党建工作室': 9, '职能管理部党委办公室': 2, '企业文化室': 4, '青年工作室': 1}}  # 保存所有人员的人数

    def addSheet1_surveyResult(self):
        """
        新增 Sheet1
        generate sheet1 of the surveyExl, which is the survey without weight
        :return:
        """
        # titleStart, r = self.sht1MdlTltScope.split(":")
        # dataStart = r + str(int(self.sht1MdlTltScope.split(":")[1][-1]) + 1)
        # Step1: add new sheet and define module sheet
        sht1_lv2Result = self.resultExl.sheets.add(self.sht1NameRes)

        # Step2.1: copy left column the surveySht to sht1 partially with style
        # UnitScpRowList = getUnitScpRowList(self.sht0TestSurvey, "A", "D", ["党建", "宣传文化"])

        print("Sheet1 侧栏问题列处理 - Index Columns Processing...")
        print("Step1: 从Sht0整体复制侧栏 - copy left column the surveySht to sht1, with style")
        shtCopyTo(self.sht0TestSurvey, self.sht1IndexScpFromSht0,
                  sht1_lv2Result, f"A1")
        print("Step2.1 删除多余行(党廉&纪检) - delete the row of left column redundant")
        sht1_lv2Result.range(self.sht0DeleteCopiedRowScp).api.EntireRow.Delete()

        # getSht12DeleteCopiedRowScp
        print("Sheet1 复制参与率部分 - Copying Participation Rate...")
        sht1OprAddPartRatio(self.sht1Mdl, self.sht1MdlPartRatioRowScp,
                            sht1_lv2Result, self.sht1PartitionInsertPoint)

        # 记录左侧栏的范围 为生成部门文件时使用 - Record the left column range for generating department files
        self.sht1IndexScp4Depart = sht1_lv2Result.used_range.address

        # Step2.2: copy title
        print("Sheet1 部门标题处理 - Title Rows Processing...")
        self.sht1TitleCopyTo = getLastColCell(sht1_lv2Result)
        shtCopyTo(self.sht1Mdl, self.sht1TitleCopyFromMdlScp,
                  sht1_lv2Result, self.sht1TitleCopyTo)  # sht1_tltScope = "F1:KZ2"
        return sht1_lv2Result

    def addSheet2_surveyGrade(self):
        """
        生成sheet2的成绩表无数据，仅有二级标题，新增二级求和与全部求和。
        generate sheet2 of the surveyExl, only with title and sum
        :return: None
        """
        # Step1: 新增Sheet2 - add new sheet and define module sheet
        sht2_lv2Score = self.resultExl.sheets.add(self.sht2NameGrade, after=self.sht1NameRes)

        print("Sheet2 表头和侧栏部分处理 - header and sidebar section")
        sht2_lv2Score.range("B1").column_width = 18.8
        print("Step2: 从Sht0整体复制侧栏 - copy left column the surveySht to sht1, with style")
        shtCopyTo(self.sht0TestSurvey, self.sht2IndexCopyFromSvyScp,
                  sht2_lv2Score, self.sht2IndexCopyTo)
        print("Step2.1 删除多余行(党廉&纪检) - delete the row of left column redundant")
        sht2_lv2Score.range(self.sht0DeleteCopiedRowScp).api.EntireRow.Delete()

        print("Step2.2: 删除左侧多余单元行 - delete the row of left column redundant")
        print("Step2.2.1: 为单元格重新计算权重 - recalculate the weight to the cell")

        smallIndexSpan = getShtUnitScp(sht2_lv2Score, self.sht2SttRow, self.sht2EndRow,
                                       self.Sht2Lv2UnitColLtr, self.sht2WgtColLtr)
        sht2UnitScpOffsite = getNewUnitWgts(sht2_lv2Score, self.sht2SttRow, self.sht2EndRow,
                                            self.Sht2Lv2UnitColLtr, self.sht2WgtColLtr)
        print("Step2.3 删除多余列 - delete the column C to I")
        sht2_lv2Score.range(self.sht2DeleteCopiedColScp).api.EntireColumn.Delete()

        # 给所有单元格边缘增加偏移 - add offset to all cells edge
        resetUnitSum(sht2_lv2Score, sht2UnitScpOffsite, self.sht2WeightColLtr)
        print("Step2.2.2: 重设权重单元值完成 - Reset unit value completed")
        print("Step2.2.3: 删除多余行 - delete the row of left column redundant")
        sht2DeleteRowLst = getSht2DeleteRowLst(sht2UnitScpOffsite)
        for _ in range(len(sht2DeleteRowLst)):
            row = sht2DeleteRowLst.pop()
            sht2_lv2Score.range(f"{self.Sht2Lv2UnitColLtr}{row}").api.EntireRow.Delete()

        # 用来每个单元合计的范围
        bigIndexSpan = getShtUnitScp(sht2_lv2Score, self.sht2SttRow, self.sht2EndRow,
                                     self.Sht2Lv1UnitColLtr, self.Sht2Lv2UnitColLtr,
                                     skipCol=self.Sht2Lv1UnitColLtr, skipWords=self.skipUnitWords
                                     )
        print("Step3: 增加合计行 -  add summary row")
        lv2UnitScpForSumRow = getShtUnitScp(sht2_lv2Score, self.sht2SttRow, self.sht2EndRow,
                                            self.Sht2Lv1UnitColLtr, self.Sht2Lv2UnitColLtr)
        sht2OprAddSummaryRows(sht2_lv2Score, lv2UnitScpForSumRow)

        print("Step4: 增加参与率统计 - add participation rate statistics")
        sht2OprAddPartRatio(self.sht2Mdl, self.sht2MdlPartRatioRowScp, sht2_lv2Score, self.sht2PartitionInsertPoint)
        # 记录左侧栏的范围 为生成部门文件时使用 及Sheet4使用 - Record the left column range for generating department files
        self.sht2IndexScp4Depart = sht2_lv2Score.used_range.address

        print("Step4: 整体复制title - copy title")
        # get last column of the sht2
        self.sht2TitleCopyTo = getLastColCell(sht2_lv2Score)
        shtCopyTo(self.sht2Mdl, self.sht2TitleCopyFromMdlScp, sht2_lv2Score, self.sht2TitleCopyTo)

        return sht2_lv2Score, smallIndexSpan, bigIndexSpan

    def addSheet3_surveyResultByYear(self):
        """
        generate sheet3 of the surveyExl, which is the survey without weight
        :return: None
        """

        # Step1: add new sheet and define module sheet
        sht3_ResYear = self.resultExl.sheets.add(self.sht3NameResYear, after=self.sht2NameGrade)

        # Step2: Set Index column
        shtCopyTo(self.sht0TestSurvey, self.sht3IndexCopyFromSvyScp, sht3_ResYear,
                  self.sht3IndexCopyFromSvyScp.split(":")[0])

        print("Step2.1 删除多余行(党廉&纪检) - delete the row of left column redundant")
        sht3_ResYear.range(self.sht0DeleteCopiedRowScp).api.EntireRow.Delete()

        print("\t 新增参与率统计")
        sht3OprAddPartRatio(self.sht3Mdl, self.sht3MdlPartRatioRowScp, sht3_ResYear, self.sht3PartitionInsertPoint)

        # Step3: copy title
        self.sht3TitleCopyTo = getLastColCell(sht3_ResYear)
        shtCopyTo(self.sht3Mdl, self.sht3TitleCopyFromMdlScp, sht3_ResYear, self.sht3TitleCopyTo)

        return sht3_ResYear

    def addSheet4_surveyGradeByYear(self):
        """
        generate sheet4 of the surveyExl, which is the survey with weight
        :return: None
        """
        print("Step1: 新增Sheet4 - add new sheet")
        sht4_surveyGradeByYear = self.resultExl.sheets.add(self.sht4NameScoreYear, after=self.sht3NameResYear)
        sht2_lv2Score = self.resultExl.sheets[self.sht2NameGrade]

        print("Step2: 粘贴问卷单元title - copy title of survey")
        # sht2_lv2Score.api.Range(self.sht4TitleFromSht2Scp).Copy()
        sht2_lv2Score.api.Range(self.sht2IndexScp4Depart).Copy()
        sht4_surveyGradeByYear.api.Range("A1").PasteSpecial(Transpose=True)

        print("Step3: 复制模板的左侧线条公司栏 - copy left column of the template")
        sht4LineCompanyCopyTo = getLastRowCell(sht4_surveyGradeByYear)
        shtCopyTo(self.sht4Mdl, self.sht4IndexFromMdl4Scp,
                  sht4_surveyGradeByYear, sht4LineCompanyCopyTo)

        print("Step4: 粘贴汇总title - summarize Title patch")
        self.sht4TitleCopyTo = getLastColCell(sht4_surveyGradeByYear)
        shtCopyTo(self.sht4Mdl, self.sht4SumTitleFromMdlScp,
                  sht4_surveyGradeByYear, self.sht4TitleCopyTo)
        # set column B width = 20
        sht4_surveyGradeByYear.range("B1").column_width = 28
        return sht4_surveyGradeByYear

    def genDepartFile(self, departCode, sumSavePathNoSuffix):
        """ 通过汇总表生成所有部门文件, 生成固定的标题侧栏，然后填充数据-保存-清空数据
        generate the department file of the surveyExl， generate the fixed title sidebar, then fill data-save-clear data
        :return: None
        """
        global sht2Dept, sht2Sum, deptUnitSht2
        # 从汇总表 获取 部门分类区间
        sht1Sum = self.resultExl.sheets[self.sht1NameRes]
        deptUnitSht1 = getDeptUnit(sht1Sum, self.sht1DeptTltRan, 0)
        if not self.isGenDepartments:
            print("选择未生成部门文件 - No department file generated")
            return

        if self.isOriginPlan:
            sht2Sum = self.resultExl.sheets[self.sht2NameGrade]
            deptUnitSht2 = getDeptUnit(sht2Sum, self.sht2DeptTltRan, 0)

        print("新建部门文件 - create new excel with xlwings")
        # try 5 times to create new excel
        for i in range(5):
            try:
                app4Depart = xw.App(visible=True, add_book=False)
                break
            except:
                print("新建部门文件失败，重试 - Failed to create new excel, retry")
                time.sleep(1)
                continue
        else:
            print("新建部门文件失败，退出 - Failed to create new excel, exit")
            return
        deptResultExl = app4Depart.books.add()
        app4Depart.display_alerts = False
        app4Depart.api.CutCopyMode = False
        sht1Dept = deptResultExl.sheets.add(self.sht1NameRes)
        # set Sheet 1 row 1:40 height = 14
        sht1Dept.range("1:40").row_height = 14

        if self.isOriginPlan:
            sht2Dept = deptResultExl.sheets.add(self.sht2NameGrade, after=sht1Dept)
            sht2Dept.range("1:40").row_height = 14
            # sht2Dept.activate()
            shtCopyTo(sht2Sum, self.sht2IndexScp4Depart, sht2Dept, "A1")
        # sht1Dept.activate()
        shtCopyTo(sht1Sum, self.sht1IndexScp4Depart, sht1Dept, "A1")

        try:
            deptResultExl.sheets["Sheet1"].delete()
        except Exception as e:
            pass
        print("从汇总表 复制 边栏")
        # 填充数据 - 保存 - 删除
        sht2BorderL, sht2BorderR = "G", "Z"
        departStt = time.time()
        n = 0
        for deptName in deptUnitSht1:
            n += 1
            # add department data
            sht1BorderL, sht1BorderR = addOneDptData(sht1Sum, deptUnitSht1[deptName], self.deptCopyHeight,
                                                     sht1Dept, self.sht1TitleCopyTo)
            if self.isOriginPlan and deptName in deptUnitSht2:
                sht2BorderL, sht2BorderR = addOneDptData(sht2Sum, deptUnitSht2[deptName], self.deptCopyHeight,
                                                         sht2Dept, self.sht2TitleCopyTo)

            # Save Excel 保存文件名需要 加上部门Code
            deptCode = ""
            try:
                deptCode = departCode[deptName][deptName]['departCode']
            except Exception as e:
                print("部门Code获取失败 - Failed to get departCode", e)
                pass
            # departFilePath = self.sumSavePath.replace(".xlsx", f"_{deptName}_{deptCode}.xlsx")
            departFilePath = sumSavePathNoSuffix + f"_{deptCode}.xlsx"
            print(f"\033[32m{n:2} - 正在保存:[{deptCode}] - [{int(time.time() - departStt)}s] {deptName} - \033[0m")
            deptResultExl.save(departFilePath)
            departStt = time.time()

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

            if self.isOriginPlan and deptName in deptUnitSht2:
                borderWidth = getColNum(sht2BorderR) - getColNum(sht2BorderL)
                borderStart = getColNum(self.sht2TitleCopyTo[0])
                borderEnd = getColLtr(borderStart + borderWidth)
                sht2Dept.activate()
                sht2Dept.range(f"{self.sht2TitleCopyTo}:{borderEnd}{self.deptCopyHeight}").api.Delete()

        print("部门文件全部生成完毕，即将关闭文件")
        deptResultExl.close()
        app4Depart.quit()

        self.resultExl.close()
        self.app4Result3.quit()

    def placeBarWithoutData(self) -> list:
        # Add Title & column
        # global sht2_lv2Score, sht4_surveyGradeByYear, smallIndexSpan, bigIndexSpan
        sht1_lv2Result = self.addSheet1_surveyResult()
        # set 1 to 40 row height
        sht1_lv2Result.range("1:40").api.RowHeight = 14
        print("sheet1 无数据页面生成完成\n")

        sht2_lv2Score, smallIndexSpan, bigIndexSpan = self.addSheet2_surveyGrade()
        sht2_lv2Score.range("1:40").api.RowHeight = 14
        print("sheet2 无数据页面生成完成\n")

        sht3_ResYear = self.addSheet3_surveyResultByYear()
        sht3_ResYear.range("1:40").api.RowHeight = 14
        print("sheet3 无数据页面生成完成\n")

        sht4_surveyGradeByYear = self.addSheet4_surveyGradeByYear()
        sht4_surveyGradeByYear.range("1:40").api.RowHeight = 14
        print("sheet4 无数据页面生成完成")

        if not self.isOriginPlan:
            # delete sheet 2 & sheet 4
            self.resultExl.sheets[self.sht2NameGrade].delete()
            self.resultExl.sheets[self.sht4NameScoreYear].delete()
            return [sht1_lv2Result, "", sht3_ResYear, "", "", ""]

        return [sht1_lv2Result, sht2_lv2Score, sht3_ResYear, sht4_surveyGradeByYear, smallIndexSpan, bigIndexSpan]

    def fillAllData(self, sht1WithLv, shtList: list, departCode: dict, sumSavePathNoSuffix: str, basIcPrpt=None):
        """
        使用sheet1的数据计算出来接下来的数据，然后填充到excel中, 获得汇总的1 个文件
        use sheet1 data to calculate the data of the next sheet, then fill it into the excel
        :param sumSavePathNoSuffix: 
        :param departCode: 
        :param shtList: sht1_lv2Result, sht2_lv2Score, sht3_ResYear, sht4_surveyGradeByYear 
        :param sht1WithLv: 
        :return: 
        """
        global sht2WithLv
        sht1_lv2Result, sht2_lv2Score, sht3_ResYear, sht4_surveyGradeByYear, smallIndexSpan, bigIndexSpan = shtList

        if basIcPrpt:
            print("使用已算出的参与率数据")
            # sht1WithLv = sht1WithLv
            basicParticipateRatio = basIcPrpt
        else:
            print("开始生成参与率")
            basicParticipateRatio = getBasicParticipates(self.allPartsStaffNum, departCode, lv2MeanStr, lv1Name)

            print("sheet1 填充数据 - Sheet1 fill data vertically")
            sht1_lv2Result.activate()
            # two Methods to set data
            # sht1PlcScoreByPD(self.sht1Module, sht1_lv2Result, staffWithLv, self.sht1MdlTltScope, dataStart)
            # printShtWithLv("sht1WithLv：", sht1WithLv)

        sht1WithLvPtRt = combineSht1Ratio(sht1WithLv, basicParticipateRatio)
        # printShtWithLv("sht1WithLvPtRt：", sht1WithLvPtRt)
        sht1SetData(sht1_lv2Result, sht1WithLvPtRt, getTltColRange(self.sht1DataColRan, 1))

        if self.isOriginPlan:
            print("sheet2 填充数据 - sheet2 fill data vertically")
            sht2_lv2Score.activate()
            sht2WithLv = getSht2WithLv(sht1_lv2Result, sht2_lv2Score, self.sht0TestSurvey, self.surveyWgtCol,
                                       sht1WithLv, smallIndexSpan, bigIndexSpan, departCode
                                       )
            sht2WithLvPtRt = combineSht2Ratio(sht2WithLv, basicParticipateRatio)
            # print("sht2WithLv：", sht2WithLvPtRt)
            sht2SetData(sht2_lv2Score, sht2WithLvPtRt, getTltColRange(self.sht2TitleCopyFromMdlScp, 1))

        print("sheet3 填充数据 - sheet3 fill data vertically")
        sht3_ResYear.activate()
        sht3WithLv = getSht3WithLv(sht1WithLv, lv1Name, lv2MeanStr)
        # print("sht3WithLv：", sht3WithLv)
        sht3WithLvPtRt = combineSht3Ratio(sht3WithLv, basicParticipateRatio, lv2MeanStr, lv1Name)
        # print("sht3WithLvPtRt：", sht3WithLvPtRt)
        sht3SetData(sht3_ResYear, sht3WithLvPtRt, self.sht3DataColRan, lv1Name)
        # sht3 set conditional formatting partially

        if self.isOriginPlan:
            print("sheet4 填充横向数据 - Sheet4 fill data horizontally")
            sht4_surveyGradeByYear.activate()
            sht4Hie = getSht4Hierarchy(sht4_surveyGradeByYear)
            sht4WithLv = getSht4WithLv(sht2WithLv, sht4Hie, lv1Name, lv2MeanStr)
            # print("sht4WithLv：", sht4WithLv)
            sht4Ratio = turnSht4Ratio(basicParticipateRatio, sht4Hie, lv1Name, lv2MeanStr)
            sht4WithLvPtRt = combineSht4Ratio(sht4WithLv, sht4Ratio, lv2MeanStr, lv1Name)
            # print("sht4WithLvPtRt：", sht4WithLvPtRt)
            # Get last row Num by used_range
            sht4LastRow = sht4_surveyGradeByYear.used_range.last_cell.row
            # sht4DataRowRan = range(4, sht4LastRow + 1)
            sht4SetData(sht4_surveyGradeByYear, sht4WithLvPtRt, 4, sht4LastRow + 1, lv1Name)

        print("删除无用的sheet - Delete useless sheet")
        self.resultExl.sheets["Sheet1"].delete()
        savePath = sumSavePathNoSuffix + "_200000000.xlsx"
        print(f"汇总表将保存在：{savePath}")
        self.resultExl.save(savePath)
        self.surveyExl.close()
        self.app4Survey1.quit()

    def getFirstSht1WithLvData(self, partyAnsExlPh, peopleAnsExlPh, savePath):
        """
        获取第一个sheet1的数据，用于计算其他sheet的数据， 使用后关闭答案
        :return:
        """
        print("开始获取第一个sheet1的数据")
        debugPath = os.path.join(savePath, "分数判断记录")
        judges = scoreJudgement(self.sht0TestSurvey, self.otherTitle, self.surveyQuesCol, self.surveyRuleCol,
                                self.surveyQuesTypeCol)
        questionLst = self.sht0TestSurvey.range(self.sht0QuestionScp).value  # 问题列表
        print("开始获取群众数据 - Start to get people data")
        surveyData = getSurveyData(self.sht0TestSurvey)
        peopleQuesLst, sht1PeopleData = judges.getStaffData(peopleAnsExlPh, "群众", debugPath, surveyData, True)
        # printSht1Data("群众", sht1PeopleData, peopleQuesLst)
        print("开始获取党员数据 - Start to get party data")
        partyQuesLst, sht1PartyData = judges.getStaffData(partyAnsExlPh, "党员", debugPath, surveyData, True)
        # printSht1Data("党员", sht1PartyData, partyQuesLst)
        # 计算所有部门人数
        self.allPartsStaffNum = countDepartStaffNum(sht1PeopleData, sht1PartyData)
        questionSortDebugPath = os.path.join(savePath, "题目对应记录")
        sht1WithLvCombine = combineMain(questionLst, peopleQuesLst, sht1PeopleData, partyQuesLst, sht1PartyData,
                                        questionSortDebugPath)
        judges.close()
        # printSht1WithLv(sht1WithLvCombine)
        return sht1WithLvCombine

    def run(self, partyAnsExlPh, peopleAnsExlPh, outputDir, sumSavePathNoSuffix,
            mockSht1WithLv=None, basIcPrPt=None):
        """
        主程序
        run the whole process, the main function.
        :return:
        """

        stt = time.time()
        departsInfo = getAllOrgInfo(self.surveyExl.sheets(self.orgShtName))
        print("一、获取答题数据，开始判分 - 0. get data of score sheet, start to calculate score")
        if mockSht1WithLv:
            # 如果已有sht1WithLv数据，直接使用
            sht1WithLvCombine = mockSht1WithLv
        else:
            sht1WithLvCombine = self.getFirstSht1WithLvData(partyAnsExlPh, peopleAnsExlPh, outputDir)
            print(f"\n\033[33m\nGetScore time: {int(time.time() - stt)}s \033[0m")

        print("\n二、填充边栏 - II. fill the sidebar")
        shtList = self.placeBarWithoutData()
        print(f"\n\033[33m\nPlaceBar time: {int(time.time() - stt)}s \033[0m")

        print("\n三、填充参与率&分数数据、生成汇总文件 - III. fill data, generate summary file")
        self.fillAllData(sht1WithLvCombine, shtList, departsInfo, sumSavePathNoSuffix, basIcPrPt)
        print(f"\n\033[33m\nFillData time: {int(time.time() - stt)}s \033[0m")

        print("\n五、生成各部门文件 - IV. generate each department file")
        self.genDepartFile(departsInfo, sumSavePathNoSuffix)

        print(f"\n\033[33m\nTotal time: {int(time.time() - stt)}s All Done! Saved to:\033[0m "
              f"\n\033[32m{outputDir}\033[0m")
        return outputDir
