import requests
import re


def phonetic_spelling(word):
    word = word.replace(" ", "_")
    phoneticSpelling = ""

    # url的格式有规律
    request = requests.get("https://en.oxforddictionaries.com/definition/" + word)
    html = request.text
    # 查看网页发现音标所处的行HTML格式有规律 使用正则表达式描述
    regularExpression = r'<span\s+class="phoneticspelling">/([^\/]*)/</span>'
    matchObject = re.search(regularExpression, html, re.I)
    if matchObject:
        if matchObject.group(1):
            phoneticSpelling = matchObject.group(1)
            print("\nphoneticSpelling: ", word, "--->", phoneticSpelling)
        else:
            print("\nword \"" + word + "\" has no phonetic spelling in the dictionary")
    else:
        print("\nword \"" + word + "\" has no phonetic spelling in the dictionary")

    return phoneticSpelling

def iciban(word):
    url = 'http://www.iciba.com/word?w=' + word
    head = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'UM_distinctid=1789ce269615cd-0ecd642fb175db-7166786d-130980-1789ce26962325',
        'Host': 'www.iciba.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68'}
    try:
        res = requests.get(url, headers=head)
        # pronunciation = re.findall(r'<li>美<!-- -->([[\s\S]*])<img', res.text)[0].replace('&#x27;', '\'')
        pronunciation = re.match(r'.*><li>([[\s\S]{2,18}])<img src=".*', res.text).groups(0)[0].replace('&#x27;', '\'')
        return pronunciation # 正则表达式有问题, 找不到关键词, 跳过了
    except Exception as E:
        print(E)
        return '[]'

# 测试
if __name__ == '__main__':
    print(iciban('Voices'))
    # print(phonetic_spelling("Chinese"))
    #
    # print(phonetic_spelling("English"))
    #
    # print(phonetic_spelling("translation"))
    #
    # print(phonetic_spelling("language"))
    #
    # print(phonetic_spelling("crawler"))
