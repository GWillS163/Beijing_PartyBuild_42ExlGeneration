from spider_pronunciation import phonetic_spelling

#读取剪贴板

ret_text = ''
#爬取网页
raw_text = 'Pieces Clothes Watches Voices'
words = [i for i in raw_text.split(' ')]
import requests
for word in words:
    print(url+word)
    ret_text += '[' + phonetic_spelling(word) + ']'


#发送至剪贴板

