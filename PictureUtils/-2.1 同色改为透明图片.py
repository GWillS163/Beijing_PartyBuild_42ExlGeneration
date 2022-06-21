# mport PIL.Image as Image                      相关模块
#
# img=Image.open('round.png')                  使用Image打开图片，返回一个对象
#
# img=img.convert('RGBA')                        图片转换为四通道。第四个通道就是我们要修改的透明度。返回新的对象
#
# L,H=img.size                                            图片尺寸
#
# color_0 = img.getpixel((0,0))                    返回图片某个坐标点颜色。
# i
# img.putpixel((x,y),(0,0,0,0))                      修改此坐标点的颜色，没有返回值，直接修改img
#
# ------------------------------------------------操作方法------------------------------------------------
#
# 1.只需要按特定规则把图片像素的第四个通道改为0即可。也可以是0-255之间的其他值，设置半透明。
#
# 2.也可以把前三个通道改为其他颜色，随你喜欢。
#
# 3.规则请随意制定。能改成什么样，取决于自己的脑洞。
#
# 4.下面的代码把所有与(0,0)点坐标相同颜色的点改为透明。
#
# ------------------------------------------------代码实现------------------------------------------------

import PIL.Image as Image


# 以第一个像素为准，相同色改为透明
def transparent_back(img):
    img = img.convert('RGBA')
    L, H = img.size
    color_0 = img.getpixel((0,0))
    for h in range(H):
        for l in range(L):
            dot = (l,h)
            color_1 = img.getpixel(dot)
            if color_1 == color_0:
                color_1 = color_1[:-1] + (0,)
                img.putpixel(dot,color_1)
    return img

if __name__ == '__main__':
    img=Image.open('round.png')
    img=transparent_back(img)
    img.save('round2.png')