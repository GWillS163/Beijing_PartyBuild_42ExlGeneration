#  Author : Github: @GWillS163
#  Time: $(Date)

import time
import random

def run():
    print('thread 1:', end='  ')
    time.sleep(2)
    print(' ### acquering...', end='  ')
    time.sleep(2)
    print(' ### loading  ', end='')
    time.sleep(2)
    print('### sending  ', end='')
    time.sleep(2)
    print('## done..',)

def fake_multi_demo():
    print('thread 1:')
    print('thread 2:')
    print('thread 3:')
    print('thread 4:')
    print('thread 5:')
    time.sleep(2)
    print('----')
    print('thread 1:', end=' ')
    print('### acquiring')
    print('thread 2:', end=' ')
    print()
    print('thread 3:', end=' ')
    print()
    print('thread 4:', end=' ')
    print('### acquiring')
    print('thread 5:', end=' ')
    print()

def fake_multi_demo2():
    thread_info = { 'a': 'thread 1:',
                    'b': 'thread 2:',
                    'c': 'thread 3:'}

    for i in range(100):
        print(f'\n\n{"="*20}第{i}次打印')
        for i in thread_info.keys():
            print(thread_info[i])
        choice_task = random.choice(['a', 'b', 'c'])
        thread_info[choice_task] += '###random_task   '
        time.sleep(2)

def signle_thread_demo():
    output = ''
    for i in range(100):
        # if len(output) >= 20:
        #     print(output)
        #     output = '正在执行X:'
        output = output + '!'
        print(i, output, end='\r')
        time.sleep(1)
        # print(end='\r')
        # print('over', end='')


if __name__ == '__main__':
    # signle_thread_demo()
    # run()
    fake_multi_demo()
    # fake_multi_demo2()

    # dis-understandably

