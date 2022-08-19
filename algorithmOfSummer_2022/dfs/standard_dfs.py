#  Author : Github: @GWillS163
#  Time: $(Date)

def dfs(treeNode):
    if treeNode == None:
        return

    print(treeNode.val)
    for child in treeNode.children:
        dfs(child)


def dfs_binaryTree(root):
    if root == None:
        return
    print(root.val)
    for child in root.children:
        dfs_binaryTree(child)