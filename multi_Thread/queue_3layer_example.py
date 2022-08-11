import queue
import threading
import time

q_2 = queue.Queue()
q_3 = queue.Queue()


def layer2():
    while True:
        item = q_2.get()
        print(f'layer 2: {"#" * item}', end='\r', flush=True)
        time.sleep(0.4)
        q_3.put(item)
        q_2.task_done()


def layer3():
    while True:
        item = q_3.get()
        # print(f'layer 3: {item}')
        # print slash loading animation here iteratively
        for _ in ['|', '-', '\\', '|', '-', '/']:
            print(f'layer 3: {item} {_}', end='\r', flush=True)
            time.sleep(0.2)
        # print('/', end='', flush=True)
        q_3.task_done()


# main
for t in range(1, 10):
    q_2.put(t)

t2 = threading.Thread(target=layer2, daemon=True)
# turn-on the worker thread
t3 = threading.Thread(target=layer3, daemon=True)
t2.start()

t3.start()
q_2.join()
q_3.join()

# block until all tasks are done
print('All work completed')
print('All task requests sent\n', end='')


