#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

from PIL import Image, ImageDraw, ImageFont

#
# def addimg(img):
#     mark_img = Image.new('RGBA', (120, 120), 'white')
#     img.paste(mark_img, (0, 0))
#     img.save(path)
#
#
# path = input("Please input the image file with path: ")
#
#
# try:
#     print("path: "+path)
#     oriImg = Image.open(path)
#     addimg(oriImg)
#     oriImg.show()
# except IOError:
#     print("can't open the file,check the path again")
#     newImg = Image.new('RGBA', (320, 240), 'blue')
#     newImg.save(path)

logo = Image.open('./images/logo.jpg')
logo.thumbnail((100, 100))
wechat = Image.open('./images/wechat.jpg')
wechat.thumbnail((100, 100))
background = Image.new('RGBA', (300, 600), 'white')
background.paste(logo, (100, 0))
background.paste(wechat, (100, 500))

font = ImageFont.truetype('./images/simsun.ttc', 36, encoding='utf-8')
# 创建Draw对象:
draw = ImageDraw.Draw(background)
draw.text((10, 110), '周冠军！', font=font, fill=(220, 20, 60))
# 选色 https://www.sioe.cn/yingyong/yanse-rgb-16/
background.save('./images/background.png')

