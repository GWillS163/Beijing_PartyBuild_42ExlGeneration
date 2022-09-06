
import sys
sys.path.append(r"D:\Project\python_scripts\forWorking\HuayunTechRPA\Exl_Opr_2022-8-18")
from main_xlwings import Excel_Operation

from shtOperation import *
import time
from shtDataCalc import *

# if result.xlsx is exist, resultExlPh named as result + time.xlsx
resultExlPh = "result" + time.strftime("%Y%m%d%H%M%S", time.localtime()) + ".xlsx"

surveyExlPh = "D:\work\考核RPA_Exl\Input\模板1：【测试问卷】标准模板示例（原文件修改）_2022-8-30.xlsx"
scoreExlPh = "D:\work\考核RPA_Exl\Input\模板2：党办调研问卷测试-8.15答题结果_（模板）_2022-8-30.xlsx"
moduleExlPh = r"D:\Project\python_scripts\forWorking\HuayunTechRPA\Exl_Opr_2022-8-18\origin\【RPA模板表(测试)】中国移动北京公司2021年度党建工作成效调研.xlsx"

# resultExlPh = ".\\result.xlsx"
test = Excel_Operation(surveyExlPh, scoreExlPh, moduleExlPh, resultExlPh)

test.mockDataDemo()
