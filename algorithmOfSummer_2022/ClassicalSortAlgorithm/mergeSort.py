from operator import eq
from typing import overload


def mergeSort(arr: list) -> list:
    if len(arr) < 2:
        return arr
    mid = len(arr) // 2
    left = mergeSort(arr[:mid])
    right = mergeSort(arr[mid:])
    return merge(left, right)


def merge(left, right):
    """
    gradually merge two sorted list, and return the sorted list
    :param left: like [1, 3, 5]
    :param right: like [4, 2, 6]
    :return: [1, 2, 3, 4, 5, 6]
    """
    result = []
    while left and right:
        if left[0] < right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))

    return result + left + right


if __name__ == '__main__':
    print(eq('srts', "srts"))
    print("srts".__eq__("srts"))