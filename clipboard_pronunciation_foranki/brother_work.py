for i in range(1,10000):
    if(i%11==10):
        print(i, '模3 =1')
        if(i % 3 == 2):
            print(i, '模3 & 模5 =1')
            if(i % 2 == 1):
                print(i, '是答案')
                break