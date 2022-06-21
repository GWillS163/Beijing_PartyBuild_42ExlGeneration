from pymouse import *     # 模拟鼠标所使用的包
from pykeyboard import *   # 模拟键盘所使用的包
import time   # 连续进行两个动作可能太快而效果不明显，因此加入暂停时间

m = PyMouse()   # 鼠标的实例m
k = PyKeyboard()   # 键盘的实例k

def Scoring():
    Score = input('请输入你判定的分数<A /A- /B+>\t')
    if Score == '':
        Score = 'A'
    #切换到上一个任务 前端
    k.press_key(k.alt_key)
    k.tap_key(k.tab_key)
    k.release_key(k.alt_key)
    time.sleep(0.3)
    #win + v
    k.press_key(91)
    k.tap_key('V')
    k.release_key(91)

    time.sleep(0.3)
    #down- ↓
        #选择<A / A- / B+>
    if Score == 'B+':
        k.tap_key(k.down_key,2)
    elif Score == 'A-':
        k.tap_key(k.down_key)
    else:
        print('已选择默认为'+ Score)

    #空格  选择
    k.tap_key(k.space_key)
    time.sleep(0.3)


def Save_as(score='A'):
    #F12
    k.tap_key(123)
    time.sleep(1)
    #输入 <评分>
        #→
    k.tap_key(k.right_key)
        #删5个末尾
    k.tap_key(k.backspace_key,5)

        #输入<评分>
    score = score.upper()
    k.type_string('-')
    k.type_string(score)

    #选择保存路径
        #F4 选择路径
    k.tap_key(115)
    k.press_key(17)  # ctrl + a
    k.tap_key('a')
    k.release_key(17)
        #输入桌面路径
    k.type_string('C:\\Users\\admin\\Desktop',)
    time.sleep(0.5)
    #k.tap_key(40)
    #回车
    time.sleep(0.3)
    k.tap_key(k.enter_key)
    #alt + s
    k.press_key(k.alt_key)
    k.tap_key('s')
    k.release_key(k.alt_key)
    time.sleep(0.3)

    #alt +F4
    k.press_key(k.alt_key)
    k.tap_key(115)
    k.release_key(k.alt_key)
    time.sleep(0.3)
    #回车

    k.tap_key(k.enter_key)
    print('Over')


print('\n'*3,'请注意切换到英文状态')
Score = input('请输入你判定的分数<A /A- /B+>\t')
if Score == '':
    Score = 'A'
time.sleep(0.3)
k.press_key(k.alt_key)
k.tap_key(k.tab_key)
k.release_key(k.alt_key)
time.sleep(0.3)
Save_as(Score)

