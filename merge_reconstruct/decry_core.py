# 主要提供解密函数
# 把所有回显 都使用print_in 输出到all_in_one 打印所有信息, 并放入队列内部
# 回显的str字符串 与判断要相分离.
import os, re, time
import shutil
import threading

from operate_tools import file_re, get_file_binary
from Crypto.Cipher import AES
from queue import Queue
queue_info = Queue()

class decry_obj():
    def __init__(self, video_path, is_delete_other_file=True, strip=400):
        self.processing = True
        self.video_numb = video_path.split("\\")[-1]  # 22043
        self.video_path = video_path  # D:\okfun\22043
        self.folde_path = video_path.strip(self.video_numb)  # D:\okfun\
        self.merge_fold = self.video_path + '_temp'  # D:\python_scripts\merge_reconstruct\22043
        self.key_crypto = ''
        self.files_inte = True  # booleen
        self.scan_files_list = ''
        self.m3u8_files_list = ''
        self.all_in_one = {'file_num': self.video_numb,
                           'file_state': '',
                           '解密情况': '',
                           '合并情况': '',
                           '最终情况': '',
                           '其他情况': '',
                           }
        self.is_delete_other_file = is_delete_other_file
        self.strip = int(strip)

    def detect_file_full(self):
        """检查文件整体问题
        """
        # 判断两个关键文件是否存在
        key_path = os.path.join(self.video_path, 'key')
        m3u8_pth = os.path.join(self.video_path, 'index.m3u8')
        k = os.path.exists(key_path)
        m = os.path.exists(m3u8_pth)
        if not(k and m):  # 若不存在
            self.files_inte = False
            self.print_in('file_state', '核心文件缺少')
            self.print_in('最终情况', '核心文件缺少')
            return
        # 判断分片长度
        m3u8_file = get_file_binary(m3u8_pth).decode('utf-8')
        self.m3u8_files_list = re.findall(self.video_numb + '/(.*)\n', m3u8_file)[1:]  # 索引文件参考分片
        self.scan_files_list = file_re(self.video_path, '^[^\.]{6,18}$')  # 实际文件分片
        if len(self.m3u8_files_list) == len(self.scan_files_list):
            self.files_inte = True
        else:
            self.files_inte = False
            self.print_in('file_state', '分片不合规')
            self.print_in('最终情况', '文件不完整')
            return
        self.print_in('file_state', '[文件正常]')
        return self.files_inte

    def get_key_crypto(self):
        key_path = os.path.join(self.video_path, 'key')
        self.key_crypto = AES.new(get_file_binary(key_path), AES.MODE_CBC)

    def single_decry(self, single_paths):
        """单个文件的解密"""
        source_data = get_file_binary(os.path.join(self.video_path, single_paths))
        decried_data = self.key_crypto.decrypt(source_data)
        with open(os.path.join(self.merge_fold, single_paths + '.ts'), 'ab') as file:
            file.write(decried_data)
        # TODO:临时屏蔽

    def __print_out(self):
        """输出实例"""
        print('开始监听')
        while self.processing:
            while queue_info.qsize():
                dct = queue_info.get()
                print(f"{dct['file_num']} {dct['file_state']} {dct['解密情况']} {dct['合并情况']} {dct['最终情况']} {dct['其他情况']}")

    def print_out(self):
        t = threading.Thread(target=self.__print_out)
        t.start()

    def ts_combine(self, lst):
        """进行批量合并 递归本函数处理"""
        os.chdir(self.merge_fold)
        self.all_in_one['合并情况'] = '合成中'
        self.ts_combine_core(lst)
        # copy_lst_str = '+'.join([i + '.ts' for i in lst[0:strip]])  # cmd 单条命令大长度为 8191 个,
        # self.merge_res = os.popen(f"copy /b {copy_lst_str} {self.video_path}_over.ts")
        # if lst[strip:]:
        #     self.ts_combine(lst[strip:], strip)



    def ts_combine_core(self, lst, strip='over'):
        """递归合成文件"""
        if len(lst) < self.strip + 1:
            if strip == 'over':
                copy_lst_str = '+'.join(lst)
                self.merge_res = os.popen(f"copy /b {copy_lst_str} {self.video_path}_over.ts").read()
                self.print_in('解密情况', f'总合成中')
                return '[总合成完毕]'
            else:
                copy_lst_str = '+'.join([i + '.ts' for i in lst])
                self.merge_res = os.popen(f"copy /b {copy_lst_str} {self.video_numb}_sub{strip}.ts").read()
                self.print_in('解密情况', f'合成中:{strip}')
                self.merge_res = f'合成子分片{strip}'
                return f'{self.video_numb}_sub{strip}.ts'
        else:
            combine_lst = []
            for strip in range(0, len(lst), self.strip):
                slip_res = self.ts_combine_core(lst[strip: strip+self.strip], str(strip))
                combine_lst.append(slip_res)
            self.ts_combine_core(combine_lst, strip='over')

        # if len(lst) < self.strip + 1:
        #     copy_lst_str = '+'.join([i + '.ts' for i in lst])
        #     self.merge_res = os.popen(f"copy /b {copy_lst_str} {self.video_numb}_over.ts").read()
        #     self.print_in('解密情况', f'合成中:{self.strip}')
        #     return '[总合成完毕]'
        # else:
        #     sub_combine_lst = []
        #     for num in range(0, len(lst), self.strip):
        #         for x in lst[num:num+self.strip]:
        #             copy_lst_str = '+'.join([i + '.ts' for i in x])
        #             self.merge_res = os.popen(f"copy /b {copy_lst_str} {self.video_numb}_sub{num}.ts").read()
        #             self.print_in('解密情况', f'合成中:{self.strip}')
        #         sub_combine_lst.append(f'{self.video_numb}_sub{num}.ts')
        #     all_copy_lst_str = '+'.join(sub_combine_lst)
        #     self.merge_res = os.popen(f"copy /b {all_copy_lst_str} {self.video_numb}_over.ts").read()
        #     self.print_in('解密情况', f'合成中:{self.strip}')

    def print_in(self, str, info):
        """把输出放入字典 并一起放到队列"""
        self.all_in_one[str] = info
        queue_info.put(self.all_in_one)

    def main_decry(self):
        # 检查文件完整性, key, m3u8, 分片数量
        # self.print_out()
        self.detect_file_full()
        if self.files_inte:
            self.get_key_crypto()
            # 遍历解密
            os.chdir(self.folde_path)
            os.makedirs(self.merge_fold, exist_ok=True)
            end_file = self.m3u8_files_list[-1].strip("index")
            for single_file in self.m3u8_files_list:
                self.print_in('解密情况', f'解密中:{single_file}/{end_file}')
                self.single_decry(single_file)
            self.print_in('解密情况', f'[解密完成]')
            # 合并合成
            self.print_in('合并情况', f'开始合并')
            self.ts_combine(self.m3u8_files_list)
            self.print_in('合并情况', '[合并完成]' if ('copied' in self.merge_res or '已复制' in self.merge_res) else '合并失败!' + self.merge_res)
            # self.print_in('合并情况', self.merge_res)

            # 删除缓存文件
            if self.all_in_one['合并情况'] == '[合并完成]':
                os.chdir(self.folde_path)
                shutil.rmtree(self.merge_fold)
                try:
                    if self.is_delete_other_file:
                        shutil.rmtree(self.video_numb)
                except Exception as E:
                    self.print_in('合并情况', f'尝试移除缓存时出现了问题:{E}')
            self.print_in('最终情况', '[合成完毕,请打开目录检查]')  # 字符串不要乱动
            self.processing = False

if __name__ == '__main__':
    a = decry_obj(r'D:\python_scripts\merge_reconstruct\22043')
    a.main_decry()
# TODO: 本地模式