#  Author : Github: @GWillS163
#  Time: $(Date)
import threading

from ruleXlsCheck import *



def loading():
    # print loading anime
    for i in ["|", "/", "-", "\\"]:
        print("\rloading... " + i, end="")
        time.sleep(0.2)


class anime:
    def __init__(self):
        # create new thread for loading
        self.t = threading.Thread(target=loading, args=(self,))

    def start(self):
        # start thread
        self.t.start()

    def stop(self):
        # stop thread
        self.t.join()


if __name__ == '__main__':
    bannedFilePath = r"D:\work\北京9.8 - 批量文件关键词检查\制度核查\公司级制度汇编-已废止.xls"
    bannedColName = "E"
    permitUsingFilePath = r"D:\work\北京9.8 - 批量文件关键词检查\制度核查\公司级制度汇编-使用中.xls"
    permitColName = "C"

    compUsingFilePath = r"D:\work\北京9.8 - 批量文件关键词检查\制度核查\公司级-控措施清单-20220909.xls"
    compColName = "D"
    sectUsingFilePath = r"D:\work\北京9.8 - 批量文件关键词检查\制度核查\部门级-防控措施清单-20220909.xlsx"
    sectColName = "C"

    savePath = "D:\\work\\北京9.8 - 批量文件关键词检查\\制度核查\\"
    # create a folder as current time stamp, in savePath

    stt = time.time()
    savePath = createFolder(savePath)

    method1, method2, method3, method4 = main(savePath, bannedFilePath, bannedColName,
                                              permitUsingFilePath, permitColName,
                                              compUsingFilePath, compColName, sectUsingFilePath, sectColName)
    end = time.time() - stt
    # print(method1, method2, method3, method4)
    print("Done!", round(end, 3), "s")
