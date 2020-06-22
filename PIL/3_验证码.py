#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

from PIL import Image, ImageDraw, ImageFont, ImageFilter

import random


# 随机字母:
def rndchar():
    return chr(random.randint(65, 90))


# 随机颜色1:
def rndcolor():
    return random.randint(64, 255), random.randint(64, 255), random.randint(64, 255)


# 随机颜色2:
def rndcolor2():
    return random.randint(32, 127), random.randint(32, 127), random.randint(32, 127)


# 240 x 60:
width = 60 * 4
height = 60
image = Image.new('RGB', (width, height), (255, 255, 255))
# 创建Font对象:
font = ImageFont.truetype('/usr/share/fonts/dejavu/DejaVuSans.ttf', 36)
# 创建Draw对象:
draw = ImageDraw.Draw(image)
# 填充每个像素:
for x in range(width):
    for y in range(height):
        draw.point((x, y), fill=rndcolor())
# 输出文字:
for t in range(4):
    draw.text((60 * t + 10, 10), rndchar(), font=font, fill=rndcolor2())
# 模糊:
image = image.filter(ImageFilter.BLUR)
image.save('./images/code.jpg', 'jpeg')
