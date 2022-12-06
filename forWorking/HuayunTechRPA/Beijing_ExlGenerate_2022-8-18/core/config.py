# Github: GWillS163
# User: 駿清清 
# Date: 17/10/2022 
# Time: 17:38

surveyExlPh1013 = r"..\Input\2022-9-27\党建表格输入配置表_2022-10-18.xlsx"
surveyExlPh1111 = r"\Input\2022-11-11\党建表格输入配置表_2022-11-10.xlsx"
surveyExlPh1116 = r"D:\Project\python_scripts\forWorking\HuayunTechRPA\Beijing_ExlGenerate_2022-8-18\Input\2022-11-16\党建表格输入配置表_2022-11-16_样式更改.xlsx"
peopleAnsExlPh0926 = r"..\Input\2022-9-27\220926党建工作成效调研测试问卷--群众.xlsx"
peopleAnsExlPh1103 = r"..\Input\2022-11-3\edited\221101党建工作成效调研测试问卷--群众.xlsx"
peopleAnsExlPh1116 = r"D:\Project\python_scripts\forWorking\HuayunTechRPA\Beijing_ExlGenerate_2022-8-18\Input\2022-11-16\2022年度党建工作成效调研问卷-群众.xlsx"
partyAnsExlPh0926 = r"..\Input\2022-9-27\220926党建工作成效调研测试问卷--党员.xlsx"
partyAnsExlPh1103 = r"..\Input\2022-11-3\edited\221101党建工作成效调研测试问卷--党员.xlsx"
partyAnsExlPh1116 = r"D:\Project\python_scripts\forWorking\HuayunTechRPA\Beijing_ExlGenerate_2022-8-18\Input\2022-11-16\2022年度党建工作成效调研问卷-党员.xlsx"
peopleAnsExlPh1128 = r"D:\work\考核RPA_Exl\Input\2022-11-28_正式\2022年度党建工作成效调研问卷-群众 .xlsx"
partyAnsExlPh1128 = r"D:\work\考核RPA_Exl\Input\2022-11-28_正式\2022年度党建工作成效调研问卷-党员 .xlsx"

# partyAnsExlPh = partyAnsExlPh0926
# peopleAnsExlPh = peopleAnsExlPh0926
# partyAnsExlPh = partyAnsExlPh1103
# peopleAnsExlPh = peopleAnsExlPh1103
# peopleAnsExlPh = peopleAnsExlPh1116
# partyAnsExlPh = partyAnsExlPh1116
peopleAnsExlPh = peopleAnsExlPh1128
partyAnsExlPh = partyAnsExlPh1128
# surveyExlPh = surveyExlPh1111
# surveyExlPh = surveyExlPh1111
surveyExlPh = surveyExlPh1116
isGenDepartments = False

savePath = r"D:\work\考核RPA_Exl\Output"
fileYear = ""
fileName = "PartyBuild"
# surveyTestShtName = "测试问卷"
surveyTestShtName = "2022年调研问卷"
# sht1ModuleName = "调研结果_输出模板"
sht1ModuleName = "二级单位调研结果"
# sht2ModuleName = "调研成绩_输出模板"
sht2ModuleName = "二级单位调研成绩"
# sht3ModuleName = "调研结果（2022年）_输出模板"
sht3ModuleName = "公司整体调研结果"
# sht4ModuleName = "调研成绩（2022年）_输出模板"
sht4ModuleName = "公司整体调研成绩"
# sht1Name = "调研结果"
sht1Name = "二级单位调研结果"
# sht2Name = "调研成绩"
sht2Name = "二级单位调研成绩"
# sht3Name = "调研结果（2022年）"
sht3Name = "公司整体调研结果"
# sht4Name = "调研成绩（2022年）"
sht4Name = "公司整体调研成绩"

# Sheet1 生成配置 : F, G
sht1IndexScpFromSht0 = "A1:F31"
sht1TitleCopyFromSttCol = "F"
sht1TitleCopyToSttCol = "G"
# Sheet2 生成配置: "C1:J1", "D"
sht2DeleteCopiedColScp = "C1:J1"
sht2MdlTltStt = "D"
# Sheet3 生成配置:  "L", "J", "K"
sht3MdlTltStt = "L"
sht0SurLastCol = "J"
sht3ResTltStt = "K"  # TODO: 应该可以自动获取

# Sheet4 生成配置:
sht4IndexFromMdl4Scp = 'A4:B52'
# sht4TitleFromSht2Scp = 'A1:C17'  # 自动获取， 自动识别
sht4SumTitleFromMdlScp = "T1:U3"

sht1WithLv = {'党委办公室（党群工作部、职能管理部党委）': {'党委工作室': [8.8, 9.4, 7.0, 8.4, 3.33, 9.6, 3.2, 9.4, 7.6, 9.6, 7.8, 8.67, 6.67, 9.0, 7.33, 6.0, 7.2, 6.67, 6.67, 7.33, 5.2, 7.6, 6.4, 9.6, 9.6, 0.0, 0.0, 7.2, 6.2], '党建工作室': [10.0, 10.0, 10.0, 10.0, 2.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 8.89, 8.89, 10.0, 10.0, 0.0, 0.0, 10.0, 10.0], '职能管理部党委办公室': [10.0, 10.0, 10.0, 10.0, 0.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 0.0, 0.0, 10.0, 10.0], '企业文化室': [7.25, 5.0, 8.25, 6.0, 5.0, 7.75, 4.0, 7.75, 8.0, 7.75, 9.5, 7.0, 6.0, 8.0, 8.0, 10.0, 9.5, 9.0, 4.0, 6.0, 7.5, 7.75, 7.0, 8.75, 7.0, 0.0, 0.0, 8.75, 9.25], '青年工作室': [10.0, 1.0, 10.0, 1.0, 0.0, 10.0, 2.0, 10.0, 1.0, 10.0, 0.0, 4.0, 4.0, 10.0, 4.0, 4.0, 6.0, 4.0, 4.0, 4.0, 10.0, 10.0, 10.0, 10.0, 10.0, 0.0, None, 4.0, 10.0], '二级单位': [9.19, 8.48, 8.95, 8.43, 2.5, 9.48, 6.86, 9.43, 8.62, 9.48, 8.9, 8.67, 8.0, 9.42, 8.5, 8.5, 9.05, 8.5, 7.67, 8.17, 8.38, 8.52, 8.1, 9.67, 9.33, 0.0, 0.0, 8.81, 8.95]}}
