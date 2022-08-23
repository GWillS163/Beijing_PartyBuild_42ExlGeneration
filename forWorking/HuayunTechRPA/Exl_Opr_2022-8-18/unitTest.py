#  Author : Github: @GWillS163
#  Time: $(Date)

from main_xlwings import *

class TestExcel_Opr(Excel_Operation):
    def run(self):

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

# if result.xlsx is exist, resultExlPh named as result + time.xlsx
resultExlPh = "result" + time.strftime("%Y%m%d%H%M%S", time.localtime()) + ".xlsx"

surveyExlPh = "D:\work\考核RPA_Exl\Input\附件1：【测试问卷】中国移动北京公司2021年度党建工作成效调研—20220816.xlsx"
scoreExlPh = "D:\work\考核RPA_Exl\Input\附件2：党办调研问卷测试-8.15答题结果_20220815.xlsx"

test = Excel_Operation(surveyExlPh, scoreExlPh, resultExlPh)
test.run()
