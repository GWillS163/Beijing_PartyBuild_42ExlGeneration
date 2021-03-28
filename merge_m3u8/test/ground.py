import re

s = re.findall('([0-9|a-z]{32,33})', '://sgjk3.com/api/video/4802/key?sign=184485166d97d3267729133345c70cd3&t=16')
print(s)
