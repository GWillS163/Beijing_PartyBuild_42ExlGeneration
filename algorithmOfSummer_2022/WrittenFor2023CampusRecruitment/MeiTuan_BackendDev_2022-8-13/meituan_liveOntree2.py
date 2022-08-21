#  Author : Github: @GWillS163
#  Time: $(Date)

class binaryTree:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def addLeft(self, value):
        if (self.value * 2) < value:
            return False
        self.left = binaryTree(value)
        return self.left

    def addRight(self, value):
        if (self.value * 2 + 1) < value:
            return False
        self.right = binaryTree(value)
        return self.right

    def preOder(self):
        print(self.value, end=" ")
        if self.left:
            self.left.preOder()
        if self.right:
            self.right.preOder()

    def iterTree(self):
        queue = [self]
        while queue:
            node = queue.pop(0)
            print(node.value)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        return queue


if __name__ == '__main__':
    # test the function
    root = binaryTree(1)
    a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 12]
    for i, n in enumerate(a):
        if i % 2 == 0:
            root.addLeft(n)
            # root = root.left
        else:
            root.addRight(n)
            # root = root.right

    # root.addLeft(2)
    # root.addRight(3)
    print("\npreOrder:", end=" ")
    root.preOder()

