from PIL import Image, ImageDraw, ImageFont, ImageFilter
import time
import qrcode
import matplotlib.pyplot as plt

# 输入二维码信息， 返回定制的 白色透明二维码  img对象
def make_qr_code(content, save_path=None):
    qr_code_maker = qrcode.QRCode(version=3,
                                  error_correction=qrcode.constants.ERROR_CORRECT_M,
                                  box_size=8,
                                  border=0,
                                  )
    qr_code_maker.add_data(data=content)
    qr_code_maker.make(fit=True)  # 自动调整大小
    img = qr_code_maker.make_image(fill_color="White", # "SlateGray",  # "teal",,#"navy",#"indigo" #"gray",#"White" # "cyan",
                                   back_color="transparent"  # "gray"
                                   ).convert('RGBA')

    return img.convert("RGBA")
    # img.save(save_path)


# 用于文字边框展示，传入draw,坐标x,y，字体，边框颜色和填充颜色
def text_border(draw, x, y, text, font, shadowcolor, fillcolor, tchik, border):
    # thin border
    draw.text((x - tchik, y), text, font=font, fill=shadowcolor)
    draw.text((x + tchik, y), text, font=font, fill=shadowcolor)
    draw.text((x, y - tchik), text, font=font, fill=shadowcolor)
    draw.text((x, y + tchik), text, font=font, fill=shadowcolor)

    # thicker border
    draw.text((x - border, y - border), text, font=font, fill=shadowcolor)
    draw.text((x + border, y - border), text, font=font, fill=shadowcolor)
    draw.text((x - border, y + border), text, font=font, fill=shadowcolor)
    draw.text((x + border, y + border), text, font=font, fill=shadowcolor)

    # now draw the text over it
    draw.text((x, y), text, font=font, fill=fillcolor)


# 负责贴二维码到poster上
def add_sticker2poster(sticker, box, poster):
    # 加载需要粘贴的二维码， 最好是带透明通道的！
    # box是 base_img的范围区域
    sticker = sticker.resize((box[2] - box[0], box[3] - box[1]))  # 将二维码resize
    # 将透明图覆盖上去，中间透明区域将显示出底图
    poster.paste(sticker, (box[0], box[1]), sticker)  # 第一个参数表示需要粘贴的图像，中间的是坐标，最后是一个是mask图片，用于指定透明区域。
    return poster


# 测量中英混合字符串字节长度
def txt_len(txt):
    return int((len(txt.encode('utf-8')) - len(txt)) / 2 + len(txt))


# 模糊滤镜 PIL官方提供的模糊有限，半径只有2。可以自己写一个
def blur(im1, box):  # 打开一个jpg图像文件，注意是当前路径:
    im1 = im1.crop(box)  # 裁剪出下方区域
    return im1.filter(ImageFilter.BLUR)  # 应用模糊滤镜:
    # im2.save('./images/blur.png', 'png')

def text_shadow(draw,x,y,text,font):
    draw.text((x+1, y+2), text, (128, 128, 128), font)
    draw.text((x, y), text, (255, 255, 255), font)


def fixed_text(draw):
        # 居中上方 文字
        s_score_font = ImageFont.truetype('images\Dengl.ttf', 34)
        # 使用自定义函数 制作带阴影文本
        class_weight, h = s_score_font.getsize('到课情况              次')
        text_shadow(draw, 360 - class_weight / 2, 217, '到课情况⁢ ⁢⁢ 次', s_score_font)
        text_shadow(draw, 360 - class_weight / 2, 267, '作业上交⁢ ⁢⁢ 次', s_score_font)
        text_shadow(draw, 360 - class_weight / 2, 317, '视频登录次数⁢  次', s_score_font)
        text_shadow(draw, 360 - class_weight / 2, 367, '24次视频每周⁢  次', s_score_font)

        # 居中区域，总成绩
        sum_score_font = ImageFont.truetype('images\Dengb.ttf', 36)
        sum_w, sum_h = sum_score_font.getsize('总成绩:')
        text_shadow(draw, 360 - sum_w/2, 435, '总成绩:', font=sum_score_font)

date = time.asctime().split()[1] + '-' + time.asctime().split()[2] + '-' + time.asctime().split()[4]
used_tm_lst = []
avg_tm_lst = []
tm_lst = []
n = 0
# 画图装饰器
def figure(f):
    def inner(*args, **kwargs):
        plt.figure(figsize=(8, 4))
        plt.title('make_poster_pic_used_time')
        global n
        # noinspection PyBroadException
        f(*args, **kwargs)
    return inner

# 修改海报数据
def edit_poster(subject, date, score,
                ID, name, Honor,
                AD_qrCode, AD_text_title, AD_text_subsc):
    try:
        t1 = time.time()
        img_poster = Image.new(mode="RGB", size=(720, 1192), color="DeepSkyBlue")
        draw = ImageDraw.Draw(img_poster)  # 创建Draw对象:

        # 画布上粘上你的图片
        # 其实也可以在底图作为画布进行编辑，而不用新建一个画布
        pic_img = Image.open('images\\road.jpeg')
        # pic_img = Image.open('images\\road.jpeg')
        pic_img = pic_img.resize((720, 1192), Image.ANTIALIAS)
        img_poster.paste(pic_img)

        # 模糊下方区域，并粘贴回来
        bounds = (0, 940, 720, 1192)
        # 裁剪出下方区域——高斯模糊↓
        pic_img_sub = pic_img.crop(bounds)
        pic_img_sub_blur = pic_img_sub.filter(ImageFilter.GaussianBlur(radius=15))
        img_poster.paste(pic_img_sub_blur, (0, 940))
        # #
        # 粘上 右上角 logo
        logo_img = Image.open('images\\qytanglogo_gray_white.png')
        logo_img = logo_img.resize((150, 140), Image.ANTIALIAS)
        img_poster.paste(logo_img, (555, 31), logo_img)
        # # 右上方 课程名称   日期
        title_font = ImageFont.truetype('images\Dengb.ttf', 30)
        # w, h = draw.textsize('中文字符', title_font)  # 不能直接测量中文字符长度。
        # w, h = draw.textsize('a' * txt_len(subject), title_font)  # 不能直接测量中文字符长度。
        w, h = draw.textsize(subject, title_font)  # 不能直接测量中文字符长度。
        print(subject, '>>>字符长度为:', w)
        w2, h2 = title_font.getsize(date)
        draw.text((540 - w, 47), subject, (240, 255, 240), font=title_font)
        draw.text((540 - w2, 96), date, (255, 255, 255), font=title_font)

        fixed_text(draw)

        # 居中上方: 标准分
        score_font = ImageFont.truetype('images\Dengb.ttf', 46)
        s_score_font = ImageFont.truetype('images\Dengl.ttf', 33)
        # 到课分
        w3, h3 = draw.textsize(str(score[0][0]), score_font)
        print('w3 _weigh',w3)
        text_border(draw, 412 - w3, 205, str(score[0][0]), font=score_font,fillcolor=(255, 255, 255),
                        shadowcolor=(0, 153, 255), tchik=1, border=1)
        w, h = draw.textsize(str(score[0][1]))
        draw.text((415, 217), '/' + str(score[0][1]), (255, 255, 255), font=s_score_font)
        # 作业分
        homework_w, h3 = draw.textsize(str(score[1][0]), score_font)
        text_border(draw, 412 - homework_w, 256, str(score[1][0]), font=score_font,fillcolor=(255, 255, 255),
                        shadowcolor=(0, 153, 255), tchik=1, border=1)
        draw.text((415, 267), '/' + str(score[1][1]), (255, 255, 255), font=s_score_font)
        # 视频分数
        video_w, h = score_font.getsize(str(score[2]))
        text_border(draw, 441 - video_w /2, 310, str(score[2]),  font=score_font, fillcolor=(255, 255, 255),
                        shadowcolor=(0, 153, 255), tchik=1, border=1)
        video_week_w, h = score_font.getsize(str(score[3]))
        text_border(draw, 441 - video_week_w/2, 357, str(score[3]), font=score_font,fillcolor=(255, 255, 255),
                        shadowcolor=(0, 153, 255), tchik=1, border=1)
        #

        # # 非常标准的居中，测量textsize之前 一定要在textsize里加上font
        score[4] = round(score[4], 1)
        if score[4] > 0:
            font = ImageFont.truetype('images\Dengb.ttf', 290)
            w_score, hei = draw.textsize(str(score[4]), font)
            print('w_score', w_score, 'font_getoffset', font.getoffset(str(score[4])[1]))
            # draw.text((360 - (w_score / 2), 480), str(score[4]), (255, 255, 255), font=font)
            text_border(draw, (360 - (w_score / 2)), 480, str(score[4]),
                        font, fillcolor=(255, 255, 255),
                        shadowcolor=(0, 153, 255), tchik=1, border=2)
        elif score[4] < 0:
            font = ImageFont.truetype('images\Dengb.ttf', 290)
            w_score, hei = draw.textsize(str(score[4]), font)
            # print('w_score', w_score, 'font_getoffset', font.getoffset(str(score[4])[1]))
            text_border(draw, (360 - (w_score / 2)), 480, str(score[4]),
                        font, fillcolor=(255, 255, 255),
                        shadowcolor=(255, 25, 0), tchik=1, border=2)
        # 右下角荣誉 文字
        honor_font = ImageFont.truetype('images\Dengl.ttf', 30)
        text_border(draw, 519, 1027, '冠军周     次', font=honor_font, shadowcolor=(255, 201, 14), fillcolor=False,
                    tchik=0.3, border=0.3)
        text_border(draw, 519, 1077, '亚军周     次', font=honor_font, shadowcolor=(205, 205, 205), fillcolor=False,
                    tchik=0.3, border=0.3)
        text_border(draw, 519, 1127, '季军周     次', font=honor_font, shadowcolor=(185, 122, 87), fillcolor=False,
                    tchik=0.3, border=0.3)
        # # 右下角区域， ID_姓名， 荣誉
        name_font = ImageFont.truetype('images\Dengb.ttf', 36)
        # 测量宽度 （注意，这里直接放入 英文字符串即可）
        id_w, hei = draw.textsize(ID, name_font)
        # (546 - id_w) 是向右对齐
        draw.text((546 - id_w, 956), ID, (255, 255, 255), font=name_font)
        name_w, hei = draw.textsize(name, name_font)
        draw.text((686 - name_w, 956), name, (255, 255, 255), font=name_font)

        hnr_one, h = honor_font.getsize(str(Honor[0]))
        text_border(draw, 630 - hnr_one / 2, 1024, str(Honor[0]), font=honor_font, shadowcolor=(255, 201, 14), fillcolor="White",
                    tchik=0.3, border=0.3)
        hnr_two, h = honor_font.getsize(str(Honor[1]))
        text_border(draw, 630 - hnr_two / 2, 1077, str(Honor[1]), font=honor_font, shadowcolor=(205, 205, 205), fillcolor="White",
                    tchik=0.3, border=0.3)
        hnr_thr, h = honor_font.getsize(str(Honor[2]))
        text_border(draw, 630 - hnr_thr / 2, 1125, str(Honor[2]), font=honor_font, shadowcolor=(185, 122, 87), fillcolor="White",
                    tchik=0.3, border=0.3)

        # 左下角 广告区域
        qyt_code = make_qr_code(AD_qrCode)
        box = (40, 965, 156, 1081)
        sticker = qyt_code.resize((box[2] - box[0], box[3] - box[1]))  # 将二维码resize
        img_poster.paste(sticker, (box[0], box[1]), sticker)  # 第一个参数表示需要粘贴的图像，中间的是坐标，最后是一个是mask图片，用于指定透明区域。

        # AD 广告文案
        font = ImageFont.truetype('images\Dengl.ttf', 24)
        draw.text((40, 1098), AD_text_title, (255, 255, 255), font=font)
        draw.text((40, 1138), AD_text_subsc, (255, 255, 255), font=font)

        # img_poster.show()  # 查看合成的图片
        file_name = ID + '_' + date + '.png'
        img_poster.save(file_name)
        print('已保存为\t\t', file_name,
              '\nrun_used time:\t\t', round(time.time() - t1, 3))
        return img_poster
    except:
        raise
        # print('不知道哪儿出问题了，反正就是出问题了，快去Trouble Shooting！')


if __name__ == '__main__':
    # for i in range(100):
    edit_poster(
        subject='Python 基础班',
        date=date,

        # 个人数据 由数据库提供
        # score =[[到课次，总课数],[上交数，总作业数], 视频观看次, 视频每周加分, 总成绩]
        score=[[1, 2], [3, 3], 1, 4, 166.0],
        ID='nb_mengjq',
        name='孟某',
        Honor=[1, 4, 7],  # 冠军次数，亚军，季军

        # AD信息由商务定义
        AD_qrCode='http://www.qytang.com',  # 二维码内的内容，可以是链接，字符
        AD_text_title='扫码加入 多人在线',  # 不超过九个中文字符
        AD_text_subsc='劲爆刺激 打卡学习',  # 不超过九个中文字符
    ).show()
