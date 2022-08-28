#  Author : Github: @GWillS163
#  Time: $(Date)

nums = int(input())
res = []
for _ in range(nums):
    name = input()
    if name and len(name) > 10:
        continue
    if all(letter.isalpha() for letter in name):
        res.append(name)
print(len(res))
