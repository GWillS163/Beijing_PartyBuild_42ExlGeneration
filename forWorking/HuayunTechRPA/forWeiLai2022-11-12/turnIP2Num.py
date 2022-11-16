# Github: GWillS163
# User: 駿清清 
# Date: 12/11/2022 
# Time: 13:08

# turn IP to binary number and plus it
import math


def turnIP2Num(ip):
    ipLst = ip.split(".")
    ipNum = 0
    for i in range(4):
        ipNum += int(ipLst[i]) * (256 ** (3 - i))
    return ipNum


def turnIp(addr):
    ips = [int(x) for x in addr.split('.')]
    return ips[0] << 24 | ips[1] << 16 | ips[2] << 8 | ips[3]


print(turnIP2Num("127.0.0.1"))
print(turnIp("127.0.0.1"))


# Calculate the number of combinations with nums and lens
def HowManyCombinations(nums, lens):
    return nums if lens == 1 else nums * HowManyCombinations(nums, lens - 1)


def HowManyCombinations2(nums, lens):
    return nums ** lens


def HowManyDifferentCombinations(nums: list, lens):
    return len(set(nums)) ** lens


# compare the two functions with the variables
for i in range(1, 10):
    for j in range(1, 10):
        print(f"{HowManyDifferentCombinations([1, 2, 3, 3, 5], j): ^10}", end=" ")
        # print(HowManyCombinations(i, j) == HowManyCombinations2(i, j), end=" ")
        print(f"{i}-{j}", end=" ")
        print(HowManyCombinations(i, j))
        # print(HowManyCombinations(i, j), HowManyCombinations2(i, j))
