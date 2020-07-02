import win32gui
import win32con
import win32clipboard as w

def win32_send_msg(window_name):
    # 发送的消息
    msg = "测试代码_本消息由python win32gui发送"
    # 窗口名字
    window_name
    # 将测试消息复制到剪切板中
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_UNICODETEXT, msg)
    w.CloseClipboard()
    # 获取窗口句柄
    handle = win32gui.FindWindow(None, window_name)
    # while 1==1:
    if 1 == 1:
        # 填充消息
        win32gui.SendMessage(handle, 770, 0, 0)
        # 回车发送消息
        win32gui.SendMessage(handle, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)

# 运行前需要打开相应的窗口
if __name__ == '__main__':
    win32_send_msg("网络入门课 第一期")