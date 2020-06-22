from aip import AipImageCensor

# """ 你的 APPID AK SK """
# APP_ID = '17899842'
# API_KEY = 'VM5S1ouZgwmk7Icc8x2l75pK'
# SECRET_KEY = '9Cvxl1qB4zGuidQod9Sw6zadQHcnIQZz'

""" API """
APP_ID = '19891414'  # 你的appid
API_KEY = 'usNMOs7sdzwep3QOgY4xoFV2'  # 你的apikey
SECRET_KEY = 'gw5vs1lKOLRGE6MstE8X8zbmxsXVBWIg'  # 你的secretkey


client = AipImageCensor(APP_ID, API_KEY, SECRET_KEY)
""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

""" 调用色情识别接口 """
result = client.imageCensorUserDefined(get_file_content('sex3.jpg'))
""" 如果图片是url调用如下 """
#result = client.imageCensorUserDefined('https://imgsa.baidu.com/forum/w%3D580/sign=559cf2cad93f8794d3ff4826e21a0ead/f3bc0ddda3cc7cd94ac925ab3401213fb90e91eb.jpg')
print(result)

#官方测试: