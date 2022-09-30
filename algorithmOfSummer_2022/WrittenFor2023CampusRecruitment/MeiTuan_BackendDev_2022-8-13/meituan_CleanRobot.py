#  Author : Github: @GWillS163
#  Time: $(Date)


# n, m, k = [int(i) for i in input().split()]  # n>=2, m<= 100
# command = input()
from pprint import pprint

n, m, k = 2, 3, 5
command = "DDDSAASSSSS"

mapp = [[0 for i in range(m)]
        for j in range(n)]
move = {
    "W": [-1, 0],
    "S": [1, 0],
    "A": [0, -1],
    "D": [0, 1]
}

no_of_cleaned = n * m -1
which_stop = -1

coord = [0, 0]
mapp[0][0] = 1
for i, c in enumerate(command):
    if not no_of_cleaned:
        which_stop = i
        break
    coord[0] += move[c][0]
    coord[1] += move[c][1]

    # make border check
    if coord[0] < 0:
        coord[0] = 0
    if coord[1] < 0:
        coord[1] = 0
    if coord[0] >= n:
        coord[0] = n - 1
    if coord[1] >= m:
        coord[1] = m - 1

    if mapp[coord[0]][coord[1]] == 0:
        no_of_cleaned -= 1
        mapp[coord[0]][coord[1]] = 1  # make as cleaned

# for row in mapp:
#     print(row)  # testScripts
    # for tile in row:
    #     if tile != 1:
    #         no_of_cleaned += 1

if no_of_cleaned:
    print("no")
    print(no_of_cleaned)
else:
    print("yes")
    print(which_stop)