#  Author : Github: @GWillS163
#  Time: $(Date)

def solution(num: int):
    print(num)
    remain = 1
    # for n in range(num, 0, -1):
    #     print(n)

    # print all combination of num, use recursion
    for n in range(num, 0, -1):
        remain += recursion(n)
    return remain


def recursion(num: int):
    if num == 1:
        return 1
    else:
        return num + recursion(num - 1)


if __name__ == '__main__':
    solution(4)
