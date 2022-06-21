# 百度tesseract-ocr使用
from aip import AipOcr
import time
'''------------------------------------------------------''' #喂picname，吐  OCR——> text，发送context至API

""" API """
APP_ID = '19665830'  # 你的appid
API_KEY = '	Xte1anTrWDjuM5xS2P5tvOdT'  # 你的apikey
SECRET_KEY = 'pafwKHBkfn2xIrCIye5UK7b94eRh2AEK'  # 你的secretkey

# 初始化AipFace对象
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

""" 读取图片 """

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def img_to_str(image_path):
    """ 可选参数 """
    options = {}
    options["language_type"] = "CHN_ENG"  # 中英文混合
    options["detect_direction"] = "true"  # 检测朝向
    options["detect_language"] = "true"  # 是否检测语言
    options["probability"] = "false"  # 是否返回识别结果中每一行的置信度

    #image = get_file_content(image_path)

    """ 带参数调用通用文字识别 """
    result = client.basicGeneral(get_file_content(image_path), options)

    # 格式化输出-提取需要的部分
    if 'words_result' in result:
        text = ('\n'.join([w['words'] for w in result['words_result']]))
    #print(type(result), "和", type(text))
    #print(text)
        return text

def run_ocr(path,picname):
    print('正在调用OCR识别',end='')
    t = time.time()
    filePath = path + str(picname)
    text = img_to_str(filePath)
    print('\t\t\t耗时' + str(round(time.time() - t,3))+ ' s')
    print('< < <■■■■■■■■■■■■■■■■■■■■■■■■■■> > >')
    print(text)
    print('< < <■■■■■■■■■■■■■■■■■■■■■■■■■■> > >')
    return text
    #print("OCR_DONe")
if __name__ == '__main__':
    run_ocr('./','2.png')

