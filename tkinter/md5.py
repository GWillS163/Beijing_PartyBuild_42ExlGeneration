from tkinter import *
import hashlib
import time

LOG_LINE_NUM = 0

class MY_GUI():
    def __init__(self, init_windows_name):
        self.init_windows_name = init_windows_name

    def set_init_windows(self):
        self.init_windows_name.title("文本处理工具_v1.2")
        self.init_windows_name.geometry('1068x681+10+10')
        self.init_data_label = Label(self.init_windows_name, text="待处理数据")
        self.init_data_label.grid(row=0, column=0)
        self.result_data_label = Label(self.init_windows_name, text="输出结果")
        self.result_data_label.grid(row=0, column=12)
        self.log_label = Label(self.init_windows_name, text="日志")
        self.log_label.grid(row=0, column=12)

        # 文本框
        self.init_data_Text = Text(self.init_windows_name, width=67, height=35)
        self.init_data_Text.grid(row=1, column=0, rowspan=10, columnspan=10)
        self.result_data_Text = Text(self.init_windows_name, width=70, height=49)
        self.result_data_Text.grid(row=1, column=12, rowspan=15, columnspan=10)
        self.log_data_Text = Text(self.init_windows_name, width=66, height=9)
        self.log_data_Text.grid(row=13, column=0, columnspan=10)

        # 按钮
        self.str_trans_to_md5_button = Button(self.init_windows_name, text="字符串转MD5", bg="gray", width=10, command=self.str_trans_to_md5) # 调用功能
        self.str_trans_to_md5_button.grid(row=1, column=11)

    def str_trans_to_md5(self):
        src = self.init_data_Text.get(1.0, END).strip().replace("\n", "").encode()
        if src:
            try:
                myMd5 = hashlib.md5()
                myMd5.update(src)
                myMd5_Digest = myMd5.hexdigest()
                self.result_data_Text.delete(1.0, END)
                self.result_data_Text.insert(1.0, myMd5_Digest)
                self.write_log_to_Text("INFO: str_trans_to_md5 success")
            except:
                self.result_data_Text.delete(1.0, END)
                self.result_data_Text.insert(1.0, "字符串转MD5失败")
        else:
            self.write_log_to_Text("ERROR:")

    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return current_time

    def write_log_to_Text(self, logmsg):
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        logmsg_in = str(current_time) + " " + str(logmsg) + "\n"
        if LOG_LINE_NUM <= 7:
            self.log_data_Text.insert(END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.log_data_Text.delete(1.0, 2.0)
            self.log_data_Text.insert(END, logmsg_in)

def gui_start():
    init_window = Tk()
    ZM = MY_GUI(init_window)
    ZM.set_init_windows()
    init_window.mainloop()

gui_start()