#  Author : Github: @GWillS163
#  Time: $(Date)

def quickSelectionSort(arr):
    for i in range(len(arr)):
        minIndex = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[minIndex]:
                minIndex = j
        arr[i], arr[minIndex] = arr[minIndex], arr[i]
    return arr


if __name__ == '__main__':
    print(quickSelectionSort([8, 3, 5, 4, 2, 6]))
    # 首先在未排序序列中找到最小（大）元素，存放到排序序列的起始位置。
    #
    # 再从剩余未排序元素中继续寻找最小（大）元素，然后放到已排序序列的末尾。
    #
    # 重复第二步，直到所有元素均排序完毕。
