from PIL import Image, ImageDraw, ImageFont, ImageFilter
import time
import qrcode

date = time.asctime().split()[1] + '-' + time.asctime().split()[2] + '-' + time.asctime().split()[4]

# 输入二维码信息， 返回定制的 白色透明二维码  img对象
def make_qr_code(content, save_path=None):
    qr_code_maker = qrcode.QRCode(version=3,
                                  error_correction=qrcode.constants.ERROR_CORRECT_M,
                                  box_size=8,
                                  border=0,
                                  )
    qr_code_maker.add_data(data=content)
    qr_code_maker.make(fit=True)  # 自动调整大小
    img = qr_code_maker.make_image(fill_color="navy",# "SlateGray",  # "teal",,#"navy",#"indigo" #"gray",#"White" # "cyan",
                                   back_color="transparent"  # "gray"
                                   ).convert('RGBA')

    return img.convert("RGBA")
    #img.save(save_path)

# 负责贴二维码到poster上
def add_sticker2poster(sticker, box, poster):
    # 加载需要粘贴的二维码， 最好是带透明通道的！
    # box是 base_img的范围区域
    sticker = sticker.resize((box[2] - box[0], box[3] - box[1]))  # 将二维码resize

    # 将透明图覆盖上去，中间透明区域将显示出底图
    poster.paste(sticker, (box[0], box[1]), sticker)  # 第一个参数表示需要粘贴的图像，中间的是坐标，最后是一个是mask图片，用于指定透明区域。
    return poster


# 修改海报数据
def edit_poster(subject, date, lst,
                ID, name, Honor,
                AD_qrCode, AD_text_title, AD_text_subsc):
    try:
        t1 = time.time()
        img_poster = Image.new(mode="RGB", size=(1080, 1440), color="DeepSkyBlue")
        draw = ImageDraw.Draw(img_poster)  # 创建Draw对象:

        # 画布上粘上你的图片
        # 其实也可以在底图作为画布进行编辑，而不用新建一个画布
        pic_img = Image.open('images\\edge.png')
        # pic_img = Image.open('images\\road.jpeg')
        pic_img = pic_img.resize((1080, 1440), Image.ANTIALIAS)
        img_poster.paste(pic_img)

        # # 模糊下方区域，并粘贴回来
        # bounds = (0, 940, 720, 1192)
        # # 裁剪出下方区域——高斯模糊↓
        # pic_img_sub = pic_img.crop(bounds)
        # pic_img_sub_blur = pic_img_sub.filter(ImageFilter.GaussianBlur(radius=21))
        # img_poster.paste(pic_img_sub_blur, (0, 940))
        # #
        # 粘上 右上角 logo
        #logo_img = Image.open('images\\qytanglogo_gray_white.png')
        logo_img = Image.open('images\\qytanglogo.png')
        #logo_img = logo_img.resize((150, 140), Image.ANTIALIAS)
        img_poster.paste(logo_img, (867, 35), logo_img)
        # # 右上方 课程名称   日期
        # title_font = ImageFont.truetype('images\Dengb.ttf', 30)
        # w, h = draw.textsize('a' * txt_len(subject), title_font)  # 不能直接测量中文字符长度。
        # w2, h2 = draw.textsize('a' * txt_len(date), title_font)  # 写一个函数测量中英混和的str长度
        # draw.text((570 - w, 47), subject, (240, 255, 240), font=title_font)
        # draw.text((540 - w2, 96), date, (255, 255, 255), font=title_font)

        # 居中上方 文字
        s_score_font = ImageFont.truetype('images\Dengb.ttf', 50)
        draw.text((109, 223), '我在乾颐堂上交了 CCNA的第五天作业', (255, 255, 255), font=s_score_font)
        draw.text((109, 300), '学习到了', (255, 255, 255), font=s_score_font)

        s_score_font = ImageFont.truetype('images\Deng.ttf', 40)
        draw.text((201, 383), lst[0], (128, 128, 128), font=s_score_font)
        draw.text((201, 462), lst[1], (128, 128, 128), font=s_score_font)
        draw.text((201, 542), lst[2], (128, 128, 128), font=s_score_font)
        draw.text((201, 619), lst[3], (128, 128, 128), font=s_score_font)
        draw.text((201, 698), lst[4], (128, 128, 128), font=s_score_font)

        draw.text((200, 380), lst[0], (255, 255, 255), font=s_score_font)
        draw.text((200, 459), lst[1], (255, 255, 255), font=s_score_font)
        draw.text((200, 539), lst[2], (255, 255, 255), font=s_score_font)
        draw.text((200, 617), lst[3], (255, 255, 255), font=s_score_font)
        draw.text((200, 696), lst[4], (255, 255, 255), font=s_score_font)

        # # 右下角区域， ID_姓名， 荣誉
        # name_font = ImageFont.truetype('images\Dengb.ttf', 36)
        # # 测量宽度 （注意，这里直接放入 英文字符串即可）
        # id_w, hei = draw.textsize(ID, name_font)
        # # (546 - id_w) 是向右对齐
        # draw.text((546 - id_w, 956), ID, (255, 255, 255), font=name_font)
        # name_w, hei = draw.textsize('a' * txt_len(name), name_font)  # 注意！这里测量长度使用的是txt_Len()
        # draw.text((686 - name_w, 956), name, (255, 255, 255), font=name_font)
        #
        # text_border(draw, 620, 1024, str(Honor[0]), font=honor_font, shadowcolor=(255, 201, 14), fillcolor=False,
        #             tchik=0.3, border=0.3)
        # text_border(draw, 620, 1077, str(Honor[1]), font=honor_font, shadowcolor=(205, 205, 205), fillcolor=False,
        #             tchik=0.3, border=0.3)
        # text_border(draw, 620, 1125, str(Honor[2]), font=honor_font, shadowcolor=(185, 122, 87), fillcolor=False,
        #             tchik=0.3, border=0.3)

        # 左下角 广告区域
        # make_QR_code
        qyt_code = make_qr_code(AD_qrCode)
        # AD 广告文案
        font = ImageFont.truetype('images\Dengl.ttf', 28)
        draw.text((85, 1357), AD_text_title, (255, 255, 255), font=font)
        draw.text((85, 1387), AD_text_subsc, (255, 255, 255), font=font)
        # P上去
        img_poster = add_sticker2poster(qyt_code, (87, 1116, 319, 1348), img_poster)

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
    # # for i in range(100):
    edit_poster(
        subject= '安全直通车 ',  # 汉字对齐不严谨时，多加一个空格试试
        date=date,

        # 个人数据 由数据库提供
        # score =[[到课次，总课数],[上交数，总作业数], 视频观看次, 视频每周加分]
        lst=[
            '1. 如何把大象放到冰箱',
            '2. 如何把大象取出来',
            '3. ASA 的拼写',
            '4. 交换机的开关机',
            '5. Python的安装与卸载'
           ],
        ID='rsec_mengjq',
        name='孟骏清',
        Honor=[1, 3, 0],  # 冠军次数，亚军，季军

        # AD信息由商务定义
        AD_qrCode='二维码的内容可以自定义，稍后再说',  # 二维码内的内容，可以是链接，字符
        AD_text_title='扫码加入 多人在线',  # 不超过九个中文字符
        AD_text_subsc='劲爆刺激 打卡学习',  # 不超过九个中文字符
    ).show()
    # day
    # lst = []
    # code_url =
    # make_qr_code('https://jinshuju.net/f/nTK6vp', save_path='t.png')