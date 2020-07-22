from PIL import Image, ImageDraw, ImageFont, ImageFilter
import time,re


date = time.asctime().split()[4] + '-' + time.asctime().split()[1]
# 输入图片

# 用于文字边框展示，传入draw,坐标x,y，字体，边框颜色和填充颜色
def text_border(draw, x, y, text,font, shadowcolor, fillcolor):
    # thin border
    draw.text((x - 3, y), text, font=font, fill=shadowcolor)
    draw.text((x + 3, y), text, font=font, fill=shadowcolor)
    draw.text((x, y - 3), text, font=font, fill=shadowcolor)
    draw.text((x, y + 3), text, font=font, fill=shadowcolor)

    # thicker border
    draw.text((x - 1, y - 1), text, font=font, fill=shadowcolor)
    draw.text((x + 1, y - 1), text, font=font, fill=shadowcolor)
    draw.text((x - 1, y + 1), text, font=font, fill=shadowcolor)
    draw.text((x + 1, y + 1), text, font=font, fill=shadowcolor)

    # now draw the text over it
    draw.text((x, y), text, font=font, fill=fillcolor)


# 修改海报数据
def edit_poster(subject, score, pre_score,
                honor):
    # if subject == '0':
    #     subject = '3x3x3'
    # elif subject == '1':
    #     subject = 'one_hand'
    # else:
    #     return print('项目参数  错误 重新输入！\n\n')
    # pre_score = 20

    try:
        if score < pre_score:
            score_area = str(score) + '↑'
            color = (43, 173, 53)
        elif score > pre_score:
            score_area = str(score) + '↓'
            color = (173, 43, 53)
        elif score == pre_score:
            score_area = str(score) + '--'
            color = (255, 255, 255)
        else:
            print('未能检测出分数！\n\n')
    except ValueError:
        print('值错误！ float不允许太大')
    try:
        t1 = time.time()
        img = Image.open(subject + '.jpg')
        # 创建Draw对象:
        draw = ImageDraw.Draw(img)

        # 日期
        title_font = ImageFont.truetype('images\Dengl.ttf', 160)
        text_border(draw, 880, 320, date, title_font, (0, 0, 0), fillcolor=(255, 255, 255))
        # 成绩
        score_font = ImageFont.truetype('images\Dengb.ttf', 220)
        text_border(draw, 940, 580, score_area, score_font, (255, 255, 255), fillcolor=color)

        # 荣誉！
        honor_font = ImageFont.truetype('images\Dengb.ttf', 210)
        draw.text((80, 280), honor[0], (74,202,109), font=honor_font)
        draw.text((80, 480), honor[1], (255, 207, 52), font=honor_font)
        draw.text((80, 680), honor[2], (51, 136, 255), font=honor_font)

        #img.show()  # 查看合成的图片
        file_name = subject + '_' + str(score) + '_' + date + '.jpg'
        img.save(file_name)
        print('已保存为\t\t', file_name,
              '\nrun_used time:\t\t', round(time.time() - t1, 3), '\n\n')
        return img
    except:
        #raise
        print('不知道哪儿出问题了，反正就是出问题了，快去Trouble Shooting！')

def run():

    # 读取文件最后一行
    f = open('.\\resource\\cube.db', "r")
    try:
        #print(f.readlines())
        txt = f.readlines()[-1]
        pre_one_hand_score = re.findall('one_hand:(.*)\t', txt)[0]
        pre_3x3x3_score = re.findall('3x3x3:(.*)', txt)[0]
        print('■■■■■■■■■■■■■■■■■■■\n读取到最近一条成绩为:\n\t'
              , txt
              , '\n')
    except IndexError:
        print('索引错误，或.\\cube.db是空文件！将过去成绩视为0')
        pre_one_hand_score = 0
        pre_3x3x3_score = 0
    f.close()

    # 循环两个成绩
    scorels = []
    subject = '3x3x3'
    for pre_score in [pre_one_hand_score, pre_3x3x3_score]:
        honor = ['', '', '']

        score = input(date + '  \t【' + subject + '】\t■>>>')
        if score == '':
            score = 0
        scorels.append(float(score))
        honor[0] = input('input one ==[<honor>]==\t>■>>>')
        if honor[0] == '':
            pass
        else:
            honor[1] = input('input two ==[<honor>]==\t■>>>')
            if honor[1] == '':
                pass
            else:
                honor[2] = input('input thre==[<honor>]==\t■>>>')
        edit_poster(str(subject), float(score), float(pre_score), honor)
        subject = 'one_hand'

    # 写入记录的成绩
    with open('.\\resource\\cube.db', 'a') as f:
        f.write('\n' + date
                + '\tone_hand:' + str(scorels[1]) +
                '\t 3x3x3:' + str(scorels[0]))

# while True:
# if __name__ == '__main__':
#     current_moth_time = input('请输入本月测速的时间')
run()