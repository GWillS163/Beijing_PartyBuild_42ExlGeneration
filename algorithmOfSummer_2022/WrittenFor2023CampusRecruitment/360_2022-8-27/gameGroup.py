#  Author : Github: @GWillS163
#  Time: $(Date)
# 最近一款吃鸡类型的游戏火爆全球。在组队模式下，你可以邀请自己的好友组建自己的小队，
# 并选择是否填充（是否同意和非好友游玩），然后加入游戏。
# 现在有A个单人队伍，B个双人队伍，C个三人队伍，D个四人队伍，
# 并且全都同意填充，但已有的多人队伍的队员不能被拆开填充到其他队伍，
# 请问最多能组成多少个四人队伍。

# 输入描述
# 第一行一个正整数T，表示数据组数。（1≤T≤100）
#
# 接下来T行，每行四个非负整数，A，B，C，D。（0≤A, B, C, D≤150）
#
# 输出描述
# 共T行，每行输出一个队伍数。

# 样例输入
# 4
# 1 2 3 4  # 已经有了4个4人队伍，2个2人队伍可以组成1个4人队伍， 3个3人队伍可以组成1个4人队伍
# 4 3 2 1  # 1 人队伍可以填充，3*2 = 6, 再+2*1 = 2个队伍； 2*3 = 6 再+2*1 = 2个队伍
# 2 2 2 1  # D:1个， B:1个， C:2*3=6 , 6+2=8. 共4个队伍
# 0 2 0 1  # D:1个，B:1个
# 样例输出
# 6
# 5
# 4
# 2



# nums = int(input())
inputs = []
#
# for _ in range(nums):
#     a, b, c, d = map(int, input().split())
#     inputs.append([a, b, c, d])


strs = """1 2 3 4
4 3 2 1
2 2 2 1
0 2 0 1"""
inputs2 = "4 3 2 1"

for row in strs.split('\n'):
    inputs.append(list(map(int, row.split())))


for comb in inputs:
    teamNum = 0
    teamNum += comb[3]

    bNeed = comb[1] * 2
    cNeed = comb[2] * 1

    # use A to fill B, C team
    while comb[0]:
        if cNeed:
            cNeed -= 1
            comb[0] -= 1
            teamNum += 1
        elif bNeed:
            bNeed -= 2
            comb[0] -= 2
            teamNum += 1
        else:
            break

    if comb[1]:
        teamNum += comb[1]//2

    print(teamNum)
