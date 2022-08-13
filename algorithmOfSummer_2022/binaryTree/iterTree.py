
class binaryTree:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def addLeft(self, value):
        self.left = binaryTree(value)
        return self.left

    def addRight(self, value):
        self.right = binaryTree(value)
        return self.right

    def preOder(self):
        print(self.value, end=" ")
        if self.left:
            self.left.preOder()
        if self.right:
            self.right.preOder()

    def midOrder(self):
        if self.left:
            self.left.midOrder()
        print(self.value, end=" ")
        if self.right:
            self.right.midOrder()

    def postOrder(self):
        if self.left:
            self.left.postOrder()
        if self.right:
            self.right.postOrder()
        print(self.value, end=" ")


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
    root.addLeft(2)
    root.addRight(3)
    print("\npreOrder:", end=" ")
    root.preOder()
    print("\nmidOrder:", end=" ")
    root.midOrder()
    print("\npostOrder:", end=" ")
    root.postOrder()
