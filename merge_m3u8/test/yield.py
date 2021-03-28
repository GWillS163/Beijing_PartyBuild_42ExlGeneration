def forever():
    print('start forver')
    while True:
        print('----------')
        print('------------------')
        print('-----------------------------')
        yield 'break\n'

# forever()
fore = forever()
for i in range(5, 100):
    print(i)
    print(next(fore))

