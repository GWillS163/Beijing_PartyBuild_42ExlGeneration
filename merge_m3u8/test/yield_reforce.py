# TODO: 如何 同时实现 yeild 与 return 的共存
# TODO: 如何修改 return 函数内的 yield 使之实现 迭代
def forever():
    print('starting')
    for i in range(1, 30):
        yield i*i
    print('for 执行完比')
    return 'over', 'completed', 'finish'

goo = forever()
for i in range(1, 30):
    f = next(goo)
    print(f'{i} * {i} = {f}')
s = forever()
print(s)


