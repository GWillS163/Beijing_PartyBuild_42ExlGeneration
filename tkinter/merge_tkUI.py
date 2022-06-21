from tkinter import *
import tkinter
class Main_UI():
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name # 设置窗口

    def set_init_window(self):
        self.init_window_name.title("okfun视频解密合成工具")           # 窗口名
        # self.init_window_name.geometry('320x160+10+10')                         #290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name.geometry('800x600+10+10')

        # self.up_layout = tkinter.PanedWindow(orient='vertical')
        # self.init_window_name.pack(fill="both", expand=1)

        self.init_thread_states = Label(self.up_layout, text="Threading_states:")
        # self.init_thread_states.grid(row=1, column=0)
        self.init_t1 = Label(self.init_window_name, text="T1_download下载线程")
        self.init_t1.grid(row=1, column=1)
        self.init_t2 = Label(self.init_window_name, text="T2_decry解密线程")
        self.init_t2.grid(row=1, column=2)
        self.init_t3 = Label(self.init_window_name, text="T3_send发送线程")
        self.init_t3.grid(row=1, column=3)
        self.init_t4 = Label(self.init_window_name, text="T4_delete删除线程")
        self.init_t4.grid(row=1, column=4)

        self.t1_status = Entry(self.init_window_name, bd=2, width=10, state=DISABLED)
        self.t1_status.grid(row=2, column=1)
        self.t2_status = Entry(self.init_window_name, bd=2, width=10, state=DISABLED)
        self.t2_status.grid(row=2, column=2)
        self.t3_status = Entry(self.init_window_name, bd=2, width=10, state=DISABLED)
        self.t3_status.grid(row=2, column=3)
        self.t4_status = Entry(self.init_window_name, bd=2, width=10, state=DISABLED)
        self.t4_status.grid(row=2, column=4)
        self.all_status = Entry(self.init_window_name, bd=2, width=10, state=DISABLED)
        self.all_status.grid(row=2, column=6)

        # 检测按钮
        self.local_test_btn = Button(self.init_window_name, activebackground='#c7d0e4', text='本地检测')
        self.local_test_btn.grid(row=3, column=0, columnspan=1)
        self.local_test = Entry(self.init_window_name, bd=1, width=20, state=NORMAL)
        self.local_test.grid(row=4, column=0)
        self.remote_test_btn = Button(self.init_window_name, activebackground='#c7d0e4', text='远端检测')
        self.remote_test_btn.grid(row=3, column=1)
        self.remote_test = Entry(self.init_window_name, bd=1, width=20, state=NORMAL)
        self.remote_test.grid(row=4, column=1, columnspan=1)
        self.local_test_btn = Button(self.init_window_name, activebackground='#c7d0e4', text='下载指定远程文件')
        self.local_test_btn.grid(row=3, column=2, columnspan=1)
        self.local_test = Entry(self.init_window_name, bd=1, width=20, state=NORMAL)
        self.local_test.grid(row=4, column=2)
        self.remote_test_btn = Button(self.init_window_name, activebackground='#c7d0e4', text='本地解密测试')
        self.remote_test_btn.grid(row=3, column=3)
        self.local_test = Entry(self.init_window_name, bd=1, width=20, state=NORMAL)
        self.local_test.grid(row=4, column=3)
        self.local_test_btn = Button(self.init_window_name, activebackground='#c7d0e4', text='远程发送测试')
        self.local_test_btn.grid(row=3, column=4)
        self.local_test = Entry(self.init_window_name, bd=1, width=20, state=NORMAL)
        self.local_test.grid(row=4, column=4)
        self.remote_test_btn = Button(self.init_window_name, activebackground='#963929', text='远程删除_所有')
        self.remote_test_btn.grid(row=3, column=5)
        self.remote_test_btn = Button(self.init_window_name, activebackground='#963929', text='远程删除_所有')
        self.remote_test_btn.grid(row=4, column=5)

        self.init_vdo_num = Label(self.init_window_name, text="编号")
        self.init_vdo_num.grid(row=5, column=0)
        self.init_src_loca = Label(self.init_window_name, text="源文件位置")
        self.init_src_loca.grid(row=5, column=1)
        self.init_down_status = Label(self.init_window_name, text="下载情况")
        self.init_down_status.grid(row=5, column=2)
        self.init_decry_status = Label(self.init_window_name, text="解密情况")
        self.init_decry_status.grid(row=5, column=3)
        self.init_local_temp_location = Label(self.init_window_name, text="本地缓存位置")
        self.init_local_temp_location.grid(row=5, column=4)
        self.init_ftp_send_status = Label(self.init_window_name, text="ftp发送情况")
        self.init_ftp_send_status.grid(row=5, column=5)
        self.init_remote_file_delete = Label(self.init_window_name, text="远程文件删除")
        self.init_remote_file_delete.grid(row=5, column=6)
        self.init_local_temp_delete = Label(self.init_window_name, text="本地缓存删除")
        self.init_local_temp_delete.grid(row=5, column=7)
        # 原始数据录入框
        self.init_current_Text = Text(self.init_window_name, width=110, height=10)
        self.init_current_Text.grid(row=6, column=0, rowspan=1, columnspan=10)


        self.init_vdo_lst = Label(self.init_window_name, text="处理视频编号")
        self.init_vdo_lst.grid(row=50, column=0)
        # self.init_sub = PanedWindow(self.init_window_name, cnf={})
        # self.init_sub.grid(row=5, column=0)
        self.init_video_Text = Text(self.init_window_name, width=110, height=3)  # 视频列表
        self.init_video_Text.grid(row=52, column=0, rowspan=10, columnspan=2)
        # self.init_log_Text = Text(self.init_window_name, width=80, height=10)  # 原始数据录入框
        # self.init_log_Text.grid(row=30, column=1)
        # self.init_config_Text = Text(self.init_window_name, width=20, height=10)
        # self.init_config_Text.grid(row=30, column=2)

def gui_start():
    init_window = Tk()              # 实例化出一个父窗口
    ZMJ_PORTAL = Main_UI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()

    init_window.mainloop()          #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


gui_start()
