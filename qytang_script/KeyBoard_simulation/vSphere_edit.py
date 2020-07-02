from pymouse import *     # 模拟鼠标所使用的包
from pykeyboard import *   # 模拟键盘所使用的包
import time   # 连续进行两个动作可能太快而效果不明显，因此加入暂停时间
import win32clipboard as w
import win32con
import pyperclip

m = PyMouse()   # 鼠标的实例m
k = PyKeyboard()   # 键盘的实例k
# x_dim, y_dim = m.screen_size()     # 获取屏幕尺寸（一般为电脑屏幕的分辨率，如1920*1080）
# # 估计需要点击的位置坐标（不知道有没有定位代码，我没找到，我是自己估计的。例如，我的电脑屏幕为(1920，1080)，我想要单击的地方估计坐标为(10，500)）
# m.move(10, 500)   # 将鼠标移动到位（此步可忽略，直接单击也可）
# time.sleep(0.5)   # 暂停0.5s，方便观察移动结果
# m.click(10, 500, 1, 1)   # 表示在(10, 500)的地方，单击左键
#
#     m.move(x, y) # 鼠标移动到坐标(x, y)
#     m.click(x, y, button, n) # 鼠标点击。x,y–坐标， button–按键选项（1为左键，2为右键），n–点击次数（默认1此，2表示双击，仅此两个值）
#     m.screen_size() # 获取屏幕尺寸，返回两个值分别为长和宽

# 获取剪切板内容
def gettext():
    w.OpenClipboard()
    t = w.GetClipboardData(win32con.CF_TEXT)
    w.CloseClipboard()
    return t
def get_machine_name():
    #F2  113
    k.press_key(113)
    time.sleep(0.3)
    #CTRL+A
    k.press_key(17)
    k.tap_key('a')
    k.release_key(17)
    time.sleep(0.3)
    #CTRL+C
    k.press_key(17)
    k.tap_key('c')
    k.release_key(17)
    time.sleep(0.3)
    k.tap_key(27)#ESC
    #打印剪切板+shutdown

    ttext = str(gettext(),encoding="gbk")
    return ttext

def pause_check():
    input('please check')
    k.press_key(k.alt_key)
    k.tap_key(k.tab_key)
    k.release_key(k.alt_key)

def poweroff():
    time.sleep(1)
    k.press_key(17)  # ctrl + e
    k.tap_key('e')
    k.release_key(17)
    time.sleep(0.3)
    k.tap_key('Y')  # 是否关机，YES
    time.sleep(0.3)
def poweron():
    time.sleep(1)
    # k.tap_key(93)#右键菜单
    k.press_key(17)  # ctrl + e
    k.tap_key('b')
    k.release_key(17)
    time.sleep(0.3)
def snapshot(string,choice):
    print('开始快照!')
    k.tap_key(93)
    time.sleep(0.3)
    k.tap_key('S') #– 模拟键盘按H键
    time.sleep(0.3)
    k.tap_key('T')
    time.sleep(0.3)
    k.type_string(string)   # 模拟键盘输入字符串
    if choice == '1'or 1:
        #tab tab space取消内存快照
        k.tap_key(k.tab_key)
        time.sleep(0.1)
        k.tap_key(k.tab_key)
        k.tap_key(k.space_key)
        time.sleep(0.2)
    k.tap_key(k.enter_key)
    time.sleep(0.5)

def rename():
#获取虚拟机名
    name = get_machine_name()
    print('srcname:\t\t',name,type(name))
    newname = ''
# 名称更改---------------------------------------------------<<<<<<<<<<<<<<<<<<<<<<<
    # 删除所有'_SEC'
    # pre, suf = name.split('_SEC')#删除'_SEC'
    # 翻译并替换入门课主机名
    # newname = name.replace('DNS_WEB_WIN2008','互联网服务器_DNS_WEB(WIN2008)',1).replace('Internal_Server_WIN2008','内部服务器_Server(WIN2008)',1).replace('Internet_PC_WIN7','互联网_Internet_PC(WIN7)',1).replace('Internet_VyOS','互联网_VyOS(开机勿动',1).replace('PC1_WIN10','内部_PC1(WIN10)',1).replace('PC2_WIN7','内部_PC2(WIN7)',1)

# 检测newname，执行或退出
    if newname == '':
        return print('重命名规则定义为空!!!')
    print('newname:\t\t', newname)
    pyperclip.copy(newname)
# 输入
    k.press_key(113)#F2  113
    time.sleep(0.5)
    # 以下语句模拟键盘点击ctrl+v
    k.press_key(k.control_key)
    k.tap_key('v')
    k.release_key(k.control_key)

# k.type_string(newname,0.03)
    time.sleep(0.3)
    k.tap_key(k.enter_key)


def run():
    #print('请选择参数，<poweroff/poweron/snapshot>,<INT>,<up/down>')
    operat = input('请选择操作<\n1.关机\n2.开机\n3.打快照\n4.重命名（规则须定义）\n5.获取主机名>')
    tm = int(input('循环操作多少页？ 输入整数'))
    direction = input('1.up/2.down')

    if direction == '1': #赋值上/下
        direction = 38
    elif direction == '2':
        direction = 40
    else:
        print("please input lowcase [up/down]")
        return
    if operat == '3':
        stri = input('\t####输入要定义的快照名称')
        choice = input('\t####输入0为开机快照,1为关机快照')

    print("prepare")
    time.sleep(1)
    k.press_key(k.alt_key)
    k.tap_key(k.tab_key)
    k.release_key(k.alt_key)
    time.sleep(0.3)

    for i in range(int(tm)):#遍历执行
        print('\n' + str(i) +'.获取虚拟机名：\t' + get_machine_name(),end='')
        if operat == '1':
            poweroff()
        elif operat == '2':
            poweron()
        elif operat == '3':
            snapshot(stri,choice)
        elif operat == '4':
            rename()
        elif operat == '5':
            print('')
        k.tap_key(direction)# 38up
        print('Done    ' + str(time.ctime()))
    input('anykey')
def help():
    print('''
虚拟键码	 对应值 	对应键
VK_LBUTTON	1	鼠标左键
VK_RBUTTON	2	鼠标右键
VK_CANCEL	3	Cancel
VK_MBUTTON	4	鼠标中键
VK_XBUTTON1	5	
VK_XBUTTON2	6	
VK_BACK	8	Backspace
VK_TAB	9	Tab
VK_CLEAR	12	Clear
VK_RETURN	13	Enter
VK_SHIFT	16	Shift
VK_CONTROL	17	Ctrl
VK_MENU	18	Alt
VK_PAUSE	19	Pause
VK_CAPITAL	20	Caps Lock
VK_KANA	21	
VK_HANGUL	21	
VK_JUNJA	23	
VK_FINAL	24	
VK_HANJA	25	
VK_KANJI	25*	
VK_ESCAPE	27	Esc
VK_CONVERT	28	
VK_NONCONVERT	29	
VK_ACCEPT	30	
VK_MODECHANGE	31	
VK_SPACE	32	Space
VK_PRIOR	33	Page Up
VK_NEXT	34	Page Down
VK_END	35	End
VK_HOME	36	Home
VK_LEFT	37	Left Arrow
VK_UP	38	Up Arrow
VK_RIGHT	39	Right Arrow
VK_DOWN	40	Down Arrow
VK_SELECT	41	Select
VK_PRINT	42	Print
VK_EXECUTE	43	Execute
VK_SNAPSHOT	44	Snapshot
VK_INSERT	45	Insert
VK_DELETE	46	Delete
VK_HELP	47	Help
48	0
49	1
50	2
51	3
52	4
53	5
54	6
55	7
56	8
57	9
65	A
66	B
67	C
68	D
69	E
70	F
71	G
72	H
73	I
74	J
75	K
76	L
77	M
78	N
79	O
80	P
81	Q
82	R
83	S
84	T
85	U
86	V
87	W
88	X
89	Y
90	Z
VK_LWIN	91	
VK_RWIN	92	
VK_APPS	93	
VK_SLEEP	95	
VK_NUMPAD0	96	小键盘 0
VK_NUMPAD1	97	小键盘 1
VK_NUMPAD2	98	小键盘 2
VK_NUMPAD3	99	小键盘 3
VK_NUMPAD4	100	小键盘 4
VK_NUMPAD5	101	小键盘 5
VK_NUMPAD6	102	小键盘 6
VK_NUMPAD7	103	小键盘 7
VK_NUMPAD8	104	小键盘 8
VK_NUMPAD9	105	小键盘 9
VK_MULTIPLY	106	小键盘 *
VK_ADD	107	小键盘 +
VK_SEPARATOR	108	小键盘 Enter
VK_SUBTRACT	109	小键盘 -
VK_DECIMAL	110	小键盘 .
VK_DIVIDE	111	小键盘 /
VK_F1	112	F1
VK_F2	113	F2
VK_F3	114	F3
VK_F4	115	F4
VK_F5	116	F5
VK_F6	117	F6
VK_F7	118	F7
VK_F8	119	F8
VK_F9	120	F9
VK_F10	121	F10
VK_F11	122	F11
VK_F12	123	F12
VK_F13	124	
VK_F14	125	
VK_F15	126	
VK_F16	127	
VK_F17	128	
VK_F18	129	
VK_F19	130	
VK_F20	131	
VK_F21	132	
VK_F22	133	
VK_F23	134	
VK_F24	135	
VK_NUMLOCK	144	Num Lock
VK_SCROLL	145	Scroll
VK_LSHIFT	160	
VK_RSHIFT	161	
VK_LCONTROL	162	
VK_RCONTROL	163	
VK_LMENU	164	
VK_RMENU	165	
VK_BROWSER_BACK	166	
VK_BROWSER_FORWARD	167	
VK_BROWSER_REFRESH	168	
VK_BROWSER_STOP	169	
VK_BROWSER_SEARCH	170	
VK_BROWSER_FAVORITES	171	
VK_BROWSER_HOME	172	
VK_VOLUME_MUTE	173	VolumeMute
VK_VOLUME_DOWN	174	VolumeDown
VK_VOLUME_UP	175	VolumeUp
VK_MEDIA_NEXT_TRACK	176	
VK_MEDIA_PREV_TRACK	177	
VK_MEDIA_STOP	178	
VK_MEDIA_PLAY_PAUSE	179	
VK_LAUNCH_MAIL	180	
VK_LAUNCH_MEDIA_SELECT	181	
VK_LAUNCH_APP1	182	
VK_LAUNCH_APP2	183	
VK_OEM_1	186	; :
VK_OEM_PLUS	187	= +
VK_OEM_COMMA	188	
VK_OEM_MINUS	189	- _
VK_OEM_PERIOD	190	
VK_OEM_2	191	/ ?
VK_OEM_3	192	` ~
VK_OEM_4	219	[ {
VK_OEM_5	220	\ |
VK_OEM_6	221	] }
VK_OEM_7	222	' "
VK_OEM_8	223	
VK_OEM_102	226	
VK_PACKET	231	
VK_PROCESSKEY	229	
VK_ATTN	246	
VK_CRSEL	247	
VK_EXSEL	248	
VK_EREOF	249	
VK_PLAY	250	
VK_ZOOM	251	
VK_NONAME	252	
VK_PA1	253	
VK_OEM_CLEAR	254	''')


run()

