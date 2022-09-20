#  Author : Github: @GWillS163
#  Time: $(Date)
from ruleXlsCheck import *


if __name__ == '__main__':
    bannedFilePath = r"D:\work\北京9.8 - 批量文件关键词检查\制度核查\公司级制度汇编-已废止.xls"
    bannedColName = "E"
    sectUsingFilePath1 = r"D:\work\北京9.8 - 批量文件关键词检查\制度核查\公司级制度汇编-使用中.xls"
    sect1ColName = "C"
    compUsingFilePath = r"D:\work\北京9.8 - 批量文件关键词检查\制度核查\公司级-控措施清单-20220909.xls"
    compColName = "D"
    sectUsingFilePath = r"D:\work\北京9.8 - 批量文件关键词检查\制度核查\部门级-防控措施清单-20220909.xlsx"
    sectColName = "C"
    savePath = "D:\\work\\北京9.8 - 批量文件关键词检查\\制度核查\\"
    main(savePath, bannedFilePath, bannedColName, sectUsingFilePath1, sect1ColName,
         compUsingFilePath, compColName, sectUsingFilePath, sectColName)
    print("Done!")
