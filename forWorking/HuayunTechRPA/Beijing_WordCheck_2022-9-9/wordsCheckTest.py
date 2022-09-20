#  Author : Github: @GWillS163
#  Time: $(Date)

from keywordsCheck import *

if __name__ == '__main__':
    filesPh = r"D:\work\北京9.8 - 批量文件关键词检查"
    filesRe = r".*\.docx"
    kws = "北京, 设计 设置," \
          "中共 中国共产党, " \
          "二十大 第二十次大会, " \
          "三中全会 第三次中央全面会议"
    prefixName = "workCheckResult"
    main(filesPh, filesRe, kws, prefixName)
