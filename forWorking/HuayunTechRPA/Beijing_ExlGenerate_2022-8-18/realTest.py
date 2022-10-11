# Github: GWillS163
# User: 駿清清 
# Date: 29/09/2022 
# Time: 14:01

# import sys
# sys.path.append(r"D:\Project\python_scripts\forWorking\HuayunTechRPA\Beijing_ExlGenerate_2022-8-18")
from core.main import Excel_Operation

# surveyExlPh = r"D:\work\考核RPA_Exl\Input\2022-9-27\【测试问卷】模板更改2022-9-14_权重.xlsx"
surveyExlPh = r"D:\work\考核RPA_Exl\Input\2022-9-27\【测试问卷】模板更改2022-10-9_权重.xlsx"
partyAnsExlPh = r"D:\work\考核RPA_Exl\Input\2022-9-27\220926党建工作成效调研测试问卷--党员.xlsx"
peopleAnsExlPh = r"D:\work\考核RPA_Exl\Input\2022-9-27\220926党建工作成效调研测试问卷--群众.xlsx"
moduleExlPh = r"D:\Project\python_scripts\forWorking\HuayunTechRPA\Exl_Opr_2022-8-18\origin\【RPA模板表(" \
              r"测试)】中国移动北京公司2021年度党建工作成效调研.xlsx "
savePath = r"D:\Project\python_scripts\forWorking\HuayunTechRPA\Beijing_ExlGenerate_2022-8-18\save"
fileYear = ""
fileName = "PartyBuild"
surveyTestShtName = "测试问卷"
sht1ModuleName = "调研结果_输出模板"
sht2ModuleName = "调研成绩_输出模板"
sht3ModuleName = "调研结果（2022年）_输出模板"
sht4ModuleName = "调研成绩（2022年）_输出模板"
sht1Name = "调研结果"
sht2Name = "调研成绩"
sht3Name = "调研结果（2022年）"
sht4Name = "调研成绩（2022年）"

sht1WithLv = {'平台生态部': {'党建与综合管理室': [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, -1.0, 10.0, 10.0, 0.0, 10.0, 10.0, 10.0, 10.0, 10.0, 0.0, 10.0, 10.0, 10.0, 10.0, 10.0], '二级单位': [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, -1.0, 10.0, 10.0, 0.0, 10.0, 10.0, 10.0, 10.0, 10.0, 0.0, 10.0, 10.0, 10.0, 10.0]}, '重要客户中心': {'党建与综合管理室': [8.0, 9.0, 9.0, 9.0, 9.0, 10.0, 8.0, 8.0, 10.0, 10.0, 10.0, 9.0, 10.0, 10.0, -1.0, 10.0, 10.0, 0.0, 10.0, 9.0, 10.0, 9.0, 9.0, 0.0, 10.0, 9.0, 10.0, 9.0, 9.0], '二级单位': [8.0, 9.0, 9.0, 9.0, 9.0, 10.0, 8.0, 8.0, 10.0, 10.0, 10.0, 9.0, 10.0, 10.0, -1.0, 10.0, 10.0, 0.0, 10.0, 9.0, 10.0, 9.0, 9.0, 0.0, 10.0, 9.0, 10.0, 9.0]}, '网络与信息安全中心': {'信安室': [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, -1.0, 10.0, 6.0, 0.0, 10.0, 10.0, 10.0, 10.0, 10.0, 0.0, 10.0, 10.0, 10.0, 10.0, 10.0], '二级单位': [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, -1.0, 10.0, 6.0, 0.0, 10.0, 10.0, 10.0, 10.0, 10.0, 0.0, 10.0, 10.0, 10.0, 10.0]}, '北京融昱信息技术有限公司': {'党建与综合管理室': [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, -1.0, 10.0, 10.0, 0.0, 10.0, 10.0, 10.0, 10.0, 10.0, 0.0, 10.0, 10.0, 9.0, 10.0, 10.0], '二级单位': [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, -1.0, 10.0, 10.0, 0.0, 10.0, 10.0, 10.0, 10.0, 10.0, 0.0, 10.0, 10.0, 9.0, 10.0]}, '信息系统部': {'党建与综合管理室': [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, -1.0, 10.0, 10.0, 0.0, 10.0, 10.0, 10.0, 10.0, 10.0, 0.0, 10.0, 10.0, 9.0, 10.0, 10.0], '二级单位': [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, -1.0, 10.0, 10.0, 0.0, 10.0, 10.0, 10.0, 10.0, 10.0, 0.0, 10.0, 10.0, 9.0, 10.0]}, '行政服务中心': {'党建与综合管理室': [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, -1.0, 10.0, 6.0, 0.0, 10.0, 10.0, 10.0, 10.0, 10.0, 0.0, 10.0, 10.0, 9.0, 10.0, 10.0], '二级单位': [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, -1.0, 10.0, 6.0, 0.0, 10.0, 10.0, 10.0, 10.0, 10.0, 0.0, 10.0, 10.0, 9.0, 10.0]}}

if __name__ == '__main__':
    test = Excel_Operation(
        surveyExlPh, partyAnsExlPh, peopleAnsExlPh,
        savePath, fileYear, fileName,
        surveyTestShtName, sht1ModuleName, sht2ModuleName, sht3ModuleName, sht4ModuleName,
        sht1Name, sht2Name, sht3Name, sht4Name
    )

    # 1. Get readData
    # sht1WithLv = test.getData()
    # test.run(sht1WithLv)
    test.run(partyAnsExlPh, peopleAnsExlPh)
    # shtList = test.placeBar()
    # test.fillAllData(sht1WithLv, shtList)
    # test.genDepartFile()
    # TODO: 平均分是 非零求平均, 二级单位是所有人单独求平均
    # TODO: 二级单位 都不为空
    # TODO：党群纪检部 sht1
