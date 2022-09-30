#  Author : Github: @GWillS163
#  Time: $(Date)


class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        symbol = {
            ")":"(",
            "]":"[",
            "}":"{"
        }
        for char in s:
            if char in "])}":
                if not stack:
                    return False
                if symbol[char] == stack[-1]:
                    stack.pop()
                else:
                    return False
            else:
                stack.append(char)
        return not stack

if __name__ == '__main__':
    # testScripts the function
    s = Solution()
    print(s.isValid("{[]}"), True)
    print(s.isValid("(]"), False)
    print(s.isValid("()[]{}"), True)
    print(s.isValid("()[]{}["), False)
    print(s.isValid("()[]{}[}"), False)
