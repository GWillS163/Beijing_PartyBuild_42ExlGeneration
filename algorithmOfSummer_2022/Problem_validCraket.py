import sys


class Solution:
    def __init__(self):
        self.symbol_dict ={
            "(": ")",
            "[": "]",
            "{": "}"
        }

    def isValid(self, s: str) -> bool:
        if len(s) % 2:
            return False
        lst = list(s)
        result = self.recursion(lst)
        return not result

    def recursion(self, lst, index=0):
        if not lst:
            return []

        while index < len(lst) - 1:
            if lst[index] in self.symbol_dict:
                if lst[index + 1] == self.symbol_dict[lst[index]]:  # match correctly
                    lst.pop(index)
                    lst.pop(index)
                    if not lst:
                        return []
                    self.recursion(lst)
            index += 1
        return lst


if __name__ == '__main__':
    # test the function
    s = Solution()
    print(s.isValid("{[]}"), True)
    print(s.isValid("(]"), False)
    print(s.isValid("()[]{}"), True)
    print(s.isValid("()[]{}["), False)