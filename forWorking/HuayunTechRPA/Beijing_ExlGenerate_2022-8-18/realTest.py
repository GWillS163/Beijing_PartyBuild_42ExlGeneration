# encoding: utf-8

# Github: GWillS163
# User: 駿清清 
# Date: 29/09/2022 
# Time: 14:01

# import sys
# sys.path.append(r"D:\Project\python_scripts\forWorking\HuayunTechRPA\Beijing_ExlGenerate_2022-8-18")
from core.config import *
from core.main import *

print("Start to run the process...")
outputDir, sumSavePathNoSuffix = getSavePath(savePath, fileYear, fileName)

exlMain = Excel_Operation(
    surveyExlPh, partyAnsExlPh, peopleAnsExlPh,
    surveyTestShtName, sht1ModuleName, sht2ModuleName, sht3ModuleName, sht4ModuleName,
    sht1Name, sht2Name, sht3Name, sht4Name,

    # Sheet1 生成配置 : F, G
    sht1TitleCopyFromSttCol, sht1TitleCopyToSttCol,
    # Sheet2 生成配置: C1:J1, D
    sht2DeleteCopiedColScp, sht2MdlTltStt,
    # Sheet3 生成配置:  "L", "J", "K"
    sht3MdlTltStt, sht0SurLastCol, sht3ResTltStt,
    # Sheet4 生成配置:
    sht4IndexFromMdl4Scp, sht4SumTitleFromMdlScp,  # , sht4DataRowRan
    isGenDepartments,  # 是否生成部门
    excludeSht0UnitLst,
    isOriginPlan # 是否是原始计划

)
# outputDir = exlMain.run(partyAnsExlPh, peopleAnsExlPh, outputDir, sumSavePathNoSuffix,
#                         mockSht1WithLv=sht1WithLv, basIcPrPt=basIcPrPt)
outputDir = exlMain.run(partyAnsExlPh, peopleAnsExlPh, outputDir, sumSavePathNoSuffix)
