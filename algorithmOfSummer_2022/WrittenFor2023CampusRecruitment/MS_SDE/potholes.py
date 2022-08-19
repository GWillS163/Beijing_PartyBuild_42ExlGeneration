#  Author : Github: @GWillS163
#  Time: $(Date)
# 给potholes的X,Y 坐标， W是压路机宽度，需要多少压路机
#
def solution(X, Y, W):
    # x = [2,3,4,2,4]
    # y = [3,2,4,2,4]
    # Y = 2
    attempt = 0
    sortedX = sorted(X, reverse=True)
    left = sortedX.pop()
    # right = sortedX[0]

    while sortedX:
        while sortedX:
            curr = sortedX.pop()
            if curr >= left+W:
                left = curr
                break
        attempt += 1
    return attempt


print(solution([2, 4, 2, 6, 7, 1],
               [0, 5, 3, 2, 1, 5], 2))
print(solution([0, 3, 6, 5],
               [0, 3, 2, 4], 1))
