#  Author : Github: @GWillS163
#  Time: $(Date)
import portion
scope = [[0, 20], [50, 100], [200, 1000]]
param = [21, 70, 202, -500]
ran = 2


def union_list(a, b):
    return a + b


def difference_list(scope, integer, ran=2):
    low = abs(integer) - ran
    high = abs(integer) + ran
    # situation 1, low and high are in the scope both
    if low > scope[0] and high < scope[1]:
        return [scope[0], low], [high, scope[1]]

    # situation 2, one para large equals border, the other is unknown
    elif low == scope[0] or high == scope[1]:
        if low == scope[0]:
            if high >= scope[1]:  # [low, high] == [scope[0], scope[1]]
                return []
            else:
                scope[1] = high  # low [scope[0], high]
        elif high == scope[1]:
            if low <= scope[0]:  # low [low, high] == [scope[0], scope[1]]
                return []
            else:
                scope[0] = low   # [scope[0], low, high]
        return scope
    # situation 3, only 1 para is in the scope: []high  low[]
    elif (scope[0] <= high <= scope[1]) or (scope[1] >= low >= scope[0]):
        if scope[0] <= high <= scope[1]:
            scope[0] = high
        elif scope[1] >= low >= scope[0]:
            scope[1] = low
        return scope

    # situation 4, no para is in the scope
    elif low >= scope[1] or high <= scope[0]:
        return scope

    return -1


if __name__ == '__main__':
    print(difference_list([200, 1000], -198), difference_list([200, 1000], -198) == [200, 1000])
    print(difference_list([200, 1000], -201), difference_list([200, 1000], -201) == [203, 1000])
    print(difference_list([200, 1000], -500) == ([200, 498], [502, 1000]))
    print(difference_list([200, 1000], -997) == ([200, 995], [999, 1000]))
    # print(x, x == [200, 998],lambda x:difference_list([200, 1000], -997))
    print(difference_list([200, 1000], -1002), difference_list([200, 1000], -1002) == [200, 1000])
    print(difference_list([200, 1000], -1003), difference_list([200, 1000], -1003) == [200, 1000])