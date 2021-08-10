import os
import threading
import time
from tkinter import *
import tkinter
from config_parser import *
from decry_core import decry_obj, queue_info
from operate_tools import *
from background_function_main import main_decry_info, main_multi_thread, t1_downs_q, t3_send
class merge_UI():
    def __init__(self, windows_name):
        self.windows_name = windows_name
        self.source_file_delete = tkinter.BooleanVar()
        self.cfg_cmb_strip = cfg_cmb_strip  # 合并步幅

    def set__windows(self):
        self.windows_name.title('merge自动化工具')
        lay = tkinter.PanedWindow(orient=VERTICAL)
        lay.pack(fill="both", expand=1)
        status_bar = tkinter.PanedWindow(orient="horizontal")
        test_bar = tkinter.PanedWindow(orient="horizontal")
        test_bar1 = tkinter.PanedWindow(orient="vertical")
        test_bar2 = tkinter.PanedWindow(orient="vertical")
        test_bar3 = tkinter.PanedWindow(orient="vertical")
        test_bar4 = tkinter.PanedWindow(orient="vertical")
        test_bar5 = tkinter.PanedWindow(orient="vertical")
        test_bar6 = tkinter.PanedWindow(orient="vertical")
        lay.add(status_bar)
        lay.add(test_bar)
        test_bar.add(test_bar1)
        test_bar.add(test_bar2)
        test_bar.add(test_bar3)
        test_bar.add(test_bar4)
        test_bar.add(test_bar5)
        test_bar.add(test_bar6)

        current_bar = tkinter.PanedWindow(orient="horizontal")
        current_bar_left = tkinter.PanedWindow(orient="vertical")
        current_bar_left_up = tkinter.PanedWindow(orient="horizontal")
        current_bar_middle = tkinter.PanedWindow(orient="vertical")
        current_bar_right = tkinter.PanedWindow(orient="vertical")
        video_num_bar = tkinter.PanedWindow(orient="horizontal")
        log_bar = tkinter.PanedWindow(orient="horizontal")
        log_bar_left = tkinter.PanedWindow(orient="horizontal")
        log_bar_right = tkinter.PanedWindow(orient="vertical")
        log_bar_right_down = tkinter.PanedWindow(orient="horizontal")
        log_bar_right_up = tkinter.PanedWindow(orient="vertical")
        log_bar_right_up1 = tkinter.PanedWindow(orient="horizontal")
        log_bar_right_up2 = tkinter.PanedWindow(orient="horizontal")
        log_bar_right_up3 = tkinter.PanedWindow(orient="horizontal")
        log_bar_right_up4 = tkinter.PanedWindow(orient="horizontal")
        log_bar_right_up5 = tkinter.PanedWindow(orient="horizontal")
        # log_bar_right_up5_checkbox = tkinter.PanedWindow(orient="horizontal")
        lay.add(current_bar)
        current_bar.add(current_bar_left)
        current_bar_left.add(current_bar_left_up)
        current_bar.add(current_bar_middle)
        current_bar.add(current_bar_right)
        lay.add(log_bar)
        log_bar.add(log_bar_left)
        log_bar.add(log_bar_right)
        log_bar_right.add(log_bar_right_up)
        log_bar_right.add(log_bar_right_down)
        log_bar_right_up.add(log_bar_right_up1)
        log_bar_right_up.add(log_bar_right_up2)
        log_bar_right_up.add(log_bar_right_up3)
        log_bar_right_up.add(log_bar_right_up4)
        log_bar_right_up.add(log_bar_right_up5)
        # log_bar_right_up5.add(log_bar_right_up5_checkbox)

        # 测试栏
        self.locl_detect_btn = Button(test_bar1, text="本地检测", font='等线', command=self.locl_detect)
        self.remt_detect_btn = Button(test_bar2, text="远程检测", font='等线', command=self.remt_detect)
        self.down_remote_btn = Button(test_bar3, text="下载远程文件_num", font='等线', command=self.down_remote)
        self.local_decry_btn = Button(test_bar4, text="本地解密测试_num", font='等线', command=self.local_decry)
        self.send_remote_btn = Button(test_bar5, text="发送至远程_num", font='等线', command=self.send_remote)

        test_bar1.add(self.locl_detect_btn)
        test_bar2.add(self.remt_detect_btn)
        test_bar3.add(self.down_remote_btn)
        test_bar4.add(self.local_decry_btn)
        test_bar5.add(self.send_remote_btn)
        self.locl_detect_ety = Entry(test_bar1, bd=2)
        self.remt_detect_ety = Entry(test_bar2, bd=2)
        self.down_remote_ety = Entry(test_bar3, bd=2)
        self.local_decry_ety = Entry(test_bar4, bd=2)
        self.send_remote_ety = Entry(test_bar5, bd=2)
        test_bar1.add(self.locl_detect_ety)
        test_bar2.add(self.remt_detect_ety)
        test_bar3.add(self.down_remote_ety)
        test_bar4.add(self.local_decry_ety)
        test_bar5.add(self.send_remote_ety)

        self.current_window_lab = Label(current_bar_left_up, text='批处理进度', justify=LEFT)
        self.current_video_lab = Label(current_bar_left_up, text='视频号', justify=LEFT)
        self.current_1_lab = Label(current_bar_left_up, text='文件类别', justify=LEFT)
        self.current_2_lab = Label(current_bar_left_up, text='合成情况', justify=LEFT)
        self.current_3_lab = Label(current_bar_left_up, text='解密情况', justify=LEFT)
        self.current_4_lab = Label(current_bar_left_up, text='远程源文件删除', justify=LEFT)
        self.current_5_lab = Label(current_bar_left_up, text='本地缓存删除', justify=LEFT)
        self.current_window_txt = Text(current_bar_left, bd=2, height=10, width=70, font=('等线', 12))
        current_bar_left_up.add(self.current_window_lab)
        current_bar_left_up.add(self.current_video_lab)
        current_bar_left_up.add(self.current_1_lab)
        current_bar_left_up.add(self.current_2_lab)
        current_bar_left_up.add(self.current_3_lab)
        current_bar_left_up.add(self.current_4_lab)
        current_bar_left_up.add(self.current_5_lab)
        current_bar_left.add(self.current_window_txt)
        self.test_1 = Button(current_bar_right, bd=2, height=1)
        self.test_2 = Button(current_bar_right, bd=2, height=1)
        self.open_localt_btn = Button(current_bar_right, text="打开本地缓存目录", font='等线', command=self.open_localt)
        self.delt_lcl_fl_btn =Button(current_bar_right, text="删除本地_成品所有", font='等线', command=self.delt_lcl_fl)
        current_bar_right.add(self.open_localt_btn)
        current_bar_right.add(self.delt_lcl_fl_btn)
        current_bar_right.add(self.test_1)
        current_bar_right.add(self.test_2)

        # video lst
        self.video_lst_lab = Label(current_bar_middle, text='视频列表', font=('等线', 16))
        self.video_lst = Text(current_bar_middle, bd=2, height=4, width=20, font=('等线', 12))
        current_bar_middle.add(self.video_lst_lab)
        current_bar_middle.add(self.video_lst)
        # log
        self.log_window_txt = Text(log_bar_left, bd=2, height=10, width=70, font=('等线', 12))
        log_bar_left.add(self.log_window_txt)

        # self.config_txt = Text(log_bar_right, width=20, height=8)
        self.config_local_detects_lab = Label(log_bar_right_up1, text='本地缓存目录', font='等线')
        self.config_remote_source_lab = Label(log_bar_right_up2, text='远程源目录', font='等线')
        self.config_remot_storage_lab = Label(log_bar_right_up3, text='远程存储目录', font='等线')
        self.config_adbs_location_lab = Label(log_bar_right_up4, text='adb目录', font='等线')
        self.config_combine_strip_lab = Label(log_bar_right_up4, text='子合并步幅')
        self.config_temp_location_lab = Label(log_bar_right_up5, text='缓存文件名', font='等线')
        self.config_local_tempory_ety = Entry(log_bar_right_up1)
        self.config_remote_source_ety = Entry(log_bar_right_up2)
        self.config_remot_storage_ety = Entry(log_bar_right_up3)
        self.config_adb_locations_ety = Entry(log_bar_right_up4)
        self.config_combine_strip_ety = Entry(log_bar_right_up4, width=2)
        self.config_temp_location_ety = Entry(log_bar_right_up5)
        self.source_file_delete_check = Checkbutton(log_bar_right_up5, text='仅保留回传文件', variable=self.source_file_delete)
        log_bar_right_up1.add(self.config_local_detects_lab)
        log_bar_right_up2.add(self.config_remote_source_lab)
        log_bar_right_up3.add(self.config_remot_storage_lab)
        log_bar_right_up4.add(self.config_adbs_location_lab)
        log_bar_right_up5.add(self.config_temp_location_lab)
        log_bar_right_up1.add(self.config_local_tempory_ety)
        log_bar_right_up2.add(self.config_remote_source_ety)
        log_bar_right_up3.add(self.config_remot_storage_ety)
        log_bar_right_up4.add(self.config_adb_locations_ety)
        log_bar_right_up4.add(self.config_combine_strip_lab)
        log_bar_right_up4.add(self.config_combine_strip_ety)
        log_bar_right_up5.add(self.config_temp_location_ety)
        log_bar_right_up5.add(self.source_file_delete_check)

        self.refresh_config_btn = Button(log_bar_right_down, text='修改配置', width=8,  command=self.edit_config)
        self.start_btn = Button(log_bar_right_down, text='开始批处理', command=self.start)
        # log_bar_right.add(self.config_txt)
        log_bar_right_down.add(self.refresh_config_btn)
        log_bar_right_down.add(self.start_btn)

    def config_full_path(self, relative_path):
        # print('临时切换进入')
        if not os.path.exists(relative_path):
            os.mkdir(relative_path)
        os.chdir(relative_path)
        full_path = os.getcwd()
        os.chdir(self.currwork_folder_full)
        # print('临时切换返回')
        return full_path

    def init_variable(self):
        # config 区域填充
        self.currwork_folder_full = os.getcwd()
        self.config_local_tempory_ety.insert('insert', cfg_local_temp_folder)
        self.config_remote_source_ety.insert('insert', cfg_remote_source_folder)
        self.config_remot_storage_ety.insert('insert', cfg_remote_storage_folder)
        self.config_adb_locations_ety.insert('insert', cfg_adb_tool_location)
        self.config_combine_strip_ety.insert('insert', cfg_cmb_strip)
        self.config_temp_location_ety.insert('insert', cfg_temp_file)
        # 绝对属性修改
        self.config_local_tempory_full = self.config_full_path(cfg_local_temp_folder).__str__()
        self.config_adb_locations_full = self.config_full_path(cfg_adb_tool_location).__str__()

        self.video_lst.insert("insert", '本区域暂未启用\n\n@Kisses_φ物')

        # 测试区域填充
        self.init_test_bar()
        if cfg_delete_fl:
            self.source_file_delete_check.select()

    def init_test_bar(self):
        # self.locl_detect_ety.
        self.locl_detect_ety.delete(0, 100)
        self.remt_detect_ety.delete(0, 100)
        self.locl_detect_ety.insert('insert', self.config_local_tempory_ety.get())
        self.remt_detect_ety.insert('insert', self.config_remote_source_ety.get())
        # self.send_remote_ety.insert('insert', )
        self.print_out('测试栏配置信息已更新:')
        self.print_config()

    def current_window_listen(self):
        """监听 解密线程信息"""
        while t1_downs_q.qsize() or t3_send.is_alive():
            # self.current_window_txt.delete('1.0',)
            self.current_window_txt.insert("end", '\n\n\n')
            # self.current_window_txt.insert("end", print_out_thod(data_notice))
            self.current_window_txt.insert("end", main_decry_info.get())
            self.current_window_txt.see(END)
        self.current_window_txt.insert("end", '批处理完成_结束, 如需运行批出还需本程序再关闭后重新打开')

    def __decry_info_threading(self):
        while True:  # TODO: 后续改进为 解密时启动
            dct = queue_info.get()
            info = f"[{dct['file_num']}] {dct['file_state']} {dct['解密情况']} {dct['合并情况']} {dct['最终情况']} {dct['其他情况']}"
            self.print_out(info)

    def decry_info_threading(self):
        t = threading.Thread(target=self.__decry_info_threading)
        t.start()

    def print_out(self, string, *args):
        string = str(string)
        for i in args:
            string += str(i)
        self.log_window_txt.insert("end", string)
        self.log_window_txt.insert("end", "\n")
        self.log_window_txt.see(END)

    def locl_detect(self):
        if not self.locl_detect_ety.get():
            self.print_out('本地检测 参数为空!')
            return
        self.print_out('本地检测:', self.locl_detect_ety.get(), ': ', ' '.join(local_fold_detect(self.config_local_tempory_full)))

    def remt_detect(self):
        if not self.remt_detect_ety.get():
            self.print_out('远程检测 参数为空!')
            return
        self.print_out('远程检测', self.remt_detect_ety.get(), ':',
                       ' '.join(remote_fold_detect(self.remt_detect_ety.get(), self.config_adb_locations_full)))

    def __down_remote(self):
        if not self.down_remote_ety.get():
            self.print_out('远程下载 参数为空!')
            return
        self.print_out(f'远程下载{self.down_remote_ety.get()} 请等待提示完成')
        self.print_out(f'远程下载{self.down_remote_ety.get()}', self.down_remote_ety.get(), ':',  # return '完成'
                       download_adb_folder(os.path.join(self.config_remote_source_ety.get(), self.down_remote_ety.get()),
                                           self.config_local_tempory_full, self.config_adb_locations_full, self.config_temp_location_ety.get()))

    def down_remote(self):
        t = threading.Thread(target=self.__down_remote)
        t.start()

    def __local_decry(self):
        if not self.local_decry_ety.get():
            self.print_out('本地解密 参数为空!')
            return
        self.print_out('本地解密', self.local_decry_ety.get(), ':',
                       )
        video_num = decry_obj(os.path.join(self.config_local_tempory_full, self.local_decry_ety.get()), self.source_file_delete.get(), self.config_combine_strip_ety.get())
        video_num.main_decry()

    def local_decry(self):
        t = threading.Thread(target=self.__local_decry)
        t.start()

    def send_remote(self):
        if not self.send_remote_ety.get():
            self.print_out('发送远程 参数为空!')
            return
        self.print_out('发送远程', self.send_remote_ety.get(), ':',
                       upload_adb(os.path.join(self.config_local_tempory_full, self.send_remote_ety.get(),), self.config_remot_storage_ety.get(), self.config_adb_locations_full))

    def __open_localt(self):
        self.print_out('打开本地文件夹', self.config_local_tempory_full)
        os.system('explorer.exe ' + self.config_local_tempory_full)

    def open_localt(self):
        t = threading.Thread(target=self.__open_localt)
        t.start()

    def delt_lcl_fl(self):
        self.print_out('删除本地文件',  ":",
                       delete_local_temp(self.config_local_tempory_full))

    def change_state_config(self, state):
        """切换配置区域状态"""
        if not state:
            self.config_local_tempory_ety.configure(state='readonly')
            self.config_remote_source_ety.configure(state='readonly')
            self.config_remot_storage_ety.configure(state='readonly')
            self.config_adb_locations_ety.configure(state='readonly')
            self.config_temp_location_ety.configure(state='readonly')
            self.config_combine_strip_ety.configure(state='readonly')
            self.source_file_delete_check.configure(state='disable')
            self.config_adbs_location_lab.configure(state='disable')
            self.config_combine_strip_lab.configure(state='disable')
            self.config_local_detects_lab.configure(state='disable')
            self.config_remot_storage_lab.configure(state='disable')
            self.config_remote_source_lab.configure(state='disable')
            self.config_temp_location_lab.configure(state='disable')
        else:
            self.config_local_tempory_ety.configure(state='normal')
            self.config_remote_source_ety.configure(state='normal')
            self.config_remot_storage_ety.configure(state='normal')
            self.config_adb_locations_ety.configure(state='normal')
            self.config_temp_location_ety.configure(state='normal')
            self.config_combine_strip_ety.configure(state='normal')
            self.source_file_delete_check.configure(state='active')
            self.config_adbs_location_lab.configure(state='normal')
            self.config_combine_strip_lab.configure(state='normal')
            self.config_local_detects_lab.configure(state='normal')
            self.config_remot_storage_lab.configure(state='normal')
            self.config_remote_source_lab.configure(state='normal')
            self.config_temp_location_lab.configure(state='normal')

    def print_config(self):
        self.print_out(f"""更新已有配置:
        {'本地缓存目录:':10}{self.config_local_tempory_full}
        {'远端源目录:':10}{cfg_remote_source_folder}
        {'远端回传目录:':10}{cfg_remote_storage_folder}
        {'adb工具目录:':10}{self.config_adb_locations_full}
        {'子合并步幅:':10}{self.config_combine_strip_ety.get()}
        {'缓存文件:':10}{cfg_temp_file}""")

    def store_config(self):
        """保存并切换至保存按钮"""
        self.config_local_tempory_full = self.config_full_path(self.config_local_tempory_ety.get())
        self.config_adb_locations_full = self.config_full_path(self.config_adb_locations_ety.get())

        self.init_test_bar()
        change_config_file(self.config_local_tempory_ety.get(), self.config_remote_source_ety.get(),
                           self.config_remot_storage_ety.get(), self.config_adb_locations_ety.get(),
                           self.config_temp_location_ety.get(), str(self.source_file_delete.get()), self.config_combine_strip_ety.get())
        self.change_state_config(False)
        self.refresh_config_btn.configure(text='修改配置', bg='#f0f0f0', command=self.edit_config)

    def edit_config(self):
        """切换配置"""
        os.chdir(self.currwork_folder_full)
        self.change_state_config(True)
        self.refresh_config_btn.configure(text='保存', bg='#499c54', command=self.store_config)

    def __start(self):
        main_multi_thread(self.config_local_tempory_full, self.config_remote_source_ety.get(),
                          self.config_remot_storage_ety.get(), self.config_adb_locations_full,
                          self.config_temp_location_ety.get(), self.source_file_delete.get(), self.config_combine_strip_ety.get())

        self.current_window_listen()

    def start(self):  # TODO: start 处理时检测 __start()内flag, 若为1 则start的功能为停止
        t = threading.Thread(target=self.__start)
        t.start()

def gui_start():
    tk_main = Tk()
    UI_obj = merge_UI(tk_main)
    os.chdir('.')
    # print(os.system('chdir'))
    UI_obj.set__windows()      # 设置窗口组件
    UI_obj.init_variable()  # 初始化窗口默认值
    UI_obj.change_state_config(False)
    UI_obj.decry_info_threading()  # 监听decry_core模块的信息

    tk_main.mainloop()

gui_start()
