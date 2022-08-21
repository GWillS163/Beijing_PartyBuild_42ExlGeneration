#  Author : Github: @GWillS163
#  Time: $(Date)

nodes = [5, 7, 8]


# condition 1: leftChild(2*k) > n, not exist
# condition 2: rightChild(2*k + 1) > n, not exist

class treeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

    def addLeft(self, val):
        if self.val * 2 < val:
            return False
        self.left = treeNode(val)
        return self.left

    def addRight(self, val):
        if (self.val * 2 + 1) < val:
            return False
        self.right = treeNode(val)
        return self.right

    # insert the nodes into the tree
    def insert(self, nodes):
        for node in nodes:
            self.insertNode(node)

    def insertNode(self, node):
        if node < self.val:
            if self.left:
                self.left.insertNode(node)
            else:
                self.left = treeNode(node)
        else:
            if self.right:
                self.right.insertNode(node)
            else:
                self.right = treeNode(node)

    def preOder(self):
        print(self.val, end=" ")
        if self.left:
            self.left.preOder()
        if self.right:
            self.right.preOder()

# inesrt the nodes into the tree
root = treeNode(nodes[0])
root.addLeft(nodes[1])
root.addRight(nodes[2])
root.preOder()

