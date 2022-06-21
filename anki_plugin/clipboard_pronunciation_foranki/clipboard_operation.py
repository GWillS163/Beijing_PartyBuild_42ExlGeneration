import win32clipboard as wc
import win32con


def get_text():
    """ 读取 """
    wc.OpenClipboard()
    text = wc.GetClipboardData(win32con.CF_TEXT)
    wc.CloseClipboard()
    return text


def set_text(strs):
    """ 写入 """
    wc.OpenClipboard()
    wc.EmptyClipboard()
    wc.SetClipboardData(win32con.CF_TEXT, strs)
    wc.CloseClipboard()


if __name__ == '__main__':
    strs = b'Unremitting self-improvement'
    set_text(strs)
    print(get_text())


# 执行结果：b'Unremitting self-improvement'