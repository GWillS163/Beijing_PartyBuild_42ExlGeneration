from tkinter import *
root = Tk()
li = ['C', 'python', 'php', 'html', 'SQL', 'java']
movie = ['CSS', 'jQuery', 'Bootstrap']

listb = Listbox(root)  # 创建两个列表组件
listb2 = Listbox(root)
ok = Button(root)
cancel = Button(root)
can = Canvas(root)

for item in li:  # 第一个小部件插入数据
    listb.insert(0, item)
for item in movie:  # 第二个小部件插入数据
    listb2.insert(0, item)
ok.widgetName = '完成'

listb.pack()  # 将小部件放置到主窗口中
listb2.pack()
ok.pack()
cancel.pack()

root.mainloop()  # 进入消息循环