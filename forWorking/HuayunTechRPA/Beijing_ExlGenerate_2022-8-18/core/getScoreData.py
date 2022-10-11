# Github: GWillS163
# User: 駿清清 
# Date: 06/10/2022 
# Time: 20:57
from .utils import Stuff, saveDebugLogIfTrue
from .shtDataCalc import getScoreWithLv, getSht1WithLv
from .shtOperation import getRuleByQuestion
from .scoreJudgeCore import *
import xlwings as xw


def combineMain(questLst, peopleQuestLst, sht1People, partyQuestLst, sht1Party):
    """
    依照统计表的答案顺序，将问卷的答案按照顺序排列，没有则为0.
    :param questLst: 统计结果表的答案顺序
    :param peopleQuestLst: 问题顺序
    :param sht1People: sht1PeopleData
    :param partyQuestLst:  问题顺序
    :param sht1Party:sht1PartyData
    :return: sht1WithLv
    """
    # 得到答案的顺序 - get order of answer
    partyOrderLst = []
    peopleOrderLst = []
    for quest in questLst:
        if quest is None:
            continue
        partyIndex = getMappingIndex(quest, partyQuestLst)
        peopleIndex = getMappingIndex(quest, peopleQuestLst)
        peopleOrderLst.append(partyIndex)
        partyOrderLst.append(peopleIndex)
    sortDebug(questLst, peopleOrderLst, partyOrderLst, partyQuestLst, peopleQuestLst, debug=True)

    # 依照统计表的答案顺序，将sht1WithLv整形
    sht1WithLvPeople = reformatSht1WithLv(sht1People, peopleOrderLst)
    sht1WithLvParty = reformatSht1WithLv(sht1Party, partyOrderLst)
    sht1WithLvCombine = lastCombination(sht1WithLvPeople, sht1WithLvParty)
    return getSht1WithLv(sht1WithLvCombine)


def reformatSht1WithLv(sht1WithLv, orderLst):
    """
    每个人都按照orderLst的顺序进行排序
    :param sht1WithLv:
    :param orderLst:
    :return:
    """
    for lv2 in sht1WithLv.keys():
        for lv3 in sht1WithLv[lv2].keys():
            lv3Scores = []
            for lv3StaffScore in sht1WithLv[lv2][lv3]:  # lv3 部门的所有人都按照orderLst的顺序进行摘选
                lv3Scores.append([lv3StaffScore[i] if i != -1 else 0 for i in orderLst])
            sht1WithLv[lv2][lv3] = lv3Scores
    return sht1WithLv


def lastCombination(sht1WithLvPeople, sht1WithLvParty):
    """
    将people 与 party 结合起来。
    :param sht1WithLvPeople:
    :param sht1WithLvParty:
    :return:
    """
    sumSht1WithLv = sht1WithLvPeople.copy()
    # combine party to people
    for lv2 in sht1WithLvParty.keys():  # 对于每一个党员的二级单位进行处理 - for each lv2 of party
        if lv2 not in sumSht1WithLv.keys():
            sumSht1WithLv.update({lv2: sht1WithLvParty[lv2]})
            continue
        # 如果有相同lv2 - if lv2 is same
        for lv3 in sht1WithLvParty[lv2].keys():  # 对于每一个党员的三级单位进行处理 - for each lv3 of party
            if lv3 not in sumSht1WithLv[lv2].keys():
                sumSht1WithLv[lv2].update({lv3: sht1WithLvParty[lv2][lv3]})
                continue
            # 如果有相同lv3 -  if lv3 is same
            sumSht1WithLv[lv2][lv3] = sumSht1WithLv[lv2][lv3] + sht1WithLvParty[lv2][lv3]
    return sumSht1WithLv


def getMappingIndex(question, questLst):
    index = -1
    # 方式1， 如果questLst中有全量的question，则返回对应的scoreLst中的值
    # index = questLst.index(question)
    # 方式2， 如果仅有部分question，则需要遍历，返回对应的scoreLst中的值
    for partyQuest in questLst:
        if partyQuest is None:
            continue
        if question in partyQuest:  # 若quest 一致
            index = questLst.index(partyQuest)
            break
    return index


def sortDebug(questLst, peopleOrderLst, partyOrderLst, partyQuestLst, peopleQuestLst, debug=True):
    """
    用于调试排序
    题目:19 11.【不定项选择题		19.【单选题】您所
    :param questLst:
    :param partyQuestLst:
    :param peopleQuestLst:
    :param debug:
    :param partyOrderLst:
    :param peopleOrderLst:
    :return:
    """
    if not debug:
        return
    notFoundSign = "—————未找到—————"
    print("\t\tparty \t people对应问题顺序:")
    n = 0
    for index1, index2 in zip(peopleOrderLst, partyOrderLst):
        if index1 == -1:
            peopleStr = notFoundSign
        else:
            peopleStr = partyQuestLst[index1]#[:10]
        if index2 == -1:
            partyStr = notFoundSign
        else:
            partyStr = peopleQuestLst[index2]#[:10]
        questAns = questLst[n] if "不计分" not in questLst[n] else questLst[n][:6] + "(不计分)"
        print(f"题目{n}:\t{questAns:<20}\t{peopleStr:<20}\t{partyStr:<20}")
        n += 1


class scoreJudgement:
    def __init__(self, testSurveySht, otherTitle):
        # 输入配置-分数表
        self.scoreExlTitle = None  # 存放scoreExl的标题
        # TODO: 使能自动获取
        self.surveyQuesCol = "E"  # 题目列
        self.surveyRuleCol = "J"  # 赋分规则列
        self.surveyQuesTypeCol = "G"  # 题目类型列
        self.otherTitle = otherTitle
        self.testSurveySht = testSurveySht
        self.app4Ans = xw.App(visible=True, add_book=False)  # 党员问卷表
        self.app4Ans.display_alerts = False
        self.app4Ans.api.CutCopyMode = False

    def getStaffData(self, ansExlPh, fileName, deBugPath, isDebug=True):
        """
        打开文件，获取答题后分数数据
        :param deBugPath:
        :param fileName:
        :param ansExlPh:
        :param isDebug:
        :return:
        """
        # 问卷表打开 - open the survey sheet
        ansExl = self.app4Ans.books.open(ansExlPh)
        staffWithLv, self.scoreExlTitle = step1StaffDict(ansExl.sheets[0], self.otherTitle)
        ansExl.close()
        # print("得到员工字典完毕")
        # print("开始分数计算")
        staffWithLv = self.step2FormatScoreWithLv(staffWithLv, deBugPath, fileName, isDebug)
        scoreWithLv = getScoreWithLv(staffWithLv)
        # sht1WithLv = getSht1WithLv(scoreWithLv)
        for lv2 in staffWithLv:
            for lv3 in staffWithLv[lv2]:
                for stu in staffWithLv[lv2][lv3]:
                    print(stu.name, stu.scoreLst)
        return self.scoreExlTitle.answerLst, scoreWithLv  # sht1WithLv

    def step2FormatScoreWithLv(self, staffWithLv, debugPath, fileName, debug=True):
        """
        给每个人打分 得到stuffScoreWithLv Dict:
        :param debugPath:
        :param staffWithLv:
        :param fileName:
        :param debug: whether save to debug csv
        :return:{lv2Depart: {lv3Depart: [stuff1, stuff2, ...]}}
        """
        debugScoreAllLst = []  # store [name, questTitle, answer, rule, score] for debug
        lv2Num = 0
        for lv2 in staffWithLv:
            lv2Num += 1
            lv3Num = 0
            for lv3 in staffWithLv[lv2]:
                lv3Num += 1
                print(f"Lv2:[{lv2Num}/{len(staffWithLv.keys())}] "
                      f"Lv3:[{lv3Num}/{len(staffWithLv[lv2].keys())}]", end="\r")
                stuffScoreList, debugScoreLst = self.calcEachStaff(staffWithLv[lv2][lv3])
                staffWithLv[lv2][lv3] = stuffScoreList
                debugScoreAllLst += debugScoreLst
        print("")
        # if debug on, save the debugScoreLst to csv with current time
        saveDebugLogIfTrue(debugScoreAllLst, fileName, debug, debugPath)
        return staffWithLv

    def calcEachStaff(self, lv3StaffScoreList):
        """
        通过所有员工列表获得员工的分数列表 {二级部门:{三级部门: [[分数, 分数], [分数, 分数]]}}
        from the staffWithLv, get the scoreLst, get the staff score list from the surveySht
        :param lv3StaffScoreList: {lv2Depart:{lv3Depart: [staff, staff]}}
        :return: {lv2Depart:{lv3Depart: [[score], [score]]}}
        """
        debugScoreLst = []
        # TODO: 优化方式v3：将所有题目和规则读取到内存中
        for staff in lv3StaffScoreList:  # each staff in the lv3Depart
            # every staff need to get the all score
            for questionNum in range(len(self.scoreExlTitle.answerLst)):
                if not staff.answerLst[questionNum]:
                    continue
                # 得到每个问题的Title - get every questTitle by questTitle num
                questTitle = self.scoreExlTitle.answerLst[questionNum]
                if "不计分" in questTitle:  # 如果是不计分的题目，跳过 - if the questTitle is not score, skip
                    staff.scoreLst[questionNum] = 0
                    break
                # 得到员工答案 - get staff staffAns
                staffAns = staff.answerLst[questionNum]
                if not staffAns:  # 员工没有答案则零分 - if staffAns is None, score is 0
                    staff.scoreLst[questionNum] = 0
                    break
                # 找到问题所属判分规则 - locate which row is rule by questTitle in scoreExl
                (answerRow, rule) = getRuleByQuestion(questTitle, self.testSurveySht,
                                                      self.surveyQuesCol, self.surveyRuleCol)
                if rule is None:  # 继续寻找问题规则 - continue to find rule of next question
                    continue
                quesType = self.testSurveySht.range(f"{self.surveyQuesTypeCol}{answerRow}").value
                staff.scoreLst[questionNum] = judgeAnswerGrade(staffAns, rule, quesType)
                bugPrintIf(staffAns, rule, questTitle, answerRow, quesType, staff, questionNum)
                debugScoreLst.append([staff.name, questTitle, quesType, staffAns, rule, staff.scoreLst[questionNum]])
        return lv3StaffScoreList, debugScoreLst

    def close(self):
        self.app4Ans.quit()


def isLineValid(i: list) -> bool:
    """
    判断是否是有效行
    :param i:
    :return:
    """
    # if i is all None, skip
    if not i:
        return False

    for j in i:  # 但凡有一个不是None，就不是空行 - if any one is not None, it is not empty
        if j:
            return True
    return False


def step1StaffDict(ansSht, otherTitle):
    """
    动态获取最大使用范围，从答案表得到数据
    get the stuff list from the surveySht
    :return: stuffLst
    """
    staffWithLv = {}
    # scoreWithLv = {}
    # use all range to the value
    lastRow = ansSht.used_range.last_cell.row
    lastCol = ansSht.used_range.last_cell.column
    content = ansSht.range((1, 1), (lastRow, lastCol)).value
    # content = ansSht.range(departmentScope).value
    scoreExlTitle = ""
    addedSort = 0
    for i in content:
        if not isLineValid(i):
            print("空行无效注意：", i)
            continue

        if i[0] == "序号":
            scoreExlTitle = Stuff(i[1], i[2], i[3], i[4], i[5], i[6], i[9:])
            continue
        stu = Stuff(i[1], i[2], i[3], i[4], i[5], i[6], i[9:])
        # print(stu)
        if stu.lv2Depart not in staffWithLv:
            staffWithLv[stu.lv2Depart] = {}
            # scoreWithLv[stu.lv2Depart] = {}
        if not stu.lv3Depart:
            stu.lv3Depart = otherTitle
        if stu.lv3Depart not in staffWithLv[stu.lv2Depart]:
            staffWithLv[stu.lv2Depart][stu.lv3Depart] = []
            # scoreWithLv[stu.lv2Depart][stu.lv3Depart] = []
        staffWithLv[stu.lv2Depart][stu.lv3Depart].append(stu)
        addedSort += 1
        # scoreWithLv[stu.lv2Depart][stu.lv3Depart].append(stu.scoreLst)
    flag = f"step1StaffDict: 原数据{lastRow}行，有效数据{addedSort}行" if lastRow - 1 != addedSort else "step1StaffDict: 有效数量 全部匹配"
    print(flag)
    return staffWithLv, scoreExlTitle  # , scoreWithLv


def bugPrintIf(answer, rule, questTitle, answerRow, quesType, stuff, questionNum):
    if stuff.scoreLst[questionNum] == -1:
        print(f"answer: {answer}\n"
              f"rule: {rule}\n"
              f"questTitle: {questTitle}\n"
              f"answerRow: {answerRow}\n"
              f"quesType: {quesType}\n"
              f"score: {stuff.scoreLst[questionNum]}")
