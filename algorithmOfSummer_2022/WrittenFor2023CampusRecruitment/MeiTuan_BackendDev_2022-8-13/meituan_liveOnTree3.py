# 美团 2023届秋招 技术综合-后端&数开&软件方向在线考试 - 正式考试阶段
# 编程题|20.0分1/1
# 生活在树上
# 时间限制： 3000MS
# 内存限制： 589824KB
# 题目描述：
# 给一棵有n个节点的二叉树，节点的编号从1到n。
#
# 其中，节点k的左儿子为节点2*k（当2*k大于n时，不存在左儿子）
#
# 节点k的右儿子为节点2*k+1（当2*k+1大于n时，不存在右儿子）
#
# 该二叉树的根节点为节点1。
#
#
#
# 对于每个节点，节点上有一些金钱。
#
# 现在你可以从根节点1开始，每次选择左儿子或者右儿子向下走，直到走到叶子节点停止，并获得你走过的这些节点上的金钱。
#
#
#
# 你的任务是求出你可以获得的最大的金钱总量。
#
#
#
# 输入描述
# 第一行是一个正整数n，表示二叉树上总共有n个节点。
#
# 第二行有n个正整数，第i个正整数表示节点i上有多少数量的金钱。
#
# 1 <= n <= 100000
#
# 对所有数据保证：单个节点上的金钱数量在 [1, 1000] 之间
#
# 输出描述
# 一行一个正整数，表示你所能获得的最大的金钱总量
#
#
# 样例输入
# 3
# 5 7 8
# 样例输出
# 13
#
# 提示
# 样例解释1
#
# 该样例中，二叉树上有三个节点，根节点为1号节点，其左儿子为2号节点，右儿子为3号节点，所能获取的最大金钱为13，为从1号节点走到3号节点，共获得5 + 8 = 13的金钱。
#
#
#
# 输入样例2
#
# 5
#
# 863 163 396 428 90
#
#
#
# 输出样例2
#
# 1454

n = int(input())
nodes = [int(i) for i in input().split()][:n]


# condition 1: leftChild(2*k) > n, not exist
# condition 2: rightChild(2*k + 1) > n, not exist

#  Author : Github: @GWillS163
#  Time: $(Date)

# construct
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


# turn list "a" to binary tree
def listToBinaryTree(a):
    if not a:
        return None
    root = treeNode(a[0])
    queue = [root]
    i = 1
    while i < len(a):
        node = queue.pop(0)
        if a[i] != None:
            node.left = treeNode(a[i])
            queue.append(node.left)
        i += 1
        if i < len(a) and a[i] != None:
            node.right = treeNode(a[i])
            queue.append(node.right)
        i += 1
    return root


# testScripts
def preOrder(root):
    if root:
        print(root.val, end=" ")
        preOrder(root.left)
        preOrder(root.right)


# this is the key!
def maxValuePath(root):
    if not root:
        return 0
    left = maxValuePath(root.left)
    right = maxValuePath(root.right)
    return max(left, right) + root.val


# nodes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 12]

root = listToBinaryTree(nodes)

print(maxValuePath(root))
