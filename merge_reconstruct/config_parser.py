# 解析配置文件
import configparser
import os
config_file_name ='merge_config.ini'

def detect_configure_file():
    try:
        f = open(config_file_name, 'r', encoding='utf-8')
        f.close()
    except Exception as E:
        if "No such file" in str(E):
            print('尝试新建')
            change_config_file(".\\okfun\\", "/storage/emulated/0/okfun/v/",
                               "/storage/emulated/0/okfun/", ".\\adb-tools\\",
                               ".\\transh.txt", "True", "400")

        else:
            print('配置文件异常, 已尝试新建:', E)

def change_config_file(a, b, c, d, e, ff, gg):
    with open('.\\' + config_file_name, 'w', encoding='utf-8') as f:
        f.write(f"""[location]
local_temp_folder = {a}
remote_source_folder = {b}
remote_storage_folder = {c}
adb_tool_location = {d}

[file]
temp_file = {e}
deleted_temp_file = {ff}
combine_strip = {gg}""")

detect_configure_file()
con = configparser.ConfigParser()
con.read(config_file_name, encoding='utf-8')

cfg_remote_source_folder = con['location']['remote_source_folder']
cfg_local_temp_folder = con['location']['local_temp_folder']
cfg_remote_storage_folder = con['location']['remote_storage_folder']
cfg_adb_tool_location = con['location']['adb_tool_location']
cfg_temp_file = con['file']['temp_file']
cfg_delete_fl = True if con['file']['deleted_temp_file'] == 'True' else False
cfg_cmb_strip = con['file']['combine_strip']
