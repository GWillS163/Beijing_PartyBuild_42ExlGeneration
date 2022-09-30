#  Author : Github: @GWillS163
#  Time: $(Date)

from runPrefix import *

if __name__ == '__main__':
    test = Excel_Operation(
        surveyExlPh, scoreExlPh,
        savePath, fileYear, fileName,
        surveyTestShtName, sht1ModuleName, sht2ModuleName, sht3ModuleName, sht4ModuleName,
        sht1Name, sht2Name, sht3Name, sht4Name
    )

    # 1. Get readData
    sht1WithLv = test.getData()

    # 2. fill data
    # 2.1 use Mock Data
    # from mockData import sht1WithLv
    # 2.2 use real data

    # test.mockDataRunDemo(sht1WithLv)

    # test.addSheet1_surveyResult()
    # test.addSheet2_surveyGrade()
    # test.addSheet3_surveyResultByYear()
    # test.addSheet4_surveyGradeByYear()
