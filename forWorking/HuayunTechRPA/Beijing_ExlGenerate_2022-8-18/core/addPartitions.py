# Github: GWillS163
# User: 駿清清 
# Date: 16/11/2022 
# Time: 12:45
# 2022-11-16 更新内容: 新增参与率等

# placeBar 函数更改的部分 ： 新增了参与率三个单元格
# placeData 部分： 在插入数据的时候，将参与率的数据插入进去
from shtOperation import shtCopyTo


def addSht1Partitions(mdlSht1, partitionScp, sht1, insertPoint="A3"):

    insertRow = 2  # 自动获取
    # insert three rows
    sht1.insert_rows(3, 3)
    shtCopyTo(mdlSht1, partitionScp, sht1, insertPoint)

    sht1.insert_row(insertRow, values="参与率")
    sht1.insert_row(insertRow, values="总人数")
    sht1.insert_row(insertRow, values="参与数")

