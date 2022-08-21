#  Author : Github: @GWillS163
#  Time: $(Date)
from pprint import pprint


def solution(A=[0, 1, 1], B=[1, 2, 3]):
    pathDct = {}
    for a, b in zip(A, B):
        if a not in pathDct:
            pathDct[a] = [b]
        else:
            pathDct[a].append(b)
        if b not in pathDct:
            pathDct[b] = [a]
        else:
            pathDct[b].append(a)

    # pprint(pathDct)

    cost = 0
    for root in pathDct[0]:
        leafCost, leafPassenger = recurTreeSum(pathDct, root, [0])
        cost += leafCost
    return cost


def recurTreeSum(pathDct, root, visited):
    if root in visited:
        return [0, []]
    # print(pathDct[root])
    visited.append(root)
    passengers = []
    cost = 0
    if len(pathDct[root]) == 1:
        return [1, [root]]
    else:
        for node in pathDct[root]:
            leafCost, leafPassenger = recurTreeSum(pathDct, node, visited)
            cost += leafCost
            passengers += leafPassenger
        cost += len(passengers) // 4 + 1 if len(passengers) > 4 else 1
    return [cost, passengers]


if __name__ == '__main__':
    print(solution())
    print(solution([1, 1, 1, 9, 9, 9, 9, 7, 8],
                    [2, 0, 3, 1, 6, 5, 4, 0, 0]))
