from PIL import Image, ImageDraw, ImageFont
import os,time


# 用于文字边框展示，传入draw,坐标x,y，字体，边框颜色和填充颜色
def text_border(draw, x, y, font, shadowcolor, fillcolor):
    # thin border
    draw.text((x - 1, y), text, font=font, fill=shadowcolor)
    draw.text((x + 1, y), text, font=font, fill=shadowcolor)
    draw.text((x, y - 1), text, font=font, fill=shadowcolor)
    draw.text((x, y + 1), text, font=font, fill=shadowcolor)

    # thicker border
    draw.text((x - 1, y - 1), text, font=font, fill=shadowcolor)
    draw.text((x + 1, y - 1), text, font=font, fill=shadowcolor)
    draw.text((x - 1, y + 1), text, font=font, fill=shadowcolor)
    draw.text((x + 1, y + 1), text, font=font, fill=shadowcolor)

    # now draw the text over it
    draw.text((x, y), text, font=font, fill=fillcolor)

def run_text_border(pos,src):
    t1 = time.time()
    x, y = [10, 10]

    src = "images\\qyt_poster-blank.png"
    im = Image.open(src)

    pointsize = 300
    fillcolor = (255, 255, 255)
    shadowcolor = "yellow"

    text = "5.0"

    font = "images\Deng.ttf"
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(font, pointsize)

    # 调用函数
    t2 = time.time()
    text_border(draw, x, y, font, (43, 43, 53), fillcolor)
    print('text_border used time:', time.time()-t2)
    fname2 = ".\\qyt_test.png"
    im.show()
    im.save(fname2)
    print(time.time()-t1)
    # os.startfile(fname2)#这个展示这个图片