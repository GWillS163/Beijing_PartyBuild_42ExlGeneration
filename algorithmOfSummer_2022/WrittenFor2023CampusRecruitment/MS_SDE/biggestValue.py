#  Author : Github: @GWillS163
#  Time: $(Date)
# 检查最大回文子串，并补全


def solution(S="39878"):
    # get the maximum number of the s
    maxes = 0
    max_i = 0
    index = 0
    for i in S:
        if int(i) > maxes:
            maxes = int(i)
            max_i = index
        index += 1
    if not max_i == 0 or max_i == len(S):
        other_value = S[max_i + 1] if S[max_i + 1] > S[max_i - 1] else S[max_i - 1]
        if not other_value == "0":
            return f"{other_value}{maxes}{other_value}"
    return str(maxes)


if __name__ == '__main__':
    print(solution("00900"))
    print(solution("39878"))
    print(solution("54321"))
    print(solution("0000"))
    print('done')
    pass
