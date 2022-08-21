#  Author : Github: @GWillS163
#  Time: $(Date)
from pprint import pprint


def solution(A=[0, 1, 1], B=[1, 2, 3]):
    pathDct = {}
    costDct = {}
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
        costDct[roots] = recursionSumTree(pathDct, roots, [])
    return sum(costDct.values())


def recursionSumTree(pathDct, node, visited):
    if node in visited:
        return 0
    visited.append(node)
    cost = 0
    if len(pathDct[node]) == 1:
        cost = 1
    else:
        for node in pathDct[node]:
            cost += recursionSumTree(pathDct, node, visited)
    return cost


if __name__ == '__main__':
    print(solution())
    print(solution([1, 1, 1, 9, 9, 9, 9, 7, 8],
                    [2, 0, 3, 1, 6, 5, 4, 0, 0]))
