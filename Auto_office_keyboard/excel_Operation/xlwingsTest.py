#  Author : Github: @GWillS163
#  Time: $(Date)


# 导入xlwings，并起一个别名 xw，方便操作
import xlwings as xw

# 1、创建一个app应用，打开Excel程序
# visible=True 表示打开操作Excel过程可见 初次接触可以设置为True，了解其过程
# add_book=False 表示启动app后不用新建个工作簿
app = xw.App(visible=True, add_book=False)

# 2、新建一个工作簿
wb = app.books.add()

# 3、新建一个sheet，并操作
# 3.1 新建sheet 起名为first_sht
sht = wb.sheets.add('first_sht')
# 3.2 在新建的sheet表中A1位置插入一个值：简说Python
sht.range('A1').value = '简说Python'
# 3.3 保存新建的工作簿，并起一个名字
wb.save('xlwings_wb.xlsx')

# 4、关闭工作簿
wb.close()

# 5、程序运行结束，退出Excel程序
app.quit()