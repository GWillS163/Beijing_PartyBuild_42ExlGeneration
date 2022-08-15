#  Author : Github: @GWillS163
#  Time: $(Date)

cubeNum, timesK = "6 4".split()
cubeNum = int(cubeNum)
timesK = int(timesK)
pi = [int(p) for p in "1 4 5 3 8 5 6".split()]

if not cubeNum and timesK and pi:
    res = input().split()
    cubeNum, timesK = int(res[0]), int(res[1])
    pi = [int(p) for p in input().split()]

res = [0] * timesK
theMax = 0

for i, p in enumerate(pi):
    isContinuous = False
    for r_i, r_n in enumerate(res):
        if p > r_n:
            res[r_i] = p
            min_index = r_i
            if res[0] >= p:
                res.pop(0)
                res.append(p)
                isContinuous = True
            else:
                isContinuous = False
            break

    if not isContinuous:
        stepMax = 0
        for r in res:
            stepMax += r

        if stepMax > theMax:
            theMax = stepMax
        res = [0] * timesK


stepMax = 0
for r in res:
    stepMax += r

if stepMax > theMax:
    theMax = stepMax
print(theMax)

