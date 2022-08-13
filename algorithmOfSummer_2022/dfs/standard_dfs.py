#  Author : Github: @GWillS163
#  Time: $(Date)

def dfs(treeNode):
    if treeNode == None:
        return

    print(treeNode.val)
    for child in treeNode.children:
        dfs(child)