from PIL import Image

def s(qyt_code,poster):
    # 加载需要粘贴的二维码， 最好是带透明通道的！
    sticker = Image.open(qyt_code)
    box = (40, 965, 156, 1081)  # base_img的范围区域
    sticker = sticker.resize((box[2] - box[0], box[3] - box[1]))  # 将二维码resize

    # 加载poster,作为底图
    back_img = Image.open(poster)
    # 将透明图覆盖上去，中间透明区域将显示出底图
    back_img.paste(sticker, (box[0], box[1]), sticker)  # 第一个参数表示需要粘贴的图像，中间的是坐标，最后是一个是mask图片，用于指定透明区域。
    back_img.show()

s(".\\images\\qyt_code.png",".\\images\\qyt_poster-blank.png")
