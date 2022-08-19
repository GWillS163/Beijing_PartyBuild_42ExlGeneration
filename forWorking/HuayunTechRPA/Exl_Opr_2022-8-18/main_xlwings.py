#  Author : Github: @GWillS163
#  Time: $(Date)
from pprint import pprint

import xlwings as xw
import pandas as pd



class Excel_Operation():
    def __init__(self, surveyExlPath, scoreExlPath):
        self.surveyExlPath = surveyExlPath
        self.scoreExlPath = scoreExlPath

        self.app4Attach1 = xw.App(visible=False, add_book=False)
        self.app4Attach2 = xw.App(visible=False, add_book=False)

        # open the survey file with xlwings
        self.surveyExl = self.app4Attach1.books.open(surveyExlPath)
        self.scoreExl = self.app4Attach2.books.open(scoreExlPath)

        self.departmentDict = {}

    def close_excel(self):
        self.surveyExl.close()
        self.scoreExl.close()
        self.app4Attach1.quit()
        self.app4Attach2.quit()

    def genSheet1_surveyWithoutWeight(self, departmentLst, newSheetName, surveySheetName='测试问卷', copy_scope="A1:J32", titleStart="K1"):
        """
        generate sheet1 of the surveyExl, which is the survey without weight
        :param newSheetName:
        :param surveySheetName:
        :param copy_scope:
        :param titleStart:
        :return:
        """
        # open the sheet named "测试问卷" of surveyPath
        surveySht = self.surveyExl.sheets[surveySheetName]
        newSht = self.surveyExl.sheets.add(newSheetName)

        # Step1: copy left column the surveySht to newSht
        newSht.range(copy_scope).value = \
            surveySht.range(copy_scope).value

        # Step2: place title
        newSht.range(titleStart).value = departmentLst
        # get merge info
        startRow = titleStart[1]
        endLetter = chr(ord(titleStart[0]) + len(departmentLst))
        # merge K1:L1 cells
        newSht.range(f"{titleStart}:{endLetter}{startRow}").merge()

        # save
        self.surveyExl.save("test.xlsx")

    def genSheet2_surveyWithWeight(self, departmentLst):
        """
        generate sheet2 of the surveyExl, which is the survey with weight
        :return:
        """
        pass

    # make the function private
    def __setAllDepartmentTitle(self, departmentScope="A1:F10"):
        """
        set the departments title from the surveyExl, can be inserted
        :param departmentScope:
        :no return: {"二级部门": ["三级部门"], ...}
        """
        self.departmentDict = {}
        content = self.app4Attach2.range(departmentScope).value
        for i in content:
            # print the 0th, 1st, 2nd,4th elements of i with format inline
            print(i[2], i[4])
            if i[2] not in self.departmentDict:
                self.departmentDict.update({i[2]: [i[4]]})
                continue
            if i[4] not in self.departmentDict[i[2]]:
                self.departmentDict[i[2]].append(i[4])

    @staticmethod
    def __convertDict2Lst(departmentDict, other="其他人员", avg="二级单位成绩"):
        """
        convert Dict 2 List
        :param department: dict
        :return: [["二级部门"],
                 ["三级部门1","三级部门2"]]
        """
        # Step2: convertDict2Lst
        result_lst = [[], []]
        for layer3 in departmentDict:
            for layer2 in departmentDict[layer3]:
                if result_lst[0].__len__() == 0:
                    result_lst[0].append(layer3)
                else:
                    result_lst[0].append("")
                result_lst[1].append(layer2)
            result_lst[0].append("")
            result_lst[1].append(other)
            result_lst[0].append("")
            result_lst[1].append(avg)
        return result_lst

    def genOneDepartFile(self, departmentLst):
        """
        generate one department file
        :param departmentLst:
        :return:
        """
        self.genSheet1_surveyWithoutWeight(departmentLst, surveySheetName="测试问卷", copy_scope="A1:J32", titleStart="K1")
        self.genSheet2_surveyWithWeight(departmentLst)

    def genMultiDepartFile(self, ):
        pass

    def genSingleDepartFile(self):
        for department in self.departmentDict:
            departmentLst = self.__convertDict2Lst(department)
            self.genOneDepartFile(departmentLst)

    def run(self):
        """
        run the whole process, the main function.
        :return:
        """
        # 1. get the all department title
        # 2. get level 2 index columns
        # 3. get level 3 index columns
        departmentLst = []
        self.__setAllDepartmentTitle()
        for key in self.departmentDict:
            if "二级部门" in key:
                continue
            print(key, self.departmentDict[key])
            departmentLst = self.__convertDict2Lst({key: self.departmentDict[key]})
            break
        self.genSheet1_surveyWithoutWeight(departmentLst, "调研分数（未加权）", "测试问卷", "A1:J32")

        self.close_excel()
        print("All done")


if __name__ == '__main__':
    surveyExlPh = r"D:\work\考核RPA_Exl\附件1：【测试问卷】中国移动北京公司2021年度党建工作成效调研—20220816.xlsx"
    scoreExlPh = r"D:\work\考核RPA_Exl\附件2：党办调研问卷测试-8.15答题结果_20220815.xlsx"

    Excel_Operation(surveyExlPh, scoreExlPh).run()
