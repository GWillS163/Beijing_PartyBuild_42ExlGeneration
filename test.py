def BFS(tree, s):
    queue = [s]
    seen = set()
    seen.add(s)

    while len(queue):
        vertex = queue.pop(0)

        nodes = tree[vertex]
        for node in nodes:
            if node not in seen:
                queue.append(node)
                seen.add(node)
    return seen


if __name__ == '__main__':
    graph = {
        'A': ['B', 'C', 'D'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F', 'G'],
        'D': ['A', 'B', 'E', 'F'],
        'E': ['B', 'D', 'F'],
        'F': ['C', 'D', 'E'],
        'G': ['C']
    }
    BFS(graph, 'A')
    print(graph)

