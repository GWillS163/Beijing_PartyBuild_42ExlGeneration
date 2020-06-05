from PIL import Image, ImageDraw, ImageFont, ImageFilter
import time
import qrcode

# 输入二维码信息， 返回定制的 白色透明二维码  img对象
def make_qr_code(content, save_path=None):
    qr_code_maker = qrcode.QRCode(version=3,
                                  error_correction=qrcode.constants.ERROR_CORRECT_M,
                                  box_size=8,
                                  border=0,
                                  )
    qr_code_maker.add_data(data=content)
    qr_code_maker.make(fit=True)  # 自动调整大小
    img = qr_code_maker.make_image(fill_color="White",
                                back_color = "transparent"#"gray"
                                   ).convert('RGBA')

    return img.convert("RGBA")
    # img.save(save_path)

# 修改海报数据
def edit_poster(subject, date, score,
                ID, name, Champion, runnerup, Second_runnerup,
                AD_qrCode, AD_text):
    img = Image.open('images\\qyt_poster-blank.png')

    # 创建Draw对象:
    draw = ImageDraw.Draw(img)
    # 创建Font对象:
    title_font = ImageFont.truetype('images\Deng.ttf', 30)
    draw.text((308, 41), subject,(255,255,255),font=title_font)
    draw.text((415, 91), date, (255,255,255),font=title_font)

    # 创建Font对象: 标准分
    score_font = ImageFont.truetype('images\Dengl.ttf', 36)
    s_score_font = ImageFont.truetype('images\Dengl.ttf', 23)
    draw.text((365, 205), score[0][0], (255, 255, 255), font=score_font)
    draw.text((393, 214), '/' + score[0][1], (255, 255, 255), font=s_score_font)
    draw.text((402, 256), score[1], (255, 255, 255), font=score_font)
    draw.text((353, 313), score[2][0], (255, 255, 255), font=score_font)
    draw.text((393, 319), '/' + score[2][1], (255, 255, 255), font=s_score_font)
    draw.text((402, 357), score[3], (255, 255, 255), font=score_font)

    # 总成绩
    font = ImageFont.truetype('images\Dengb.ttf', 280)
    draw.text((180, 480), score[4], (0, 153, 255), font=font)

    # 右下角区域， ID_姓名， 荣誉
    font = ImageFont.truetype('images\Dengl.ttf', 36)
    draw.text((372, 956), ID, (255, 255, 255), font=font)
    draw.text((581, 956), name, (255, 255, 255), font=font)
    draw.text((614, 1017), Champion, (255, 255, 255), font=font)
    draw.text((614, 1067), runnerup, (255, 255, 255), font=font)
    draw.text((614, 1117), Second_runnerup, (255, 255, 255), font=font)

    draw.text((40, 1098), AD_text, (255, 255, 255), font=font)

    # make_QR_code
    qyt_code = make_qr_code(AD_qrCode)

    #  P上去
    poster = add_qyt_code(qyt_code, img)
    poster.show()  # 查看合成的图片
    poster.save(ID + date + '.png')

# 负责贴二维码到poster上
def add_qyt_code(sticker,poster):
    # 加载需要粘贴的二维码， 最好是带透明通道的！
    box = (40, 965, 156, 1081)  # base_img的范围区域
    sticker = sticker.resize((box[2] - box[0], box[3] - box[1]))  # 将二维码resize

    # 将透明图覆盖上去，中间透明区域将显示出底图
    poster.paste(sticker, (box[0], box[1]), sticker)  # 第一个参数表示需要粘贴的图像，中间的是坐标，最后是一个是mask图片，用于指定透明区域。

    return poster

if __name__ == '__main__':
    t1 = time.time()
    date = time.asctime().split()[1] + '-' + time.asctime().split()[2] + '-' + time.asctime().split()[4]

    edit_poster(subject='网络入门课-第一期',
                date=date,

                score=[['7', '14'], '7', ['14', '23'], '4', '5.0'],
                ID='nb_mengjq',
                name='孟骏清',
                Champion='8',
                runnerup='1',
                Second_runnerup='0',

                AD_qrCode='https:g.cn',
                AD_text='广告位招租'
                )
    print('run_used time:', time.time()-t1)