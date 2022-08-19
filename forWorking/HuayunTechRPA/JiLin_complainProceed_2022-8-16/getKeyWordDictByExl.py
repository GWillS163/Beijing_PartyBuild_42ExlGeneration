#  Author : Github: @GWillS163
#  Time: $(Date)
userDataContent = [[], []]
keywordDict = {}
lastName = None
for row in userDataContent[2:]:
    if not row[0] and not row[3:]:
        continue

    # 如果本行有值但无名则沿用上一行的名字
    name = row[0] if row[0] and row[3:] else lastName
    keywords = []
    for key in row[3:]:
        if not key:
            continue
        keywords.append(str(key))

    if row[0]:
        keywordDict.update({name: keywords})
    else:
        keywordDict[lastName] += keywords
    lastName = name