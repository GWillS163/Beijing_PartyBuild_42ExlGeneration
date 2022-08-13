#  Author : Github: @GWillS163
#  Time: $(Date)
import queue

mountainMap = [[20, 30, 40],
               [100, 30, 50],
               [400, 80, 60]]

q = queue.Queue()


def dfs(rootNode):
    if rootNode is None:
        return
    q.put(rootNode)
    while not q.empty():
        node = q.get()
        print(node.val)
        for child in node.children:
            q.put(child)
