#  Author : Github: @GWillS163
#  Time: $(Date)


# import a module that can read docx & doc file
import docx2txt
# why

keywords = ["中共中央", "十九届"]
# read docx file content
text = docx2txt.process("D:\work\北京 - 批量文件关键词检查\附录3 北京--运维投诉处理方案设计文档--案例.docx")
print(text)
