import threading, queue

two = queue.Queue()
three = queue.Queue()


def three_layer():
    while True:
        item = three.get()
        print(f'layer 3 Working on {item}')
        three.task_done()


# turn-on the worker thread
threading.Thread(target=three_layer, daemon=True).start()


def two_layer():
    while True:
        rang = two.get()
        for n in range(1, 6):
            print('layer 2:', rang)
        three.put(rang)
        two.task_done()


threading.Thread(target=two_layer, daemon=True).start()


for t in range(1, 5):
    two.put(int(input('几个数字')))

print('All task requests sent\n', end='')


# block until all tasks are done
two.join()
three.join()
print('All work completed')