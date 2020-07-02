import time, os, re
from pymouse import *  # 模拟鼠标所使用的包
from pykeyboard import *  # 模拟键盘所使用的包
time.sleep(3)
M = PyMouse()
K = PyKeyboard()
K.type_string('1274667113', 0.1)
time.sleep(3)
K.tap_key(38)  # 面板选择
K.tap_key(38)
K.tap_key(38)
time.sleep(1)
K.tap_key(K.enter_key)
time.sleep(1)