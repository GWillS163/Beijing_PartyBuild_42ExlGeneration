#  Author : Github: @GWillS163
#  Time: $(Date)
import re


def regexTest():
    scopeStrs = """4
4或5
4或5或20
全选
1-4
1-4全选 
任选3个
1-4任选3个
1-4任选3个及以上"""
    # [1-4][全选|任选]\d个及以上
    # 纯数字: 4
    # [4或5]
    # ('4', None, None, None, None, None, None, None, None)
    # (None, '4', '5', None, None, None, None, None, None)
    # (None, None, None, None, None, '全选', None, None, None)
    # (None, None, None, '1', '4', None, None, None, None)
    # (None, None, None, '1', '4', '全选', None, None, None)
    # (None, None, None, None, None, None, '任选', '3', None)
    # (None, None, None, '1', '4', None, '任选', '3', None)
    # (None, None, None, '1', '4', None, '任选', '3', '及以上')
    for strs in scopeStrs.split('\n'):
        scopeRan = re.search(r"(?:^(\d{,3})$)|"
                             r"(^\d{,3}(?:或\d{,3})+$)|"
                             r"(?:^(\d{,3})-(\d{,3}))?(?:(全选)|(?:(任选)(\d{,3}))个(及以上)?$)?"
                             , strs).groups()

        scopeRan = re.search(r"(^\d{,3})$|(^\d{,3}(?:或\d{,3})+$)|(?:^(\d{,3})-(\d{,3}))?(?:(全选)|(任选)(\d{,3})-?(\d{,3})?个)?(及以上)?",
                             strs).groups()
        print(scopeRan)


def regexTest2():
    strings = """
4
23
4或5或20
4或5"""
    for strs in strings.split('\n'):
        if not strs:
            continue
        scopeRan = re.search(r"(?:(\d{1,3})(?:或(\d{1,3}))?)", strs).groups()
        print(scopeRan)


if __name__ == '__main__':
    regexTest()
    # regexTest2()
