import re, time

# # 读取最后一行
# f = open('.\\t.db')
# txt = f.readlines()[-1]
# pre_one_hand_score = re.findall('one_hand:(.*)\t', txt)
# pre_3x3x3_score = re.findall('3x3x3:(.*)', txt)

# 写入文件
score = 'score'
with open('.\\t.db', 'a') as f:

    # 确定是当前月份
    if
    # 写入
    f.writelines('\n' + time.asctime().split(' ')[1] +
                 '\tone_hand:' + score + '\t 3x3x3:' + score)