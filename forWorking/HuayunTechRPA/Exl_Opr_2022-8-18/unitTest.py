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
    rule3 = """
10分：全选
8分：任选3个
6分：任选2个
4分：任选1个
"""

    selection_single = "1. 及时编发党员学习材料，组织党员学习"
    rule_single = """
1.1分
2.2分
3.3分
4.4分
5.5分
6.6分
7.7分
8.8分
9.9分
10.10分"""

    realAnswer2 = """
2.政治信仰更加坚定,3.理想信念更加笃定"""
    realRule2 = """
10分：1-4全选
8分：1-4任选3个
6分：1-4任选2个
4分：1-4任选1个
0分：5"""
    selection_single2 = "10. 带头学习，勤勉敬业"
    selection_single_error = "1.组织学习, 10. 带头学习，勤勉敬业"
    print(judgeAnswerGrade(selection1, rule1, "不定项选择题"), 10)
    print(judgeAnswerGrade(selection2, rule1, "不定项选择题"), 4)
    print(judgeAnswerGrade(selection2, rule2, "不定项选择题"), 0)
    print(judgeAnswerGrade(selection2, rule3, "不定项选择题"), 4)
    print(judgeAnswerGrade(selection_single, rule_single, "单项"), 1)
    print(judgeAnswerGrade(selection_single2, rule_single, "单项"), 10)
    print(judgeAnswerGrade(selection_single_error, rule_single, "单项"), "报错")
    print(judgeAnswerGrade(realAnswer2, realRule2, "不定项选择题"), 6)


def ScoreJudgeBugFixCase():
    ans1 = """
2. 对基层党员、群众积极引导和帮助,3. 工作大体可以按时按计划推进，但标准化、规范化水平有待提高,4. 组织相关主题实践活动的创新性稍显不足,6. 在“抓实党业深度融合，以党建促进高质量发展方面”有待提高"""
    rule1 = """10分：1-6任选5个及以上
8分：1-6任选3-4个
6分：1-6任选2个
4分：1-6任选1个"""
    print(judgeAnswerGrade(ans1, rule1, "不定项选择题"), 8)
    ans2 = """
    3.有提升，但不明显"""
    rule2 = """
10分：1
8分：2
6分：3
4分：4"""
    print(judgeAnswerGrade(ans2, rule2, "单选"), 6)
    ans3 = """3.每半年开展3次"""
    rule3 = """10分：5-6
8分：3-4
6分：2
4分：1
0分：7"""
    print(judgeAnswerGrade(ans3, rule3, "单选"), 8)
    ans4 = """5.基本不存在"""
    rule4 = """10分：5
8分：4
6分：3
4分：2
0分：1"""
    print(judgeAnswerGrade(ans4, rule4, "单选"), 10)
    ans5 = """'1.习近平总书记“七一”重要讲话精神学习,3.“共筑百年梦、融合创未来”庆祝建党100周年主题宣传,6.“两和升级”'
    """
    rule5 = """'10分：1-13任选10个及以上或选14
9分：1-13任选8-9个
8分：1-13任选6-7个
6分：1-13任选4-5个
4分：1-13任选2-3个
0分：0-1个或选15或选16'"""
    print(judgeAnswerGrade(ans5, rule5, "不定项选择题"), 4)


def main():
    # if result.xlsx is exist, resultExlPh named as result + time.xlsx
    resultExlPh = "result" + time.strftime("%Y%m%d%H%M%S", time.localtime()) + ".xlsx"

    surveyExlPh = "D:\work\考核RPA_Exl\Input\附件1：【测试问卷】中国移动北京公司2021年度党建工作成效调研—20220816.xlsx"
    scoreExlPh = "D:\work\考核RPA_Exl\Input\附件2：党办调研问卷测试-8.15答题结果_20220815.xlsx"

    test = TestExcel_Opr(surveyExlPh, scoreExlPh, resultExlPh)
    stuffLst = test.getStuffLst()
    for stu in stuffLst:
        print(stu)
    print(test.scoreExlTitle)
    stuffLst = test.getStuffAllScore(stuffLst)

    print("展示分数：")
    for stu in stuffLst:
        print(stu.name,
              # stu.answerLst,
              stu.scoreLst)


if __name__ == '__main__':
    scoreTest()
    ScoreJudgeBugFixCase()

    # main()
