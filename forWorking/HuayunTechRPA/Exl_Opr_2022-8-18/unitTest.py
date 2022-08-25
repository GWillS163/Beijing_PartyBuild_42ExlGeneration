#  Author : Github: @GWillS163
#  Time: $(Date)

from main_xlwings import *


class TestExcel_Opr(Excel_Operation):


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

# test = TestExcel_Opr(surveyExlPh, scoreExlPh, resultExlPh)
# stuffLst = test.getStuffLst()
# test.getScore(stuffLst)

def scoreTest():
    selection1 = """
    1. 及时编发党员学习材料，组织党员学习
    2. 对基层党员、群众积极引导和帮助
    3. 工作大体可以按时按计划推进，但标准化、规范化水平有待提高
    4. 组织相关主题实践活动的创新性稍显不足
    5. 带头学习，勤勉敬业
    6. 在“抓实党业深度融合，以党建促进高质量发展方面”有待提高
    """
    selection2 = "5. 带头学习，勤勉敬业"
    rule1 = """
    10分：1-6任选5个及以上
    8分：1-6任选3-4个
    6分：1-6任选2个
    4分：1-6任选1个"""

    rule2 = """
    10分：1-4全选
8分：1-4任选3个
6分：1-4任选2个
4分：1-4任选1个
0分：5"""
    print(judgeAnswerGrade(selection1, rule1, "不定项选择题"))
    print(judgeAnswerGrade(selection2, rule1, "不定项选择题"))
    print(judgeAnswerGrade(selection2, rule2, "不定项选择题"))


scoreTest()


# judge a string is digit or letter only or not.
def isDigitOrLetter(string):
    for char in string:
        if not (char.isdigit() or char.isalpha()):
            return False
    return True
