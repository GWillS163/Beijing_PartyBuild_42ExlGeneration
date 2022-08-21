#  Author : Github: @GWillS163
#  Time: $(Date)

a = [4, 2, 2, 2]


# condition 1
# i < j < k

# condition 2
# a[i] - a[j] = 2 * a[j] - a[k]
res = 0
for i, n in enumerate(a):
    for j, m in enumerate(a):
        for k, l in enumerate(a):
            if i < j < k and n - m == 2 * m - l:
                # print(i+1, j+1, k+1)
                res += 1

print(res)