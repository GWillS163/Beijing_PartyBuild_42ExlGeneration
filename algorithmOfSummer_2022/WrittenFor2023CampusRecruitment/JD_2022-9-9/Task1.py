#  Author : Github: @GWillS163
#  Time: $(Date)
# import sys
# for line in sys.stdin:
#     a = line.split()
#
#
# import sys
# if __name__ == "__main__":
#     # 读取第一行的n
#     n = int(sys.stdin.readline().strip())
#     ans = 0
#     for i in range(n):
#         # 读取每一行
#         line = sys.stdin.readline().strip()
#         # 把每一行的数字分隔后转化成int列表
#         values = list(map(int, line.split()))
#         for v in values:
#             ans += v
#     print(ans)


def solution(inputs):
    last = None
    count = 0
    for char in inputs:
        if char != last:
            last = char
            continue
        count += 1
        last = None
    print(count)


if __name__ == '__main__':
    testCase = ["rede", "rredd", "rrdd", "rreedd",
                "reedddee", "reeddee", "reedd", "reed", "ree", "re"
                "rreeedd", "rreeeedd", "rreeeeedd", "rreeeeeedd",
                "rreeeeeeedd", "rreeeeeeeedd", "rreeeeeeeeedd", "rreeeeeeeeeedd",
                ]
    for case in testCase:
        print( case, end=": ")
        solution(case)