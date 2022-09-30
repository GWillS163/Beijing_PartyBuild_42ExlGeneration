#  Author : Github: @GWillS163
#  Time: $(Date)

import csv
import time


def save2csv(lst, path):
    # get current time as file name
    fileName = time.strftime("输出结果%Y-%m-%d_%H%M%S", time.localtime())
    # save to csv
    with open(path+fileName+".csv", "w", newline="") as f:
        for row in lst:
            csv.writer(f).writerow(row)


save2csv([[1,2,3], [3,4,5]], "D:\\")
