#  Author : Github: @GWillS163
#  Time: $(Date)
from quickSort import quickSort


def bucketSort(arr):
    bucket = [[] for _ in range(len(arr))]
    for i in range(len(arr)):
        bucket[i].append(arr[i])
    for i in range(len(bucket)):
        bucket[i] = quickSort(bucket[i])
    result = []
    for i in range(len(bucket)):
        result += bucket[i]
    return result


if __name__ == '__main__':
    print(bucketSort([8, 3, 5, 4, 2, 6]))