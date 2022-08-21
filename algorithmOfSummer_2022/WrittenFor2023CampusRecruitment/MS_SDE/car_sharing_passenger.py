#  Author : Github: @GWillS163
#  Time: $(Date)
from pprint import pprint


def solution(A=[0, 1, 1], B=[1, 2, 3]):
    pathDct = {}
    cost_passengerDct = {}
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
    for roots in pathDct[0]:
        cost_passengerDct[roots] = recursionSumTree(pathDct, roots, [0])
    return sum([roots[0] for roots in cost_passengerDct.values()])


def recursionSumTree(pathDct, root, visited):
    if root in visited:
        return [0, []]
    visited.append(root)
    passengers = [root]
    cost = 0
    if len(pathDct[root]) == 1:
        return [1, [root]]
    else:
        for node in pathDct[root]:
            leafCost, leafPassenger = recursionSumTree(pathDct, node, visited)
            cost += leafCost
            passengers += leafPassenger

        cost += 1 if not len(passengers) > 4 else len(passengers) // 4 + 1
    return [cost, passengers]


if __name__ == '__main__':
    print(solution())
    print(solution([1, 9, 9, 9, 9],
                   [0, 1, 6, 5, 4]))
    print(solution([1, 1, 1, 9, 9, 9, 9, 7, 8],
                   [2, 0, 3, 1, 6, 5, 4, 0, 0]))

